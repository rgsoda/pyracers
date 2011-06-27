#!/usr/bin/env python
# -*- coding: utf-8 -*-
from player import Player


class Session:

    class __impl:
        players = []
        local_player = None

        def spam(self):
            return id(self)

        def set_local_player(self, nick):
            self.local_player = nick

        def create_player(self, nick):
            player = Player(name=nick, position=(400, 300))
            self.players.append(player)

        def update_player(self, nick, position, direction):
            for p in self.players:
                if p.name == nick:
                    p.position = position
                    p.direction = direction

        def append_player(self, player):
            self.players.append(player)

        def get_players(self):
            return self.players

    __instance = None

    def __init__(self):

        if Session.__instance is None:
            Session.__instance = Session.__impl()

        self.__dict__['_Session__instance'] = Session.__instance

    def __getattr__(self, attr):
        return getattr(self.__instance, attr)

    def __setattr__(self, attr, value):
        return setattr(self.__instance, attr, value)
