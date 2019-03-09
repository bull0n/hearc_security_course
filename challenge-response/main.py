'''
description challenge response exercise
author Raphael Margueron, Lucas Bulloni
date 09.03.2018
'''

import secrets
import time
import hashlib
from enum import Enum

def calculate_hash(nonce, password):
    encoded_string = (str(nonce) + password).encode('utf8')
    return hashlib.sha256(encoded_string).hexdigest()

class Server():
    TIMEOUT_DELTA = 1000

    class Message(Enum):
        CONNECTION_SUCESSFUL = 1 # the login is ok
        NO_NONCE_ASKED = 2 #
        NONCE_TIMEDOUT = 3 # in case of a delayed login
        INVALID_USER = 4 # if the user is not registered

    def __init__(self):
        self.users = {} # key : login, value : password
        self.available_nonce = {} # key : login, value : list((nonce , time))

    def register_client(self, client):
        self.users[client.login] = client.password

    def generate_nonce(self, client_login):
        nonce = secrets.randbits(64)

        if client_login not in self.available_nonce:
            self.available_nonce[client_login] = []

        self.available_nonce[client_login].append((nonce, time.time() + Server.TIMEOUT_DELTA))
        return nonce

    def try_authenticate(self, login, sended_hash):
        if login not in self.users:
            return Server.Message.INVALID_USER

        if login not in self.available_nonce:
            return Server.Message.NO_NONCE_ASKED

        possible_nonces = self.available_nonce[login]
        password = self.users[login]

        for nonce, timeout in possible_nonces:
            expected_hash = calculate_hash(nonce, password)
            if expected_hash == sended_hash:
                if time.time() <= timeout:
                    return Server.Message.CONNECTION_SUCESSFUL
                else:
                    return Server.Message.NONCE_TIMEDOUT

        return False


class Client():
    def __init__(self, login, password):
        self.login = login
        self.password = password

    def ask_nonce(self, server):
        return server.generate_nonce(self.login)

    def authenticate(self, server, nonce):
        login_hash = calculate_hash(nonce, self.password)
        return server.try_authenticate(self.login, login_hash)

class UseCases:
    @staticmethod
    def get_accounts():
        server = Server()
        client = Client("Alex", "t3rr1eur")
        server.register_client(client)
        return client, server

    @staticmethod
    def show_result(server_message):
        if server_message == Server.Message.CONNECTION_SUCESSFUL:
            print("Connection sucessful")
        elif server_message == Server.Message.INVALID_USER:
            print("Connection failed : invalid user")
        elif server_message == Server.Message.NONCE_TIMEDOUT:
            print("Connection failed : nonce timed out")
        elif server_message == Server.Message.NO_NONCE_ASKED:
            print("Connection failed : invalid user")

    @staticmethod
    def sucessful():
        client, server = UseCases.get_accounts()
        nonce = client.ask_nonce(server)
        is_ok = client.authenticate(server, nonce)
        UseCases.show_result(is_ok)

    @staticmethod
    def failure_time():
        client, server = UseCases.get_accounts()
        nonce = client.ask_nonce(server)
        time.sleep(Server.TIMEOUT_DELTA / 1000.0 + 1)
        is_ok = client.authenticate(server, nonce)
        UseCases.show_result(is_ok)

    @staticmethod
    def replay_attack():
        pass

if __name__ == '__main__':
    UseCases.sucessful()
    UseCases.failure_time()
