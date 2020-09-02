import pygame

class Snake:
    def __init__(self):
        self.coord =  [(300, 300), (310, 300), (320,300)]
        self.surface = pygame.Surface((10,10))
        self.surface.fill((255,255,255))
        self.direction = "LEFT"

    def UpdateSnake(self):
        for i in range(len(self.coord) - 1, 0, -1):
            self.coord[i] = (self.coord[i-1][0], self.coord[i-1][1])

        if self.direction == 'UP':
            self.coord[0] = (self.coord[0][0], self.coord[0][1] - 10)
        if self.direction == 'DOWN':
            self.coord[0] = (self.coord[0][0], self.coord[0][1] + 10)
        if self.direction == 'RIGHT':
            self.coord[0] = (self.coord[0][0] + 10, self.coord[0][1])
        if self.direction == 'LEFT':
            self.coord[0] = (self.coord[0][0] - 10, self.coord[0][1])

    def UpdateDirection(self,direction):
        if direction != None:
            self.direction = direction
