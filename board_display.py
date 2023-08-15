import pygame
from pygame.locals import *

class Board():
    def __init__(self,board_len):
        self.len = board_len
        pygame.init()
        self.clock = pygame.time.Clock()
        self.board_width = self.len * 50 + 100
        self.board_height = self.len * 50 + 100
        self.grid_size = 50                            #棋子大小
        # 设置窗口大小
        self.screen = pygame.display.set_mode((self.board_width, self.board_height),pygame.RESIZABLE)
        pygame.display.set_caption('超级无敌牛逼帅')
        # 设置背景色为白色
        self.screen.fill((205,201,201))
        # print(type(screen))
        pygame.draw.rect(self.screen, (205,149,12), (50,50,9*50,9*50), 0)
        # 设置矩形颜色为棕色
        rect_color = (0,0,0)
        # 循环画棋盘线
        for i in range(75, self.board_width - 75, self.grid_size):
            for j in range(75, self.board_height - 75, self.grid_size):
                pygame.draw.rect(self.screen, rect_color, (i, j, self.grid_size, self.grid_size), 1)
        pygame.display.update()        
        
        
    def new_game(self):
        self.screen.fill((205,201,201))
        pygame.draw.rect(self.screen, (205,149,12), (50,50,15*50,15*50), 0)
        for i in range(75, self.board_width - 75, self.grid_size):
            for j in range(75, self.board_height - 75, self.grid_size):
                pygame.draw.rect(self.screen, (0,0,0), (i, j, self.grid_size, self.grid_size), 1)
        pygame.display.update()        
        
    
    #刷新界面
    def update(self):
            pygame.display.update()
            
    def quit(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()


            
    def update_(self):
        while True:
            self.clock.tick(60)
            self.clear()
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
        
        
    #画棋子
    def draw_circle(self,pos,player):
        if player == 0:
            color = (0,0,0)
        else:
            color = (255,255,255)
        pygame.draw.circle(self.screen, color, pos, 25, width=0)
        # self.update()
        pass
    
    def clear(delf):
        pygame.event.clear()
        pass
    

    def get_click(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    a,b = event.pos
                    return a,b
        pass
    


    def change_pos(self,x,y):
        if (x % 50 <25):
            x = int(x / 50)
        else:
            x = int(x / 50 ) + 1
        if (y % 50 <25):
            y = int(y / 50)
        else:
            y = int(y / 50 ) + 1
        return x,y
