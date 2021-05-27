from pics import images
import pygame


class RedCounter(pygame.sprite.Group):
    def __init__(self, offset):
        super().__init__()
        self.numbers = [pygame.sprite.Sprite(self) for _ in range(3)]
        self.x, self.y = offset
        self.value = 0

    def update(self, value):
        chars = '{0:03d}'.format(value)
        for i in range(3):
            sprite = self.numbers[i]
            sprite.image = images[f"c{chars[i]}"]
            sprite.rect = sprite.image.get_rect()
            sprite.rect.x = self.x + i * 24
            sprite.rect.y = self.y