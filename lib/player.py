#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pygame
import math
import json
import os
# from lib.subpixelsurface import SubPixelSurface


class Player(pygame.sprite.Sprite):
    MAX_FORWARD_SPEED = 15
    MAX_REVERSE_SPEED = 0.2
    ACCELERATION = 0.02
    TURN_SPEED = 0.02

    def __repr__(self):
        return "Player %s pos: %s" % (self.name, self.position)

    def __init__(self, image=None, position=None, name=None):
        if image == None:
            image = 'car.png'
        pygame.sprite.Sprite.__init__(self)
        self.sprite_image = pygame.image.load(os.path.join('assets', image))
        # self.sprite_image_subpixel = SubPixelSurface(
        #     self.sprite_image, x_level=4)
        self.rect = self.sprite_image.get_rect()
        self.position = position
        self.speed = self.direction = 0
        self.k_left = self.k_right = self.k_down = self.k_up = 0
        self.name = name

    def update(self):
        # SIMULATION
        self.speed += (self.k_up + self.k_down)
        if (self.speed > self.MAX_FORWARD_SPEED):
            self.speed = self.MAX_FORWARD_SPEED
        if (self.speed < -self.MAX_REVERSE_SPEED):
            self.speed = self.MAX_REVERSE_SPEED
        self.direction += (self.k_right + self.k_left)
        x, y = self.position
        rad = self.direction * math.pi / 180
        x += self.speed * -1 * math.sin(rad)
        y += self.speed * -1 * math.cos(rad)
        self.position = (x, y)
        self.image = pygame.transform.rotate(self.sprite_image, self.direction)
        self.rect = self.image.get_rect()
        self.rect.center = self.position

    def get_status(self):
        status = {
            'status': "pos_update",
            'pos': self.position,
            'speed': self.speed,
            'direction': self.direction,
            'name': self.name
        }
        return json.dumps(status)
