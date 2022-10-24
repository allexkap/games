from maze import Player
from getkey import getkey, keys
DIRS = {keys.UP : 'up', keys.DOWN : 'down', keys.LEFT : 'left', keys.RIGHT : 'right'}

player = Player()
try:
    while True:
        if (k := getkey()) in DIRS:
            player.move(DIRS[k])
except KeyboardInterrupt:
    print()
