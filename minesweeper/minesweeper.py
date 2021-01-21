import random
import pygame
import re
import sys
import time
import os


class Board:
    def __init__(self, size, bombs=10):
        self.size = size
        self.bombs = bombs

        self.board = self.make_board()
        self.set_values()
        self.checked = set()

    def make_board(self):
        board = [[0 for _ in range(self.size)] for _ in range(self.size)]

        bomb_count = 0
        while bomb_count < self.bombs:
            loc = random.randint(0, self.size ** 2 - 1)
            row = loc // self.size
            col = loc % self.size

            if board[row][col] == '*':
                continue

            board[row][col] = '*'
            bomb_count += 1

        return board

    def set_values(self):
        for row in range(self.size):
            for col in range(self.size):
                if self.board[row][col] == '*':
                    continue
                self.board[row][col] = self.get_neighbors(row, col)

    def get_neighbors(self, r, c):
        num_bombs = 0
        for row in range(max(0, r - 1), min(self.size - 1, r + 1) + 1):
            for col in range(max(0, c - 1), min(self.size - 1, c + 1) + 1):
                if r == row and c == col:
                    continue
                if self.board[row][col] == '*':
                    num_bombs += 1

        return num_bombs

    def dig(self, row, col):
        self.checked.add((row, col))

        if self.board[row][col] == '*':
            return False
        elif self.board[row][col] > 0:
            return True

        for r in range(max(0, row - 1), min(self.size - 1, row + 1) + 1):
            for c in range(max(0, col - 1), min(self.size - 1, col + 1) + 1):
                if (r, c) in self.checked:
                    continue
                self.dig(r, c)

        return True

    def __str__(self):
        visible_board = [[None for _ in range(self.size)] for _ in range(self.size)]
        for row in range(self.size):
            for col in range(self.size):
                if (row, col) in self.checked:
                    visible_board[row][col] = str(self.board[row][col])
                else:
                    visible_board[row][col] = ' '

        string_rep = ''
        widths = []
        for idx in range(self.size):
            columns = map(lambda x: x[idx], visible_board)
            widths.append(
                len(
                    max(columns, key=len)
                )
            )

        # print the csv strings
        indices = [i for i in range(self.size)]
        indices_row = '   '
        cells = []
        for idx, col in enumerate(indices):
            fmt = '%-' + str(widths[idx]) + "s"
            cells.append(fmt % col)
        indices_row += '  '.join(cells)
        indices_row += '  \n'

        for i in range(len(visible_board)):
            row = visible_board[i]
            string_rep += f'{i} |'
            cells = []
            for idx, col in enumerate(row):
                fmt = '%-' + str(widths[idx]) + "s"
                cells.append(fmt % col)
            string_rep += ' |'.join(cells)
            string_rep += ' |\n'

        str_len = int(len(string_rep) / self.size)
        string_rep = indices_row + '-' * str_len + '\n' + string_rep + '-' * str_len

        return string_rep

    def __repr__(self):
        return self.board


sys.setrecursionlimit(999999)
WIDTH = HEIGHT = 600
pygame.init()
size = 20
difficulty = 6
num_bombs = (size ** 2) // (12 - difficulty)
sq_size = WIDTH // size
screen = pygame.display.set_mode((WIDTH, HEIGHT))
board = Board(size, num_bombs)
WHITE = (255, 255, 255)
GREY = (128, 128, 128)
BLACK = (0, 0, 0)
marked = set()
game_over = False
reveal = False


def get_image(path, size=(sq_size, sq_size)):
    return pygame.transform.scale(pygame.image.load(os.path.join("minesweeper", path)), (size[0], size[1]))


images = dict()
images['*'] = get_image('Minesweeper_mine.png')
images['uncovered'] = get_image('Minesweeper_uncovered.png')
images['flag'] = get_image('Minesweeper_flag.png')
for i in range(9):
    images[i] = get_image(f'Minesweeper_{i}.png')

def start_game():
    pass


def show_solution():
    for xidx, row in enumerate(board.board):
        for yidx, cell in enumerate(row):
            cell_width = WIDTH // size
            cell_height = HEIGHT // size
            screen.blit(images[cell], (xidx * cell_width, yidx * cell_height))


def write(text, x, y, color, font=pygame.font.SysFont('arial', 50)):
    words = font.render(text, 1, color)
    screen.blit(words, (x, y))


def end_game():
    global game_over
    print('....')
    game_over = True


def check_win():
    for i in range(len(board.board)):
        for j in range(len(board.board[i])):
            if (i, j) not in board.checked and board.board[i][j] != '*':
                return False
            else:
                continue
    return True


def get_events():
    global game_over
    global reveal
    safe = True
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            location = pos[0] // sq_size, pos[1] // sq_size
            if event.button == 1:
                safe = board.dig(location[0], location[1])
            if event.button == 3:
                if location in marked:
                    marked.remove(location)
                else:
                    marked.add(location)
            if not safe:
                end_game()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_over:
                reveal = True


def draw_grid(win, rows, cell_width, cell_height, padding=0):
    for i in range(rows):
        for j in range(rows):
            pygame.draw.rect(win, GREY, (i * cell_width + padding // 2, j * cell_height - padding // 2,
                                         cell_width, cell_height), 2)


def draw_text():
    for xidx, row in enumerate(board.board):
        for yidx, cell in enumerate(row):
            cell_width = WIDTH // size
            cell_height = HEIGHT // size

            if (xidx, yidx) in board.checked and not cell == 0:
                # write(str(cell), xidx * cell_width, yidx * cell_height, BLACK)
                screen.blit(images[cell], (xidx * cell_width, yidx * cell_height))
            elif (xidx, yidx) in board.checked and cell == 0:
                screen.blit(images['uncovered'], (xidx * cell_width, yidx * cell_height))
            else:
                screen.blit(images[0], (xidx * cell_width, yidx * cell_height))
            if (xidx, yidx) in marked:
                screen.blit(images['flag'], (xidx * cell_width, yidx * cell_height))


def draw():
    screen.fill(WHITE)
    draw_grid(screen, size, WIDTH // size, HEIGHT // size)
    draw_text()
    pygame.display.update()


def main():
    run = True
    while run:
        start_game()
        get_events()
        draw()
        if game_over:
            write('You Lost', 200, 300, BLACK)
            pygame.display.update()
        if reveal:
            show_solution()
            pygame.display.update()

        if check_win():
            write('You Won!!', 200, 300, BLACK)
            pygame.display.update()


if __name__ == '__main__':
    main()
