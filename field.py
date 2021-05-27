from pics import images
import pygame


class Field(pygame.sprite.Group):
    def __init__(self, offset):
        super().__init__()
        self.x, self.y = offset

    def update(self, game):
        self.empty()
        pics = game.get_pics()
        mask = game.get_mask()
        n, m = game.get_size()
        for row in range(n):
            for col in range(m):
                if mask[row, col]:
                    sprite = pygame.sprite.Sprite(self)
                    sprite.image = images[str(pics[row, col])]
                    sprite.rect = sprite.image.get_rect()
                    sprite.rect.x = 18 + 29 * col
                    sprite.rect.y = 97 + 29 * row
