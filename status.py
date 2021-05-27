from pics import images
import pygame


class Status(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)
        self.image = images['start']
        self.rect = self.image.get_rect().move(126, 27)
        self.status = 0

    def win(self):
        self.image = images['win']
        self.status = 1

    def lose(self):
        self.image = images['lose']
        self.status = 2

    def start(self):
        self.image = images['start']
        self.status = 0

    def finished(self):
        return self.status

