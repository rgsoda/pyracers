#!/usr/bin/env python
# -*- coding: utf-8 -*-
from lib.player import Player
import copy


class Session:

    class __impl:
        players = []
        local_player = None
        ready = False
        scroll_group = None

        def spam(self):
            return id(self)

        def set_scroll_group(self, group):
            self.scroll_group = group

        def set_local_player(self, player):
            self.local_player = player

        def set_session_ready(self, val):
            self.ready = val

        def is_ready(self):
            return self.ready

        def create_player(self, nick):
            if not contains(self.players, lambda x: x.name == nick):
                print "Creating user %s" % nick
                player = Player(name=nick, position=(400, 300))
                self.players.append(player)
                self.scroll_group.add(player)
                return player
            else:
                print "NOT Creating user %s" % nick

        def update_player(self, nick, position, direction):
            for p in self.players:
                if p.name == nick:
                    p.position = position
                    p.direction = direction

        def get_player_names(self):
            names = []
            for p in self.players:
                names.append(p.name)
            return names

        def player_exists(self, name):
            return contains(self.players, lambda x: x.name == name)

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


def contains(list, filter):
    for x in list:
        if filter(x):
            return True
    return False
