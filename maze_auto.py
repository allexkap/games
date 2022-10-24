from os import get_terminal_size
from time import sleep
from maze import Player


def Bot(player, delay=0.1):
    current = 0
    while True:
        failed = player.move(current)
        if not failed: sleep(delay)
        current += 2*(not failed) - 1
        current %= 4

try:
    x, y = get_terminal_size()
    Bot(Player((x-10)//4, (y-5)//2, slow=True))
except KeyboardInterrupt:
    print()
