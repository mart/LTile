import numpy as np
from PIL import Image


class LTile:
    """An instance of the L-tile problem
    Requires that n is a power of 2
    Finds a placement of L-shaped tiles on an n by n grid with one tile missing, renders a gif
    """
    def __init__(self, n, missing, gif_step=1, gif_speed=30):
        self.counter = 0
        self.tiles = [[0 for y in range(n)] for x in range(n)]
        self.missing = missing
        self.colors = [tuple(np.random.choice(range(256), size=3)) for _ in range(len(self.tiles) ** 2 // 3 + 1)]
        self.colors[0] = (0, 0, 0)
        self.images = []
        self.gif_step = gif_step
        self.size = n
        self.gif_speed = gif_speed

    def solve(self):
        self.fill(self.missing, (0, 0), (self.size, self.size))

    def create_gif(self):
        self.images[0].save('animation' + str(self.size) + '.gif',
                            save_all=True,
                            append_images=self.images[1:],
                            duration=self.gif_speed,
                            loop=0)

    def fill(self, reserved, up_left, low_right):
        side_length = low_right[0] - up_left[0] + 1
        if side_length == 2:
            self.place_tile(reserved, up_left[0], up_left[1])
        else:
            half = side_length // 2
            # define the 4 boards as tuple(upper left, lower right, center corner) - all coordinate tuples are (x, y)
            boards = [
                ((up_left[0], up_left[1]),               (up_left[0] + half - 1, up_left[1] + half - 1),         (up_left[0] + half - 1, up_left[1] + half - 1)),
                ((up_left[0], up_left[1] + half),        (up_left[0] + half - 1, up_left[1] + half * 2 - 1),     (up_left[0] + half - 1, up_left[1] + half)),
                ((up_left[0] + half, up_left[1]),        (up_left[0] + half * 2 - 1, up_left[1] + half - 1),     (up_left[0] + half, up_left[1] + half - 1)),
                ((up_left[0] + half, up_left[1] + half), (up_left[0] + half * 2 - 1, up_left[1] + half * 2 - 1), (up_left[0] + half, up_left[1] + half))
            ]
            for board in boards:
                # test if reserved tile is in this board
                if board[0][0] <= reserved[0] <= board[1][0] and board[0][1] <= reserved[1] <= board[1][1]:
                    # place tile to occupy one space in each of the 3 other boards
                    self.place_tile(board[2], up_left[0] + half - 1, up_left[1] + half - 1)
                    self.fill(reserved, board[0], board[1])
                else:
                    self.fill(board[2], board[0], board[1])

    def place_tile(self, reserved, x, y):
        self.counter += 1
        for i in range(x, x + 2):
            for k in range(y, y + 2):
                if reserved[0] == i and reserved[1] == k:
                    continue
                else:
                    self.tiles[i][k] = self.counter
        if self.counter % self.gif_step == 0:
            self.images.append(self.render())

    def render(self):
        n = len(self.tiles)
        im = Image.new('RGB', (n, n), 'white')
        pixels = im.load()
        for x in range(n):
            for y in range(n):
                pixels[x, y] = self.colors[self.tiles[x][y]]
        waldo = Image.open('waldo.jpg').resize((20, 20))
        im = im.resize((n * 20, n * 20))
        im.paste(waldo,
                 (self.missing[0] * 20, self.missing[1] * 20, self.missing[0] * 20 + 20, self.missing[1] * 20 + 20))
        return im


# careful with this, the gif filesizes can explode
n = 2 ** 3
tile = LTile(n, tuple(np.random.choice(range(n), size=2)), gif_speed=300)
tile.solve()
tile.create_gif()
n *= 2
tile = LTile(n, tuple(np.random.choice(range(n), size=2)), gif_speed=100)
tile.solve()
tile.create_gif()
n *= 2
tile = LTile(n, tuple(np.random.choice(range(n), size=2)))
tile.solve()
tile.create_gif()