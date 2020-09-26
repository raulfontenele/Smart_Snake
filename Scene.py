import pygame,random
from pygame.locals import *
from Snake import Snake
import numpy as np
import math

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

        self.max_steps = (self.x_len + self.y_len)/10
        self.steps = 0

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
               
            self.score += 1
            #.fitness += self.score*self.fitness
            ## Permitir mais passos sempre que pegar uma maça, não permitindo ultrapassar um limite de passos máximo
            self.max_steps += (self.x_len + self.y_len)/10
            if self.max_steps > (self.x_len + self.y_len)*3/10:
                self.max_steps = (self.x_len + self.y_len)*3/10
            #print("pegou")
        #else:
            #self.fitness += ((self.x_len/(abs(self.apple_coord[0] - snake.coord[0][0]) + 1 )) + (self.y_len/(abs(self.apple_coord[1] - snake.coord[0][1]) + 1)))*2 
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
        self.steps += 1
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
        fitness = self.CalculateFitness()
        return fitness,self.score

    def CalculateDistances(self,snake):
        return np.array([float(self.apple_coord[0] - snake.coord[0][0]),float(self.apple_coord[1] - snake.coord[0][1]),
        float(self.x_len - snake.coord[0][0]),float(0 - snake.coord[0][0]),float(self.y_len - snake.coord[0][1]),float(0 - snake.coord[0][1])])
        #float(snake.coord[0][0] - snake.coord[len(snake.coord)-1][0]),float(snake.coord[0][1] - snake.coord[len(snake.coord)-1][1])

    def CalculateFitness(self):
        if self.score < 10:
            fitness = math.floor(self.steps*self.steps) * math.pow(2,self.score) 
        else:
            fitness = math.floor(self.steps * self.steps)
            fitness *= math.pow(2,10)
            fitness *= (self.score-9)
        return fitness

    def CalculateMetrics(self,snake):
        metrics = []
        for i in range(24):
            metrics.append(0)
        
        directions = [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]
        for index in range(len(directions)):
            look = self.LookInDirection(directions[index],snake)
            for i in range(3):
                metrics[index*3+i] = look[i]

        return np.array(metrics)
        

    def LookInDirection(self,dir,snake):

        ## Inicializaçaõ de variáveis
        point = list(snake.coord[0])
        distance = 0
        data = []

        ## Inicializar dados de retorno
        for i in range(3):
            data.append(float(0))

        while self.CheckColisionWall(point) == False:  
            ##Incremento na direção
            distance+=1
            for i in range(len(dir)):
                point[i]+=10*int(dir[i])
            if self.CheckColisionApple(point) == True:
                data[0] = 1
            if self.CheckColisionBody(point,snake) == True:
                data[1] = float(1/distance)

        data[2] = float(1/distance)
        
        return data
        
    def CheckColisionWall(self,coord):
        ## Checar colisão com a parede
        #print(coord)
        #print(self.wall)
        if tuple(coord) in self.wall:
            return True
        else:
            return False
    def CheckColisionBody(self,coord,snake):
        ##Checar colisão com o próprio corpo
        if tuple(coord) in snake.coord:
            #print("corpitcho")
            return True
        else:
            return False
    def CheckColisionApple(self,coord):
        #print(coord)
        #print(self.apple_coord)
        ##Checar colisão com o próprio corpo
        if tuple(coord) == self.apple_coord:
            #print("achou")
            return True
        else:
            return False
