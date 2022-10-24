from os import get_terminal_size
from time import sleep
from maze import Player


def Bot(player, delay=0.1):
    DIRS = ('up', 'left', 'down', 'right')
    ANGLES = (1, -1, -1, -1)
    failed = 0
    current = 0
    while True:
        if player.move(DIRS[current]):
            failed += 1
        else:
            failed = 0
            sleep(delay)
        current = (current+ANGLES[failed])%4

x, y = get_terminal_size()
player = Player((x-10)//4, (y-5)//2, slow=1)

try:
    Bot(player)
except:
    print()

