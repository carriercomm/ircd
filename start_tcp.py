#!/usr/bin/env python

import logging
import tornado.ioloop
from servers.tcpserver import TCPServer
import config

if __name__ == '__main__':
    logging.getLogger().setLevel(logging.DEBUG)
    server = TCPServer(config)
    tornado.ioloop.IOLoop.instance().start()
