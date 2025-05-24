import copy
import random
import sys
import pygame
import numpy as np

from constants import *

#Pygame SetUp
pygame.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Tic Tac toe AI")

class AI:

    def __init__(self, level = 1 , player = 2):
        self.level = level
        self.player = player

    def rnd(self, board):
        empty_sqrs = board.get_empty_sqrs()
        idx = random.randrange(0, len(empty_sqrs))

        return empty_sqrs[idx]

    def minimax(self, board,maximizing):

        #terminal case
        case = board.final_state()
        if case == 1:
            return 1 , None
        if case == 2:
            return -1, None

        elif board.isFull():
            return 0, None

        if maximizing:
            max_eval = -100
            best_move = None
            empty_sqrs = board.get_empty_sqrs()

            for row,col in empty_sqrs:
                temp_board = copy.deepcopy(board)
                temp_board.mark_square(row,col,1)
                eval = self.minimax(temp_board,False)[0]
                if eval > max_eval:
                    max_eval = eval
                    best_move = (row,col)

            return max_eval, best_move
        else:
            min_eval = 100
            best_move = None
            empty_sqrs = board.get_empty_sqrs()

            for row, col in empty_sqrs:
                temp_board = copy.deepcopy(board)
                temp_board.mark_square(row, col, self.player)
                eval = self.minimax(temp_board, True)[0]
                if eval < min_eval:
                    min_eval = eval
                    best_move = (row, col)

            return min_eval, best_move


    def eval(self, main_board):
        move = ()
        eval = None
        if self.level == 0:
            # random choice
            eval = 'random'
            move = self.rnd(main_board)
        else:
            # minimax algorithm
            eval ,move = self.minimax(main_board, False)

        print(f'Ai has chosen {move} with and eval of {eval}')
        return move

class Board:
    def __init__(self):
        self.squares = np.zeros((ROWS,COlS))
        self.empty_sqrs = self.squares
        self.marked_sqrs = 0

    def final_state(self, show = False):
        # return 1 if player 1
        # return 2 if player 2
        # return 0 if no win yet
        for i in range(3):
            #col check
            if self.squares[0][i] == self.squares[1][i] == self.squares[2][i] != 0:
                if show:
                    color = CIRC_COLOR if self.squares[0][i] == 2 else CROSS_COLOR
                    iPos = (i * SQSIZE + SQSIZE // 2, 20)
                    fPos = (i * SQSIZE + SQSIZE // 2, HEIGHT - 20)
                    pygame.draw.line(screen, color ,iPos,fPos , LINE_WIDTH)
                return self.squares[0][i]
            #row check
            if self.squares[i][0] == self.squares[i][1] == self.squares[i][2] != 0:
                if show:
                    color = CIRC_COLOR if self.squares[i][0] == 2 else CROSS_COLOR
                    iPos = (20, i * SQSIZE + SQSIZE // 2)
                    fPos = (WIDTH - 20, i * SQSIZE + SQSIZE // 2)
                    pygame.draw.line(screen, color ,iPos,fPos , LINE_WIDTH)
                return self.squares[i][0]

        #diagonal Check
        if self.squares[0][0] == self.squares[1][1] == self.squares[2][2] != 0:
            if show:
                color = CIRC_COLOR if self.squares[0][0] == 2 else CROSS_COLOR
                iPos = (20,20)
                fPos = (WIDTH - 20, HEIGHT - 20)
                pygame.draw.line(screen, color, iPos, fPos, CROSS_WIDTH)
            return self.squares[0][0]
        if self.squares[0][2] == self.squares[1][1] == self.squares[2][0] != 0:
            if show:
                color = CIRC_COLOR if self.squares[0][2] == 2 else CROSS_COLOR
                iPos = (20, HEIGHT - 20)
                fPos = (WIDTH - 20, 20)
                pygame.draw.line(screen, color, iPos, fPos, CROSS_WIDTH)
            return self.squares[0][2]

        return 0

    def mark_square(self, row, col, player):
        self.squares[row][col] = player
        self.marked_sqrs += 1

    def get_empty_sqrs(self):
        empty_sqrs = []
        for row in range(ROWS):
            for col in range(COlS):
                if self.isCondition(row, col):
                    empty_sqrs.append((row, col))
        return empty_sqrs

    def isCondition(self,row,col):
        return self.squares[row][col] == 0

    def isFull(self):
        return self.marked_sqrs == 9

    def isEmpty(self):
        return  self.marked_sqrs == 0


class Game:
    def __init__(self):
        self.board = Board()
        self.player = 1
        self.ai = AI()
        self.game_mode = "ai" # AI
        self.running = True
        self.show_lines()

    def show_lines(self):
        screen.fill(BG_COLOR)
        #vertical line
        pygame.draw.line(screen,LINE_COLOR,(SQSIZE,0),(SQSIZE,HEIGHT),LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (WIDTH - SQSIZE, 0), (WIDTH - SQSIZE, HEIGHT), LINE_WIDTH)
        #Horizontal Line
        pygame.draw.line(screen, LINE_COLOR, (0, SQSIZE), (HEIGHT,SQSIZE), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (0, HEIGHT - SQSIZE), (HEIGHT, HEIGHT - SQSIZE), LINE_WIDTH)

    def draw_fig(self,row,col):
        if self.player == 1:
            #draw cross
            # descending line
            start_desc = (col * SQSIZE + OFFSET, row * SQSIZE + OFFSET)
            end_desc = (col * SQSIZE + SQSIZE - OFFSET, row * SQSIZE + SQSIZE - OFFSET)
            pygame.draw.line(screen,CROSS_COLOR, start_desc , end_desc ,CROSS_WIDTH)
            # ascending line
            start_asc = (col * SQSIZE + OFFSET, row * SQSIZE + SQSIZE - OFFSET)
            end_asc = (col * SQSIZE + SQSIZE - OFFSET, row * SQSIZE + OFFSET)
            pygame.draw.line(screen,CROSS_COLOR, start_asc , end_asc ,CROSS_WIDTH)


        elif self.player == 2:
            #draw circle
            center = (col * SQSIZE + SQSIZE // 2, row * SQSIZE + SQSIZE // 2)
            pygame.draw.circle(screen, CIRC_COLOR ,center, RADIUS , CIRC_WIDTH)

    def changeTurn(self):
        self.player = self.player % 2 + 1

    def change_game_mode(self):
        self.game_mode = 'ai' if self.game_mode == 'pvp' else 'pvp'
    def reset(self):
        self.__init__()

    def isOver(self):
        return self.board.final_state(show=True) != 0 or self.board.isFull()

def main():

    #object
    game = Game()
    board = game.board
    ai = game.ai
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                row = pos[1] // SQSIZE
                col = pos[0] // SQSIZE
                if board.isCondition(row,col) and game.running:
                    board.mark_square(row,col,game.player)
                    game.draw_fig(row,col)
                    game.changeTurn()
                    if game.isOver():
                        game.running = False

            elif event.type == pygame.KEYDOWN:
                #reset game
                if event.key == pygame.K_r:
                    game.reset()
                    board = game.board
                    ai = game.ai
                # g - change game mode
                if event.key == pygame.K_g:
                    game.change_game_mode()
                #change level of ai
                if event.key == pygame.K_0:
                    ai.level = 0
                if event.key == pygame.K_1:
                    ai.level = 1

        if game.game_mode == 'ai' and game.player == ai.player and game.running:
            pygame.display.update()

            #ai method
            row , col = ai.eval(board)
            if board.isCondition(row, col):
                board.mark_square(row, col, game.player)
                game.draw_fig(row, col)
                game.changeTurn()
                if game.isOver():
                    game.running = False

        pygame.display.update()



main()