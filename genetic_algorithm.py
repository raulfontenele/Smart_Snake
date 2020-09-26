import numpy as np
import random as rd
from Scene import Scene
from Snake import Snake
import pygame, random
from pygame.locals import *
from feedfoward import feedfoward
from normalize import preparateInputData
from genetic_operators import *

def ConvertDirection(vector):
    if vector == [-1,-1,-1,1]:
        my_direction = 'UP'
    elif vector == [-1,-1,1,-1]:
        my_direction = 'DOWN'
    elif vector == [-1,1,-1,-1]:
        my_direction = 'LEFT'
    #elif vector == [1,-1,-1,-1]:
    else:
        my_direction = 'RIGHT'
    return my_direction


def SaveBestParent(population,fitness):

    ## Guardar o índice do filho com melhor fitness
    best_index = np.argsort(np.array(fitness))[-1]

    return population[best_index]

def Roulette(population,fitness):

    ## Criar roleta
    roulette = fitness/np.sum(fitness) 
    # Sortear número
    num = rd.random()

    acc = 0
    for index in range(len(fitness)):
        acc += roulette[index]
        if num < acc:
            return population[index] 


def PlayGame(scene,snake,population,topology,fps):

    clock = pygame.time.Clock()
    while True:
        clock.tick(fps)

        coord = preparateInputData(scene.CalculateMetrics(snake),60)

        dir = feedfoward(population,topology,coord,4)
        
        direction = ConvertDirection(dir)

        snake.UpdateDirection(direction)

        scene.CheckCatchApple(snake)

        snake.UpdateSnake()

        ret = scene.CheckColisson(snake)
        if ret == False and scene.CheckFinalStep() == False:
            scene.UpdateScreen(snake)
        else:
            fit,score = scene.GameOver()
            return fit,score
  

def Main(topology,mutation_tax,crossover_tax,qtd_population,generations):
    x_train_length = 24
    d_train_length = 4
    screen_length = 600
    x_screen = 600
    y_screen = 600

    fps = 2000

    population = []
    fitness = []
    offspring_population = []
    offspring_fitness = []

    max_score = 0

    for i in range(qtd_population):
        population.append(init_weigth(topology,x_train_length,d_train_length))
        offspring_population.append(init_weigth(topology,x_train_length,d_train_length))
        fitness.append(0)
        offspring_fitness.append(0)

    ##Repetir o sistema pela quantidade de gerações especificadas

    for gen in range(generations):
    
        print("Começou a geração " + str(gen+1))

        score_gen = 0
        ctrMortesPassos = 0

        ## Calcular fitness
        for index in range(qtd_population):
            scene = Scene(x_screen,y_screen)
            snake = Snake()
            
            fit,score = PlayGame(scene,snake,population[index],topology,fps)

            fitness[index] = fit
            if (score>max_score): 
                max_score = score
            if (score>score_gen): 
                score_gen = score

        ##Gerar novos filhos

        ## Salvar o melhor pai
        best = SaveBestParent(population,fitness)
        offspring_population[0] = best

        for index in range(qtd_population -1):
            ##Roleta
            parents=[]
            for i in range(2):
                parent= Roulette(population,fitness)  
                parents.append(parent)

            ##Crossover
            offspring = Crossover(parents)

            ##Mutação
            offspring = Mutation(offspring,mutation_tax)
            
            ## Adicionar a nova população
            offspring_population[index + 1] = offspring
        
        population = offspring_population


        print("Média: " + str(sum(fitness)/len(fitness)))
        print("Máximo: " + str(max(fitness)))
        print("Score Máximo: " + str(max_score))
        print("Score Geracao: " + str(score_gen))
        print("Mortes por excesso: " + str(ctrMortesPassos))            
    
def init_weigth(topology,x_train_length,d_train_length):
    weights = []
    # Inicializar as matrizes de pesos e o acumulador
    for index in range(len(topology)+1):
        if index == 0:
            weight = 2*np.random.rand(topology[index], x_train_length+1)-1
        elif index == len(topology):
            weight = 2*np.random.rand(d_train_length,topology[index-1] + 1)-1
        else:
            weight = 2*np.random.rand(topology[index], topology[index-1]+1)-1
        
        weights.append(weight)

    return weights

Main([15,15],0.01,0.9,2000,30)