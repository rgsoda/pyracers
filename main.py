#!/usr/bin/env python
# -*- coding: utf-8 -*-

# INTIALISATION
import pygame
import sys
import os
import json
from player import Player
from session import Session
from conn import ChatFactory
from twisted.internet import reactor
from pygame.locals import *

PORT = 9234
FPS = 45


def game_init(host=None, port=None, nickname=None):

    background = pygame.image.load(os.path.join('assets', 'track.jpg'))
    size = (width, height) = background.get_size()
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()

    session = Session()

    serverClient = ChatFactory()
    reactor.connectTCP(host, port, serverClient)
    rect = screen.get_rect()

    player = Player('car.png', rect.center, nickname)
    session.append_player(player)
    session.set_local_player(nickname)

    def _loop():
        player_group = pygame.sprite.RenderPlain(session.get_players())

        serverClient.sendMessage(player.get_status())
        deltat = clock.tick(FPS)
        for event in pygame.event.get():

            if not hasattr(event, 'key'):
                continue
            down = event.type == KEYDOWN

            if event.key == K_RIGHT:
                player.k_right = down * -5
                player.k_down = down * - 0.02
            elif event.key == K_LEFT:
                player.k_left = down * 5
                player.k_down = down * - 0.02
            elif event.key == K_UP:
                player.k_up = down * 2
            elif event.key == K_DOWN:
                player.k_down = down * -2
            elif event.key == K_ESCAPE:
                status = {'status': 'disconnected', 'name': player.name}
                serverClient.sendMessage(json.dumps(status))
                sys.exit(0)
        screen.blit(background, background.get_rect())
        player_group.update(deltat)
        player_group.draw(screen)
        pygame.display.flip()
        reactor.callLater(1. / FPS, _loop)

    status = {'status': 'connected', 'name': nickname}
    serverClient.sendMessage(json.dumps(status))

    get_players = {'command': 'get_players'}
    serverClient.sendMessage(json.dumps(get_players))

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
        game_init(host=host, port=PORT, nickname=nickname)
        reactor.run()
