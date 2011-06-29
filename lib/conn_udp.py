#!/usr/bin/env python
# -*- coding: utf-8 -*-
from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor
import json
from lib.session import Session


class ServerClient(DatagramProtocol):

    session = Session()

    def __init__(self, host=None, port=None):
        print "init"
        self.host = host
        self.port = port

    def startProtocol(self):
        self.transport.connect(self.host, self.port)
        self.transport.write("hello")  # no need for address

    def datagramReceived(self, data, (host, port)):
        # print "received %r from %s:%d" % (data, host, port)
        self.parse_message(data)

    # Possibly invoked if there is no server listening on the
    # address to which we are sending.
    def connectionRefused(self):
        print "No one listening"

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
                speed = msg.get('speed')
                direction = msg.get('direction')
                self.session.update_player(nick=nick,
                                           position=pos,
                                           speed=speed,
                                           direction=direction)
        except Exception:
            pass


# 0 means any port, we don't care in this case
# reactor.listenUDP(0, ServerClient('127.0.0.1', 9234))
# reactor.run
