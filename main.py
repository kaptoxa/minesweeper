from pics import images
from status import Status
from sapper import on_field, create_game, n
from counter import RedCounter

import pygame


class Tile(pygame.sprite.Sprite):
    def __init__(self, row, col, value):
        super().__init__(tiles)
        self.image = images[str(value)]
        self.rect = self.image.get_rect()
        self.rect.x = 18 + 29 * col
        self.rect.y = 97 + 29 * row


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Minesweeper')
    screen = pygame.display.set_mode((298, 377))
    clock = pygame.time.Clock()

    tiles = pygame.sprite.Group()
    statuses = pygame.sprite.Group()
    bombs_counter = RedCounter((26, 27))
    bombs_counter.update(10)
    secs_counter = RedCounter((200, 27))


    game = create_game()
    status = Status(statuses, (126, 27))
    fin = False
    while not fin:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                fin = True
                break
            if event.type == pygame.MOUSEBUTTONUP:
                x, y = event.pos
                if x > 126 and x < 173 and y > 26 and y < 73:
                    if status.finished():
                        status.start()
                        game = create_game()

                i = (x - 18) // 30
                j = (y - 98) // 30
                if on_field(i, j):
                    if event.button == 1:
                        if game.turn(j, i) == 2:
                            status.lose()
                    if event.button == 3:
                        game.flag(j, i)
        if fin:
            break

        if game.solved():
            status.win()

        tiles.empty()
        pics = game.get_pics()
        mask = game.get_mask()
        for row in range(n):
            for col in range(n):
                if mask[row, col]:
                    Tile(row, col, pics[row, col])
        bombs_counter.update(game.remained())
        if not status.finished():
            secs_counter.update(status.duration())

        screen.blit(images['background'], (0, 0))
        tiles.draw(screen)
        bombs_counter.draw(screen)
        secs_counter.draw(screen)
        statuses.draw(screen)
        pygame.display.flip()
        clock.tick(10)