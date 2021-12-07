import pygame
from pygame.locals import *
from pygame.color import Color
from itertools import product
import numpy as np


class Board:
    DIM = 8
    moveLog = []

    def __init__(self, game):
        self.screen = game.screen
        self.game = game

        self.img = dict()
        self.load_images()

        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
        ]

        self.whiteToMove = True

        self.isMoving = False
        self.movingPiece = ""

    def load_images(self):
        pieces = ["B", "K", "N", "p", 'Q', 'R']
        color = ['b', 'w']
        pieces_color = product(color, pieces)
        for color, piece in list(pieces_color):
            self.img[color + piece] = pygame.image.load(f"img/{color + piece}.png")

    def draw(self):
        size = self.game.WIDTH // self.DIM
        colors = [Color('white'), Color('gray')]
        for i in range(self.DIM):
            for j in range(self.DIM):
                color = colors[(i + j) % 2]
                pygame.draw.rect(self.screen, color, (j * size, i * size, size, size))

        self.draw_pieces()

    def draw_pieces(self):
        size = self.game.WIDTH // self.DIM
        for i in range(self.DIM):
            for j in range(self.DIM):
                piece = self.board[i][j]
                if piece != "--":
                    self.screen.blit(self.img[piece], pygame.rect.Rect(j * size, i * size, size, size))

    def move(self):
        size = self.game.WIDTH // self.DIM
        mouse_pos = np.array(pygame.mouse.get_pos(), dtype=np.int32)//size
        btn_pressed = pygame.mouse.get_pressed()[0]
        r, c = mouse_pos
        if btn_pressed:
            piece = self.board[c][r]
            pygame.mouse.set_cursor(SYSTEM_CURSOR_HAND)
            if piece != "--" and not self.isMoving:
                self.movingPiece = [self.img[piece], piece]
                self.isMoving = True
                self.board[c][r] = "--"
                Board.moveLog.append((piece, c, r))

            if self.isMoving:
                self.screen.blit(self.movingPiece[0], pygame.Rect(r*size, c*size, size, size))
        else:
            pygame.mouse.set_cursor(SYSTEM_CURSOR_ARROW)
            if self.isMoving:
                self.board[c][r] = self.movingPiece[1]
                Board.moveLog.append((self.movingPiece[1], c, r))
            self.isMoving = False
            self.movingPiece = ""

    def update(self):
        self.draw()
        self.move()


class Game:
    WIDTH = 512
    HEIGHT = 512

    def __init__(self):
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.scene = []
        self.awake()

    def awake(self):
        self.scene.append(Board(self))

    def display_update(self):
        self.screen.fill(color=Color(0xff, 0xff, 0xff))
        for gameObj in self.scene:
            gameObj.update()
        pygame.display.update()

    def update(self):
        run = True
        while run:
            for ev in pygame.event.get():
                if ev.type == QUIT:
                    run = False
                if ev.type == KEYDOWN:
                    if ev.key == K_z and pygame.key.get_mods() & K_LCTRL:
                        board = self.scene[0]
                        if board.moveLog:
                            piece, c, r = board.moveLog[-2]
                            _, cN, rN = board.moveLog[-1]
                            board.moveLog.pop()
                            board.moveLog.pop()
                            board.board[c][r] = piece
                            board.board[cN][rN] = "--"

            self.display_update()

        pygame.quit()
        exit(0)


if __name__ == "__main__":
    g = Game()
    g.update()
