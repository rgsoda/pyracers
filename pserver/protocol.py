#!/usr/bin/env python
# -*- coding: utf-8 -*-

from twisted.internet.protocol import Factory
from twisted.protocols.basic import LineReceiver
from twisted.internet import reactor
import json


class PyRacerProto(LineReceiver):

    def connectionMade(self):
        self.factory.clients.append(self)

    def connectionLost(self, reason):
        self.factory.clients.remove(self)

    def lineReceived(self, data):
        self.parse_message(data)

    def message_others(self, data):
        for c in self.factory.clients:
            if c != self:
                c.sendLine(data)

    def parse_message(self, message):
        msg = None
        if message:
            try:
                msg = json.loads(message)
                if msg.get('status') == 'connected':
                    self.factory.users.append(msg.get('name'))
                    self.message_others(message)
                if msg.get('status') == 'pos_update':
                    self.message_others(message)
                if msg.get('command') == 'get_players':
                    data = {'status': 'players', 'players': self.factory.users}
                    self.sendLine(json.dumps(data))
            except Exception, e:
                print e


class ServerFactory(Factory):

    protocol = PyRacerProto

    def __init__(self):
        self.clients = []
        self.users = []


if __name__ == '__main__':

    factory = ServerFactory()
    reactor.listenTCP(9234, factory)
    reactor.run()
