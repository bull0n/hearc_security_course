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
        self.shared_secret = None

    def response():
        print('Im a server')

class Client():
    def __init__(self):
        self.shared_secret = None

if __name__ == '__main__':
    print('hello world')
    print(secrets.randbits(64))
