'''
Name: ssh-pymongo
Version: 1.0.4 (base version of fork)
Summary: Simple shortcut for PyMongo over ssh.
Home-page: https://github.com/mindey/ssh-pymongo
Author: Mindey, forked and adapted by H. Brendebach (github: @HBrendy)
License: MIT
'''

import getpass
import urllib

import pymongo
from sshtunnel import SSHTunnelForwarder


class MongoSession:

    def __init__(self, host, user = None, password = None, key = None, key_password = None, port = 22, uri = 'mongodb://127.0.0.1:27017', to_host = '127.0.0.1', to_port = 27017):

        HOST = (host, port)
        USER = user or getpass.getuser()
        KEY = key or f'/home/{USER}/.ssh/id_rsa'
        KEY_PASSWORD = key_password
        self.to_host = to_host
        self.uri = uri;
        URI = urllib.parse.urlparse(uri)

        if uri:
            to_host = URI.hostname or to_host
            to_port = URI.port or to_port

        if password:
            self.server = SSHTunnelForwarder(
                HOST,
                ssh_username = USER,
                ssh_password = password,
                remote_bind_address = (to_host, to_port)
            )
        else:
            self.server = SSHTunnelForwarder(
                HOST,
                ssh_username = USER,
                ssh_pkey = KEY,
                ssh_private_key_password = KEY_PASSWORD,
                remote_bind_address = (to_host, to_port)
            )

        self.start()

    def start(self):
        self.server.start()

        source_uri = urllib.parse.urlparse(self.uri)
        tunnel_uri = source_uri._replace(netloc = source_uri.netloc.replace(str(source_uri.port), str(self.server.local_bind_port)))

        self.connection = pymongo.MongoClient(host = tunnel_uri.geturl())

    def stop(self):
        self.connection.close()
        self.server.stop()
        del self.connection

    def close(self):
        self.stop()
