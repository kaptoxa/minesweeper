from pics import images
from sapper import on_field, create_game
import status
import counter
import field

import pygame


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Minesweeper')
    screen = pygame.display.set_mode((298, 377))
    clock = pygame.time.Clock()
    game = create_game()

    # prepare sprites groups
    field = field.Field((18, 98))
    bombs_counter = counter.RedCounter((26, 27))
    bombs_counter.update(10)
    secs_counter = counter.RedCounter((200, 27))
    statuses = pygame.sprite.Group()
    status = status.Status(statuses, (126, 27))


    # game loop
    fin = False
    clamped = set()
    while not fin:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                fin = True
                break
            if event.type == pygame.MOUSEBUTTONDOWN:
                clamped.add(event.button)
            if event.type == pygame.MOUSEBUTTONUP:
                x, y = event.pos
                if x > 126 and x < 173 and y > 26 and y < 73:
                    if status.finished():
                        status.start()
                        game = create_game()

                i = (x - 18) // 30
                j = (y - 98) // 30
                if on_field(i, j):
                    if clamped == {1, 3}:
                        game.auto_turn(j, i)
                    if clamped == {1}:
                        if game.turn(j, i) == 2:
                            status.lose()
                    if clamped == {3}:
                        game.flag(j, i)
                clamped.clear()
        if fin:
            break

        if game.solved():
            status.win()

        # update states of entities
        field.update(game)
        bombs_counter.update(game.remained())
        if not status.finished():
            secs_counter.update(status.duration())

        # draw field, counters and status
        screen.blit(images['background'], (0, 0))
        field.draw(screen)
        bombs_counter.draw(screen)
        secs_counter.draw(screen)
        statuses.draw(screen)
        pygame.display.flip()
        clock.tick(10)