#!/usr/bin/env python
# -*- coding: utf-8 -*-

from twisted.internet import reactor
from twisted.internet.protocol import ClientFactory
from twisted.protocols.basic import LineReceiver
import json
from lib.session import Session


class ChatClient(LineReceiver):

    session = Session()

    def connectionMade(self):
        self.factory.clientReady(self)

    def lineReceived(self, line):
        self.parse_message(line)

    def connectionLost(self, reason):
        pass

    def parse_message(self, message):
        msg = None
        try:
            msg = json.loads(message)
            if msg.get('status') == 'players':
                for nick in msg.get('players'):
                    self.session.create_player(nick)
                self.session.set_session_ready(True)
            if msg.get('status') == 'connected':
                nick = msg.get('name')
                self.session.create_player(nick)
            if msg.get('status') == 'disconnected':
                nick = msg.get('name')
                self.session.remove_player(nick)
            if msg.get('status') == 'pos_update':
                pos = msg.get('pos')
                nick = msg.get('name')
                direction = msg.get('direction')
                self.session.update_player(nick=nick,
                                           position=pos, direction=direction)
        except Exception:
            pass


class ChatFactory(ClientFactory):
    protocol = ChatClient

    clientInstance = None
    messageQueue = []

    def clientConnectionFailed(self, connector, reason):
        reactor.stop()

    def clientConnectionLost(self, connector, reason):
        pass

    def startFactory(self):
        self.messageQueue = []
        self.clientInstance = None

    def clientReady(self, instance):
        self.clientInstance = instance
        for msg in self.messageQueue:
            self.sendMessage(msg)

    def sendMessage(self, msg='Hey there'):
        if self.clientInstance is not None:
            self.clientInstance.sendLine("%s%s" % (msg, '\r\n'))
        else:
            self.messageQueue.append(msg)
