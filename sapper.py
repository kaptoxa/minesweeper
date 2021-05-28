import numpy as np
from random import randint


n = 9  # size of field to play
m = 10  # count of bombs

def on_field(x, y):
    return x > -1 and x < n and y > -1 and y < n

DELTAS = [(dx, dy) for dy in range(-1, 2) for dx in range(-1, 2)]
del DELTAS[4]


class Sapper():

    def __init__(self, n, m, x=0, y=0):
        """ init data to keep info about bombs and numbers,
            and what fields are opened. x, y - lucky first turn """
        field = np.zeros((n, n), dtype=np.int8)
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

        print(field)
        opened = np.zeros((n, n), dtype=np.int8)
        self.field, self.opened, self.bombs = field, opened, bombs

    def get_pics(self):
        return np.where(self.opened == 1, self.field, self.opened)

    def get_mask(self):
        return self.opened > 0

    def get_size(self):
        return self.field.shape

    def __next_zeroes(self, i, j):
        if not self.field[i, j] and not self.opened[i, j]:
            self.opened[i, j] = 1
            self.__open_zeroes(i, j)

    def __open_zeroes(self, x, y):
        for dx, dy in DELTAS:
            i, j = x + dx, y + dy
            if on_field(i, j):
                self.__next_zeroes(i, j)
                if self.field[i, j]:
                    self.opened[i, j] = 1

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

    def auto_turn(self, x, y):
        cleared = True
        for dx, dy in DELTAS:
            i, j = x + dx, y + dy
            if on_field(i, j):
                if self.field[i, j] == 10 and self.opened[i, j] != 12:
                    cleared = False
                    break
        if cleared:
            for dx, dy in DELTAS:
                i, j = x + dx, y + dy
                if on_field(i, j):
                    if self.field[i, j] == 10:
                        self.opened[i, j] = 12
                    elif self.field[i, j]:
                        self.opened[i, j] = 1
                    else:
                        self.__open_zeroes(i, j)

    def flag(self, x, y):
        if self.opened[x, y] == 12:
            self.opened[x, y] = 0
        elif not self.opened[x, y]:
            self.opened[x, y] = 12

    def remained(self):
        return m - sum(x == 12 for x in self.opened.flat)

    def solved(self):
        easy = self.opened.copy()
        easy[easy > 10] = 0
        count = np.sum(easy)
        if count == n * n - m:
            self.opened = np.where(self.field == 10, 12, self.opened)
            return True
        else:
            return False


def create_game():
    return Sapper(n, m)