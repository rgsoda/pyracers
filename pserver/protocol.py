#!/usr/bin/env python
# -*- coding: utf-8 -*-

from twisted.internet.protocol import Factory
from twisted.protocols.basic import LineReceiver
from twisted.internet import reactor
import json


class PyRacerProto(LineReceiver):

    def connectionMade(self):
        pass

    def connectionLost(self, reason):
        for c in self.factory.clients:
            if c['client'] == self:
                self.factory.clients.remove(c)

    def lineReceived(self, data):
        self.parse_message(data)

    def message_others(self, data):
        for c in self.factory.clients:
            if c['client'] != self:
                c['client'].sendLine(data)

    def get_usernames(self):
        usernames = []
        for c in self.factory.clients:
            usernames.append(c['name'])

    def parse_message(self, message):
        msg = None
        if message:
            try:
                msg = json.loads(message)
                if msg.get('status') == 'connected':
                    print msg
                    name = msg.get('name')
                    self.message_others(message)
                    self.factory.clients.append({'name': name, 'client': self})
                if msg.get('status') == 'disconnected':
                    self.message_others(message)
                if msg.get('status') == 'pos_update':
                    self.message_others(message)
                if msg.get('command') == 'get_players':
                    print msg
                    data = {
                        'status': 'players',
                        'players': self.get_usernames(),
                    }
                    self.sendLine(json.dumps(data))
            except Exception, e:
                print e


class ServerFactory(Factory):

    protocol = PyRacerProto

    def __init__(self):
        self.clients = []


if __name__ == '__main__':

    factory = ServerFactory()
    reactor.listenTCP(9234, factory)
    reactor.run()
