'''
description challenge response exercise
author Raphael Margueron, Lucas Bulloni
date 09.03.2018
'''

import secrets

from diffiehellman.diffiehellman import DiffieHellman

class Server():
    def __init__(self):
        self.used_nonce = set()
        self.diffiehellman = DiffieHellman()
        self.public_key = None
        self.shared_secret = None

    def response(self):
        print('Im a server')

class Client():
    def __init__(self):
        self.shared_secret = None
        self.diffiehellman = DiffieHellman()
        self.public_key = None

    def request(self):
        print('Im a client')

if __name__ == '__main__':
    print('hello world')
    print(secrets.randbits(64))