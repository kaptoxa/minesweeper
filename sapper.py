import numpy as np
from random import randint

n = 8  # size of field to play
m = 10  # count of bombs


class Sapper():

    def __init__(self, n, m, x=0, y=0):
        """ init data to keep info about bombs and numbers,
            and what fields are opened. x, y - lucky first turn """
        field = np.zeros((n, n), dtype=np.int8)
        opened = np.copy(field)
        bombs = set()

        while len(bombs) < m:
            i = randint(0, n - 1)
            j = randint(0, n - 1)
            if abs(x - i) > 0 and abs(y - j) > 0:
                bombs.add((i, j))

        for i, j in bombs:
            xl, xr = [i - 1, i + 2] if i > 0 else [0, i + 2]
            yl, yr = [j - 1, j + 2] if j > 0 else [0, j + 2]
            field[xl: xr, yl: yr] += 1

        for i, j in bombs:
            field[i, j] = 10

        np.where(field == 0, 9, field)

        self.field, self.opened, self.bombs = field, opened, bombs
#        self.turn(x, y)

    def get(self):
        return self.field * self.opened

    def show(self):
        pics = ' 123456789x?F'
        for i in range(n):
            for j in range(n):
                c = self.field[i, j]
                if self.opened[i][j] == 1:
                    print('[' + pics[c] + ']' if c else '   ', end='')
                elif self.opened[i][j] > 1:
                    c = self.opened[i, j]
                    print('[' + pics[c] + ']', end='')
                else:
                    print('[' + pics[c] + ']' if c > 10 else '[ ]', end='')
            print()

    def __next_zeroes(self, i, j):
        if not self.field[i, j] and not self.opened[i, j]:
            self.opened[i, j] = 1
            self.__open_zeroes(i, j)

    def __open_zeroes(self, x, y):
        for d in [-1, 1]:
            i, j = x + d, y
            if i in range(0, n):
                self.__next_zeroes(i, j)

        for d in [-1, 1]:
            i, j = x, y + d
            if j in range(0, n):
                self.__next_zeroes(i, j)

        xl, xr = [x - 1, x + 2] if x > 0 else [0, x + 2]
        xr = n if xr > n else xr
        yl, yr = [y - 1, y + 2] if y > 0 else [0, y + 2]
        if yr > n:
            yr = n
        for i in range(xl, xr):
            for j in range(yl, yr):
                if self.field[i, j] and not (i, j) == (x, y):
                    self.opened[i, j] = 1
        # self.opened[xl: xr, yl: yr] *= self.field[xl: xr, yl: yr]

    def turn(self, x, y):
        if self.opened[x, y] > 1:
            self.opened[x, y] = 0
            return 0
        else:
            self.opened[x, y] = 1

        if (x, y) in self.bombs:
            return 2

        if not self.field[x, y]:
            self.__open_zeroes(x, y)

        return 0

    def flag(self, x, y):
        if not self.opened[x, y]:
            self.opened[x, y] = 12

    def mark(self, x, y):
        if not self.opened[x, y]:
            self.opened[x, y] = 11

    def fin(self):
        easy = self.opened.copy()
        easy[easy > 10] = 0
        count = np.sum(easy)
        return count == n * n - m


rules = """
t x y - to open (x, y) cell
f x y - to flag (x, y) cell
q x y - to set ? in (x, y) cell
"""
print(rules)
for i in range(n):
    print('[ ]' * n)


# def parse_turn():
#     correct = False
#     while not correct:
#         line = input().split()
#
#         if len(line) == 3:
#             c, x, y = line
#             if x.isdigit() and y.isdigit():
#                 x, y = int(x) - 1, int(y) - 1
#                 correct = (0 <= x < n and 0 <= y < n)
#
#         if not correct:
#             print('Not correct turn! Please, try one more time:')
#
#     return c, x, y


# c, y, x = parse_turn()
game = Sapper(n, m)

# while True:
#     game.show()
#
#     c, y, x = parse_turn()
#     if c == 't':
#         if game.turn(x, y) == 2:
#             game.show()
#             print('Game over!')
#             break
#
#     if c == 'f':
#         game.flag(x, y)
#     if c == 'q':
#         game.mark(x, y)
#
#     if game.fin():
#         print('You are winner!')
#         break
