import sys
import time
import pygame
from pygame.color import THECOLORS as COLORS
from backend import print_matrix, give_me_a_game, check
from rumpy import RumClient
from config import *

# size
B = BLOCK = 70  # 每个单位是80，总宽是9个单位
C = CORNER = 3  # 每个单位是4


class SudokuGUI(RumClient):
    def init(self, name=None):
        self.name = name or USERNAME
        self.is_post_to_rum = True  # 是否发布到 rum
        self.running = True  # 是否继续游戏
        self.blank_number = 25  # 难度 # int(sys.argv[1])
        self.cur_blank_number = self.blank_number
        self.group_id = GROUP_ID

    def loop(self):
        # init pygame
        pygame.init()

        # contant
        SIZE = [9 * B, 10 * B]
        self.font60 = pygame.font.SysFont("Times", 42)  # 80
        self.font80 = pygame.font.SysFont("Times", 54)  # 80

        # create screen
        self.screen = pygame.display.set_mode(SIZE)

        # variable parameter
        self.cur_i, self.cur_j = 0, 0
        self.cur_change_number = 0

        # matrix abount
        MATRIX_ANSWER, MATRIX, BLANK_IJ = give_me_a_game(blank_size=self.blank_number)
        print(BLANK_IJ)
        print_matrix(MATRIX)
        note = f"题目:\n{print_matrix(MATRIX)}\n"

        # main loop
        starttime = time.time()
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    break
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.cur_j, self.cur_i = int(event.pos[0] / B), int(
                        event.pos[1] / B
                    )
                elif event.type == pygame.KEYUP:

                    if (
                        chr(event.key) in ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
                        and (self.cur_i, self.cur_j) in BLANK_IJ
                    ):
                        MATRIX[self.cur_i][self.cur_j] = int(chr(event.key))
                        self.cur_blank_number = sum(
                            [
                                1 if col == 0 or col == "0" else 0
                                for row in MATRIX
                                for col in row
                            ]
                        )
                        self.cur_change_number += 1
            # background
            self.draw_background()
            # choose item
            self.draw_choose()
            # numbers
            self.draw_number(MATRIX, BLANK_IJ)
            # point
            self.curl_time = time.time() - starttime
            self.draw_context()
            # flip
            pygame.display.flip()

            # check win or not
            if self.check_win(MATRIX_ANSWER, MATRIX):
                print("You win, smarty ass!!!", f"takes {int(self.curl_time)} seconds.")
                break

        note = (
            f"{self.name} 难度 {self.blank_number}\n通关！用时 {int(self.curl_time)} 秒\n"
            + note
        )
        if self.is_post_to_rum:
            # post result to rum
            self.group.send_note(content=note)

        pygame.quit()

    def draw_background(self):
        self.screen.fill(COLORS["white"])
        boards = [
            (0, 0, 3 * B, 9 * B),
            (3 * B, 0, 3 * B, 9 * B),
            (6 * B, 0, 3 * B, 9 * B),
            (0, 0, 9 * B, 3 * B),
            (0, 3 * B, 9 * B, 3 * B),
            (0, 6 * B, 9 * B, 3 * B),
        ]
        for board in boards:
            pygame.draw.rect(self.screen, COLORS["black"], board, C)

    def draw_choose(self):
        pygame.draw.rect(
            self.screen,
            COLORS["blue"],
            (self.cur_j * B + C, self.cur_i * B + C, B - 2 * C, B - 2 * C),
            0,
        )

    def check_win(self, matrix_all, matrix):
        if matrix_all == matrix:
            return True
        return False

    def check_color(self, matrix, i, j):
        _matrix = [[col for col in row] for row in matrix]
        _matrix[i][j] = 0
        if check(_matrix, i, j, matrix[i][j]):
            return COLORS["green"]
        return COLORS["red"]

    def draw_number(self, matrix, blank_lj):
        for i in range(len(matrix)):
            for j in range(len(matrix[0])):
                _color = (
                    self.check_color(matrix, i, j)
                    if (i, j) in blank_lj
                    else COLORS["gray"]
                )
                txt = self.font80.render(
                    str(matrix[i][j] if matrix[i][j] not in [0, "0"] else ""),
                    True,
                    _color,
                )
                x, y = j * B + 6 * C, i * B + 2 * C
                self.screen.blit(txt, (x, y))

    def draw_context(self):
        txt = self.font60.render(
            "Blank:"
            + str(self.cur_blank_number)
            + " Done:"
            + str(self.cur_change_number)
            + f" Time:{int(self.curl_time)} s",
            True,
            COLORS["black"],
        )
        x, y = 2 * C, 9 * B
        self.screen.blit(txt, (x, y))


if __name__ == "__main__":
    game = SudokuGUI()
    game.init()
    game.loop()
