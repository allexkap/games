from maze import Player
from getkey import getkey, keys
DIRS = {keys.UP: 0, keys.LEFT: 1, keys.DOWN: 2, keys.RIGHT: 3}

player = Player()
try:
    while True:
        if (k := getkey()) in DIRS:
            player.move(DIRS[k])
except KeyboardInterrupt:
    print()
