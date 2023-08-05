#!/usr/bin/env python3
# @author zeppelsoftware/b3z
# zeppel.eu
# repository: github.com/zeppelsoftware/pyny
# (c)2020 Zeppel


import os
import configparser
import socket
import sys
from http.server import HTTPServer, CGIHTTPRequestHandler

__all__ = ["run"]

version = "1.0.7"
class Config:
    file = "pyny.config"
    section = "pyny Web"
    port = 8080
    root = "html"

    @staticmethod
    def load():
        c = configparser.ConfigParser()
        c.read(Config.file)
        return c

def run():
    # load config if exists
    if os.path.isfile(Config.file):
        configuration = {}
        config = Config.load()
        options = config.options(Config.section)
        for option in options:
            try:
                configuration[option] = config.get(Config.section, option)
            except:
                raise Exception(f'Config File broken. Check {configuration[option]}.')
        #apply
        Config.root = configuration['webroot']
        Config.port = int(configuration['port'])

    else:
        # create new config file if not
        conf = configparser.ConfigParser()
        conf.add_section(Config.section)
        conf.set(Config.section, 'webroot', str(Config.root))
        conf.set(Config.section, 'port', str(Config.port))

        conffile = open(Config.file, 'w')
        conf.write(conffile)
        conffile.close()

    # check & set web root
    if not os.path.isdir(Config.root):
        os.makedirs(Config.root)
    os.chdir(Config.root)

    # check if port is available
    if socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect_ex(("127.0.0.1", Config.port)) == 0:
        raise ConnectionError(f'Port {Config.port} is not available.')

    print("                           __    __     _     \n _ __  _   _ _ __  _   _  / / /\ \ \___| |__  \n| '_ \| | | | '_ \| | | | \ \/  \/ / _ \ '_ \ \n| |_) | |_| | | | | |_| |  \  /\  /  __/ |_) |\n| .__/ \__, |_| |_|\__, |   \/  \/ \___|_.__/ \n|_|    |___/       |___/\n\n")
    print(f'Version {version}\n')
    print(f'Webserver available at http://127.0.0.1:{Config.port}')

    httpServer = HTTPServer(('', Config.port), CGIHTTPRequestHandler)
    httpServer.serve_forever()


