import os

RBX_ENV = os.getenv('RBX_ENV', 'dev')
RBX_PROJECT = f'{RBX_ENV}-platform-eu'
