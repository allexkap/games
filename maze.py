class Player:

    offsets = ((1, -1), (0, -1), (1, 1), (0, 1))
    colors = {'b': '  ', 'w': '██', 'r': '\33[31m██\33[0m'}

    def __init__(self, n=4, m=4, slow=False):
        self.slow = slow
        self.n = n
        self.m = m
        self.pos = [1, 1]
        self.wall_cache = [[False for _ in range(self.n*2+1)] for _ in range(self.m*2+1)]
        self.euler()

        self.clear()
        self.set_pixel(-2, 2*self.m+2, color='', save=True)
        self.use_lidar()
        self.set_pixel(*self.pos, color='r')
        self.flush()


    def euler(self):
        from random import randint
        self.right = [[False for _ in range(self.n-1)] for _ in range(self.m)]
        self.under = [[False for _ in range(self.n)] for _ in range(self.m-1)]
        sides = [i for i in range(self.n)]
        c = self.n

        for i in range(self.m):
            last = not self.m-i-1
            for j in range(self.n-1):
                if sides[j] == sides[j+1] or randint(0, 1) and not last:
                    self.right[i][j] = True
                else:
                    s = sides[j+1]
                    for k in range(self.n):
                        if sides[k] == s:
                            sides[k] = sides[j]
            if last: break
            for j in range(self.n):
                if sides.count(sides[j]) > 1 and randint(0, 1):
                    self.under[i][j] = True
                    sides[j] = (c := c + 1)


    def is_wall(self, x, y):
        return not (x and y and 2*self.n-x and 2*self.m-y) or \
            (not x%2 or self.under[y//2-1][x//2]) and \
            (not y%2 or self.right[y//2][x//2-1]) and \
            (not x%2 or not y%2)


    def flush(self, restore=True):
        print('\33[u' if restore else '', end='', flush=True)


    def clear(self):
        print('\33c', end='', flush=False)


    def set_pixel(self, x, y, color='w', save=False):
        print(
            '\33[{};{}H{}{}'.format(
                y+1 + 2,
                x*2+1 + 2*2,
                Player.colors[color] if color else '',
                '\33[s' if save else ''
            ), end='', flush=False
        )


    def use_lidar(self):
        I = 0
        for i in range(9):
            x = self.pos[0]+i%3-1
            y = self.pos[1]+i//3-1
            if self.is_wall(x, y):
                if not self.wall_cache[y][x]:
                    self.wall_cache[y][x] = True
                    self.set_pixel(x, y)
                I += i%2
        return I


    def move(self, direction):
        pos = self.pos.copy()
        k, d = Player.offsets[direction]
        pos[k] += d
        if self.is_wall(*pos):
            return True

        self.set_pixel(*self.pos, color='b')
        self.set_pixel(*pos, color='r')
        self.pos = pos

        if self.use_lidar() < 2 or self.slow or self.move(direction):
            self.flush()
