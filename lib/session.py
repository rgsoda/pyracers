#!/usr/bin/env python
# -*- coding: utf-8 -*-
from lib.player import Player


class Session:

    class __impl:
        players = {}
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
            if not nick in self.players:
                print "Creating user %s" % nick
                player = Player(name=nick, position=(400, 300))
                self.players[nick] = player
                self.scroll_group.add(player)
                return player
            else:
                print "NOT Creating user %s" % nick

        def remove_player(self, nick):
            p = self.players.get(nick, None)
            if p:
                del self.players[nick]
                self.scroll_group.remove(p)

        def update_player(self, nick, position, speed, direction):
            p = self.players.get(nick, None)
            if p:
                p.speed = speed
                p.position = position
                p.direction = direction

        def get_player_names(self):
            return self.players.keys()

        def get_players(self):
            return self.players.values()

        def player_exists(self, name):
            return name in self.players

    __instance = None

    def __init__(self):

        if Session.__instance is None:
            Session.__instance = Session.__impl()

        self.__dict__['_Session__instance'] = Session.__instance

    def __getattr__(self, attr):
        return getattr(self.__instance, attr)

    def __setattr__(self, attr, value):
        return setattr(self.__instance, attr, value)
