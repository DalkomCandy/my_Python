import pygame
import random
import numpy as np
from enum import Enum
from constants import CP, TEST_GRID
from pygame.locals import *     
            
N = 4

class game_2048:
    def __init__(self, w=300, h=330):
        self.grid = np.zeros((N,N), dtype=int)
        self.w = w
        self.h = h
        self.SPACING = 4
        self.border = h // 10
        self.score = 0
        
        pygame.init()
        pygame.display.set_caption('2048')
        self.clock = pygame.time.Clock()
        
        pygame.font.init()
        self.font = pygame.font.SysFont('arial', 25)
        
        self.display = pygame.display.set_mode((self.w, self.h))
        
    def __str__(self):
        return str(self.grid)
    
    def _place_num(self, k=1):
        random_positon = list(zip(*np.where(self.grid == 0)))
        
        for pos in random.sample(random_positon, k=k):
            if random.random() < .1:
                self.grid[pos] = 4 # 10%의 확률로 4 등장
            else:
                self.grid[pos] = 2 # 나머지 90% 확률로 2 등장
            print(self.grid)
    
  
    def _get_nums(self, move_result):
        move_result_n = move_result[move_result != 0]
        move_result_n_sum = []
        skip = False
        
        for j in range(len(move_result_n)):
            if skip:
                skip = False
                continue
            if j != len(move_result_n) - 1 and move_result_n[j] == move_result_n[j + 1]:
                new_move_result_n = move_result_n[j] * 2 # 블록이 합쳐짐
                self.score += 1
                skip = True
            else:
                new_move_result_n = move_result_n[j]
            move_result_n_sum.append(new_move_result_n)
        return np.array(move_result_n_sum)
                     
            
    def make_move(self, move):
        for i in range(N):
            if move in 'lr':
                move_result = self.grid[i, :] # 왼쪽 or 오른쪽이면 행으로 움직임
            else:
                move_result = self.grid[:, i] # 왼쪽 or 오른쪽이 아니면 열로 움직임
                
            flipped = False
            if move in 'rd':
                flipped = True
                move_result = move_result[::-1]
            
            move_result_n = self._get_nums(move_result)
            
            new_move_result = np.zeros_like(move_result) # 움직이기 전에 양수가 들어있던 블록으로 0으로
            new_move_result[:len(move_result_n)] = move_result_n # 새로운 움직임 후에 양수였던 값들을 이동함
            
            if flipped:
                new_move_result = new_move_result[::-1]

            if move in 'lr':
                self.grid[i, :] = new_move_result
            else:
                self.grid[:, i] = new_move_result
                
    grid = TEST_GRID

    def draw_game(self):
        self.display.fill(CP['back'])
        
        for i in range(N):
            for j in range(N):
                n = self.grid[i][j]
                
                rect_x = j*(self.w) // N + self.SPACING
                rect_y = i*(self.h) // N + self.SPACING
                rect_w = (self.w) // N - 2*self.SPACING
                rect_h = (self.h) // N - 2*self.SPACING
                print(rect_x,rect_y,rect_h,rect_w)
                
                pygame.draw.rect(self.display,
                                CP[n],
                                pygame.Rect(rect_x, rect_y, rect_w, rect_h),
                                #border_radius=0
                                )
                text = self.font.render(f'Score : {self.score}', True, 'black')
                self.display.blit(text, [0,0])
                pygame.display.flip()

                if n == 0:
                    n = ''
                text_surface = self.font.render(f'{n}', True, 'black')
                text_rect = text_surface.get_rect(center=(rect_x + rect_w /2,
                                                          rect_y + rect_h / 2))
                self.display.blit(text_surface, text_rect)
                
    @staticmethod         
    def press_key():
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    return 'q'
                if event.type == pygame.KEYDOWN:
                    if event.key == K_UP:
                        return 'u'
                    elif event.key == K_DOWN:
                        return 'd'
                    elif event.key == K_RIGHT:
                        return 'r'
                    elif event.key == K_LEFT:
                        return 'l'
                    elif event.key == K_q or event.key == K_ESCAPE:
                        return 'q'
                    
    def game_over(self):
        grid_bu = self.grid.copy()
        for move in 'lrud':
            self.make_move(move)
            if not all((self.grid == grid_bu).flatten()):
                self.grid = grid_bu
                return False
        return True
                    
    def play(self):
        self._place_num(k=2)
        while True:
            self.draw_game()
            pygame.display.flip()
            cmd = self.press_key()
            if cmd == 'q':
                break
            old_grid = self.grid.copy() # 아무것도 움직이지않을 때 키를 누르면 블록이 나오지 않아야함
            self.make_move(cmd)
            if self.game_over():
                print('Game Over!')
                break

            if not all((self.grid == old_grid).flatten()):
                self._place_num()
            
                
        
if __name__ == '__main__':
    game = game_2048()
    game.play()