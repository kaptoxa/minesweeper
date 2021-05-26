import os
import pygame
import sapper


images = {}
def load_images():

    names = os.listdir('pics')
    for name in names:
        filename = os.path.join('pics', name)
        if not os.path.isfile(filename):
            print(f"Нет файла {filename}!")
            return
        image = pygame.image.load(filename)
        print(f'{filename} loaded.')
        key, *other = name.split('.')
        images[key] = image


class Tile(pygame.sprite.Sprite):
    def __init__(self, row, col, value):
        super().__init__(tiles)
        self.image = images[str(value)]
#        self.add(tiles)
        self.rect = self.image.get_rect().move(18 + 30 * col, 97 + 30 * row)


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Minesweeper')
    screen = pygame.display.set_mode((298, 377))
    clock = pygame.time.Clock()
    tiles = pygame.sprite.Group()

    load_images()

    fin = False
    while not fin:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                fin = True
                break
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if event.button == 1:
                    x -= 18
                    y -= 98
                    i = x // 30
                    j = y // 30
                    print(x, y, ':', i, j)

                    sapper.game.turn(j, i)
                    tiles.empty()
                    field = sapper.game.get()
                    for row in range(sapper.n):
                        for col in range(sapper.n):
                            if field[row, col]:
                                Tile(row, col, field[row, col])

#                    sapper.game.show()

        if fin:
            break
        screen.blit(images['background'], (0, 0))
        tiles.draw(screen)
        pygame.display.flip()
        clock.tick(10)

