#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame
import sys
import os
import json

from lib.session import Session
from lib.conn import ChatFactory
import lib.scroll_bgmanager as scroll_bgmanager
import lib.scroll_group as scroll_group

from twisted.internet import reactor
from pygame.locals import *

PORT = 9234
FPS = 90
RES = (800, 600)


def game_init(host=None, port=None, nickname=None):
    clock = pygame.time.Clock()

    background = pygame.image.load(os.path.join('assets', 'montreal.jpg'))
    screen = pygame.display.set_mode(RES)

    bgManager = scroll_bgmanager.BackgroundManager(screen, background)

    session = Session()

    serverClient = ChatFactory()
    reactor.connectTCP(host, port, serverClient)

    get_players = {'command': 'get_players'}
    serverClient.sendMessage(json.dumps(get_players))

    print session.players
    print "checking in session about player %s" % nickname
    print "player exists: %s" % session.player_exists(nickname)

    if session.player_exists(nickname):
        sys.exit(0)

    local_group = scroll_group.ScrollSpriteGroup(bgManager)
    session.set_scroll_group(local_group)

    player = session.create_player(nickname)
    session.set_local_player(player)

    local_group.add(player)

    bgManager.BlitSelf(screen)
    pygame.display.flip()

    def _loop():

        serverClient.sendMessage(player.get_status())
        clock.tick(FPS)
        for p in session.get_players():
            if p != player:
                if pygame.sprite.collide_rect(player, p):
                    player.speed = 0

        for event in pygame.event.get():
            if not hasattr(event, 'key'):
                continue
            down = event.type == KEYDOWN
            if event.key == K_RIGHT:
                player.k_right = down * -5
                player.k_down = down * -0.2
            elif event.key == K_LEFT:
                player.k_left = down * 5
                player.k_down = down * -0.2
            elif event.key == K_UP:
                player.k_up = down * 0.2
            elif event.key == K_DOWN:
                player.k_down = down * -0.4
            elif event.key == K_ESCAPE:
                status = {'status': 'disconnected', 'name': player.name}
                serverClient.sendMessage(json.dumps(status))
                reactor.stop()
                pygame.quit()
                sys.exit(0)


        bgManager.NotifyPlayerSpritePos(player.rect)

        local_group.clear(screen)
        local_group.update()
        changedRects = local_group.draw(screen)
        pygame.display.update(changedRects)
        reactor.callLater(1. / FPS, _loop)

    status = {'status': 'connected', 'name': nickname}
    serverClient.sendMessage(json.dumps(status))

    _loop()


def usage():
    print "Usage:"
    print "main.py host nickname\n"
    sys.exit(0)

if __name__ == '__main__':
    if len(sys.argv) != 3:
        usage()
    else:
        host, nickname = sys.argv[1], sys.argv[2]
        try:
            game_init(host=host, port=PORT, nickname=nickname)
            reactor.run()
        except SystemExit:
            pass
