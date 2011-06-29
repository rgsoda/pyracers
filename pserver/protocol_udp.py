#!/usr/bin/env python
# -*- coding: utf-8 -*-

from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor
import json


class Echo(DatagramProtocol):

    def __init__(self):
        self.clients = {}

    def datagramReceived(self, data, (host, port)):
        self.parse_message(data, (host, port))

    def message_others(self, data, sender_dest):
        for name, dest in self.clients.items():
            if dest != sender_dest:
                self.transport.write(data, dest)

    def parse_message(self, message, dest):
        msg = None
        if message:
            try:
                msg = json.loads(message)
                if msg.get('status') == 'connected':
                    print msg
                    name = msg.get('name')
                    self.message_others(message, dest)
                    self.clients[name] = dest
                if msg.get('status') == 'disconnected':
                    self.message_others(message, dest)

                if msg.get('status') == 'pos_update':
                    self.message_others(message, dest)
                if msg.get('command') == 'get_players':
                    print msg
                    data = {
                        'status': 'players',
                        'players': self.get_usernames(),
                    }
                    self.transport.write(json.dumps(data), dest)
            except Exception, e:
                print e


reactor.listenUDP(9234, Echo())
reactor.run()
