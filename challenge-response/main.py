"""
Description : challenge response exercise
"""

import secrets
import time
import hashlib
from enum import Enum

__author__ = "Raphael Margueron and Lucas Bulloni"
__version__ = "1.0"
__email__ = "raphael.margueron@he-arc.ch / lucas.bulloni@he-arc.ch"
__date__ = "09.03.2018"

"""
Questions-réponses :
- quel hachage cryptographique utilisez-vous et pourquoi ?
    - sha3_512 : car il est implémenté avec SHA-3[1] qui il n'a pas encore de vulnérabilité trouvé[2], 256 pour avoir une faible probabilité de colision
- quelles précautions pour le générateur aléatoire ?
    - secrets.token_bytes : car les nombres aléatoires généré sont cryptographiquement sûrs[3] avec une taille de 64 octets car 32 étaient considéré comme bon contre les attaques brut force en 2015[4]
- quelles précautions pour la construction garantissant l'unicité du nonce ?
    - avoir peu de chance de colisions avoir des grands hashes
- quelles précautions pour la durée de validité du nonce ?
    - stocker une date de péremption assez proche dans le temps pour ne pas permettre que le nonce fuite et assez éloigné dans le temps pour ne pas empêcher l'utilisateur de se connecter dû à un trop long délais entre les différentes requêtes

sources :
    - [1] : https://docs.python.org/3/library/hashlib.html#hash-algorithms
    - [2] : https://en.wikipedia.org/wiki/Cryptographic_hash_function#Attacks_on_cryptographic_hash_algorithms
    - [3] : https://docs.python.org/3/library/secrets.html
    - [4] : https://docs.python.org/3/library/secrets.html#how-many-bytes-should-tokens-use
"""


def calculate_hash(nonce, password):
    """Create a hash from the nonce and the password"""
    encoded_string = (str(nonce) + password).encode("utf8")
    return hashlib.sha3_512(encoded_string).hexdigest()


class Server():
    """A CHAP authentication server class"""

    # Nonce avaiable time
    TIMEOUT_DELTA = 0.2  # seconds

    # False == less verbose
    DEBUG = True
    NONCE_SIZE = 64

    class Message(Enum):
        """Authentication result message enum"""
        # the login is ok
        CONNECTION_SUCESSFUL = 0
        # unknon connection failed
        CONNECTION_FAILED = 1
        # in case of a delayed login
        NONCE_TIMEDOUT = 2
        # if the user is not registered
        INVALID_USER = 3
        # if the nonce is not available (in case of replay attack)
        INVALID_NONCE = 4

    @staticmethod
    def message(message):
        """Use to hide the error type when in debug"""
        if message == Server.Message.CONNECTION_SUCESSFUL or Server.DEBUG:
            return message
        else:
            return Server.Message.CONNECTION_FAILED

    def __init__(self):
        # key : login, value : plain text password
        self.users = {}
        # key : login, value : list((nonce, time))
        # values are lists
        # pro : avoid DoS attack, because if a mischievous client spam nonce generation for a targeted client, the targed client wont be able to authenticate in case of a single nonce per client
        # con : the serve could be overloaded with useless nonces
        # the con could be fixed with a deamon service that clear every expired nonces
        self.available_nonce = {}

    def register_client(self, client):
        """Add a user to the server users list"""
        self.users[client.login] = client.password

    def generate_nonce(self, client_login):
        """Generate a nonce for a specific login"""
        nonce = secrets.token_bytes(Server.NONCE_SIZE)

        # Create an array for this user if it doesnt exist
        if client_login not in self.available_nonce:
            self.available_nonce[client_login] = []

        self.available_nonce[client_login].append(
            (nonce, time.time() + Server.TIMEOUT_DELTA))
        return nonce

    def try_authenticate(self, login, sended_hash):
        """Try to authenticate a user with a specific login and a specific hash"""
        if login not in self.users:
            return Server.message(Server.Message.INVALID_USER)

        if login not in self.available_nonce:
            return Server.message(Server.Message.INVALID_NONCE)

        possible_nonces = self.available_nonce[login]
        password = self.users[login]

        for nonce, timeout in possible_nonces:
            expected_hash = calculate_hash(nonce, password)
            if expected_hash == sended_hash:
                # reset the nonce list for this user
                self.available_nonce[login] = []
                if time.time() <= timeout:
                    return Server.message(Server.Message.CONNECTION_SUCESSFUL)
                else:
                    return Server.message(Server.Message.NONCE_TIMEDOUT)

        return Server.message(Server.Message.INVALID_NONCE)


class Client():
    """Data client class, used to store user/password"""
    def __init__(self, login, password):
        self.login = login
        self.password = password

    def ask_nonce(self, server):
        return server.generate_nonce(self.login)

    def generate_login_message(self, nonce):
        return calculate_hash(nonce, self.password)


class UseCases:
    """Various use cases for the CHAP implementation"""
    @staticmethod
    def get_accounts():
        server = Server()
        client = Client("Alex", "t3rr1eur")
        server.register_client(client)
        return client, server

    @staticmethod
    def show_result(server_message):
        if server_message == Server.Message.CONNECTION_SUCESSFUL:
            print("  Connection sucessful")
        elif server_message == Server.Message.CONNECTION_FAILED:
            print("  Connection failed")
        elif server_message == Server.Message.INVALID_USER:
            print("  Connection failed : invalid user")
        elif server_message == Server.Message.NONCE_TIMEDOUT:
            print("  Connection failed : nonce timed out")
        elif server_message == Server.Message.INVALID_NONCE:
            print("  Connection failed : invalid nonce")
        else:
            print("  unhandeled server_message")

    @staticmethod
    def sucessful():
        """Simple exemple with a sucessful login"""
        print("Use case authentication sucessful : ")
        # retives accounts
        client, server = UseCases.get_accounts()
        # the client ask for a nonce
        nonce = client.ask_nonce(server)
        # with this nonce
        login_message = client.generate_login_message(nonce)
        is_ok = server.try_authenticate(client.login, login_message)
        UseCases.show_result(is_ok)

    @staticmethod
    def failure_time():
        print("Use case nonce timeout : ")
        client, server = UseCases.get_accounts()
        nonce = client.ask_nonce(server)
        # wait until the nonce expired
        time.sleep(Server.TIMEOUT_DELTA + 0.1)
        login_message = client.generate_login_message(nonce)
        is_ok = server.try_authenticate(client.login, login_message)
        UseCases.show_result(is_ok)

    @staticmethod
    def replay_attack():
        print("Use case replay attack : ")
        client, server = UseCases.get_accounts()
        nonce = client.ask_nonce(server)
        login_message = client.generate_login_message(nonce)
        # use the nonce, once
        is_ok = server.try_authenticate(client.login, login_message)
        UseCases.show_result(is_ok)
        # use the nonce, a second time, simulate a replay attack
        is_ok = server.try_authenticate(client.login, login_message)
        UseCases.show_result(is_ok)

    @staticmethod
    def wrong_password():
        print("Use case wrong password : ")
        client, server = UseCases.get_accounts()
        client.password = "alterated password"
        nonce = client.ask_nonce(server)
        # create login_message with the wrong password
        login_message = client.generate_login_message(nonce)
        is_ok = server.try_authenticate(client.login, login_message)
        UseCases.show_result(is_ok)

    @staticmethod
    def invalid_login():
        print("Use case invalid login : ")
        client, server = UseCases.get_accounts()
        nonce = client.ask_nonce(server)
        login_message = client.generate_login_message(nonce)
        # try to authenticate with a bad login
        is_ok = server.try_authenticate("other login", login_message)
        UseCases.show_result(is_ok)


if __name__ == "__main__":
    UseCases.sucessful()
    UseCases.failure_time()
    UseCases.replay_attack()
    UseCases.wrong_password()
    UseCases.invalid_login()
