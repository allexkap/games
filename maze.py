class Player:

    colors = {'b': '  ', 'w': '██', 'r': '\33[1;31m██\33[0m'}

    def __init__(self, n=4, m=4):
        self.n = n
        self.m = m
        self.pos = [1, 1]
        self.wall_cache = [[False for _ in range(self.n*2+1)] for _ in range(self.m*2+1)]

        self.euler()
        self.clear()
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


    def flush(self):
        print(end='', flush=True)


    def clear(self):
        print('\33c', end='', flush=False)


    def set_pixel(self, x, y, color='w'):
        print(
            '\33[{};{}H{}\33[u'.format(
                y+1 + 2,
                x*2+1 + 2*2,
                Player.colors[color],
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


    def move(self, key):
        x, y = self.pos
        if key == 'up' and not self.is_wall(x, y-1):
            self.pos[1] -= 1
        elif key == 'down' and not self.is_wall(x, y+1):
            self.pos[1] += 1
        elif key == 'left' and not self.is_wall(x-1, y):
            self.pos[0] -= 1
        elif key == 'right' and not self.is_wall(x+1, y):
            self.pos[0] += 1
        else:
            return True

        self.set_pixel(x, y, color='b')
        self.set_pixel(*self.pos, color='r')
        if self.use_lidar() < 2 or self.move(key):
            self.flush()
