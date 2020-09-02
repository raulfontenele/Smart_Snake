import pygame,random
from pygame.locals import *
from Snake import Snake
import numpy as np

class Scene():
    def __init__(self,x_len,y_len):
        self.x_len = x_len
        self.y_len = y_len

        pygame.init()
        pygame.display.set_caption('Snake')
        self.screen = pygame.display.set_mode((x_len,y_len))

        self.wall = self.InitWall()
        self.wall_surface = pygame.Surface((10,10))
        self.wall_surface.fill((230,230,230)) 

        self.apple = pygame.Surface((10,10))
        self.apple.fill((255,0,0))
        self.apple_coord = self.AppleRandom()

        self.score = 0
        self.fitness = 0

        self.max_steps = self.x_len + self.y_len

    def InitWall(self):
        wall = []
        for x in range(int((self.x_len)/10)):
            for y in range(int((self.y_len)/10)):
                if x == 0 or x == (self.x_len)/10 - 1 or y==0 or y == (self.y_len)/10 - 1:
                    wall.append((x*10,y*10))
        return wall

    def UpdateScreen(self,snake):
        self.screen.fill((0,0,0))
        self.screen.blit(self.apple,self.apple_coord)
        for pos in snake.coord:
            self.screen.blit(snake.surface,pos)
        for pos in self.wall:
            self.screen.blit(self.wall_surface,pos)

        pygame.display.update()
    
    def AppleRandom(self):
        x = random.randint(10,self.x_len - 10)
        y = random.randint(10,self.y_len - 10)
        return (x//10 * 10, y//10 * 10)

    def CheckCatchApple(self,snake):
        if snake.coord[0][0] == self.apple_coord[0] and snake.coord[0][1] == self.apple_coord[1]:
            self.apple_coord = self.AppleRandom()
            snake.coord.append((0,0))
            self.fitness *= 2 
            self.score += 1
            ## Permitir mais passos sempre que pegar uma maça, não permitindo ultrapassar um limite de passos máximo
            self.max_steps += (self.x_len + self.y_len)
            if self.max_steps > (self.x_len + self.y_len)*3:
                self.max_steps = (self.x_len + self.y_len)*3
            #print("pegou")
        else:
            self.fitness += ((self.x_len/(abs(self.apple_coord[0] - snake.coord[0][0])+1)) + (self.y_len/(abs(self.apple_coord[1] - snake.coord[0][1]) +1))) 
        #return snake

    def CheckColisson(self,snake):
        ## Checar se houve colisão da cobra com ela mesma
        for index in range(len(snake.coord) - 1):
            if snake.coord[0] == snake.coord[index + 1]:
                return True
        
        for index in range(len(self.wall)):
            if snake.coord[0] == self.wall[index]:
                return True
        
        return False

    def CheckFinalStep(self):
        ## Reduzir o número de passsos
        self.max_steps+=-1
        if(self.max_steps <= 0):
            return True
        else:
            return False

    def GameOver(self):
        font = pygame.font.SysFont('chalkduster.ttf', 100)
        img = font.render('Game Over', True, (0, 0, 255))
        self.screen.blit(img, (self.x_len/2 - 170, self.y_len/2-50))
        #self.screen.blit(background_image, (0,0))
        pygame.display.update()
        return self.fitness,self.score

    def CalculateDistances(self,snake):
        return np.array([float(self.apple_coord[0] - snake.coord[0][0]),float(self.apple_coord[1] - snake.coord[0][1]),
        float(self.x_len - snake.coord[0][0]),float(0 - snake.coord[0][0]),float(self.y_len - snake.coord[0][1]),float(0 - snake.coord[0][1]),
        float(snake.coord[0][0] - snake.coord[len(snake.coord)-1][0]),float(snake.coord[0][1] - snake.coord[len(snake.coord)-1][1])])
