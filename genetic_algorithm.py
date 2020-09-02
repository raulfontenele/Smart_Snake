import numpy as np
import random as rd
from Scene import Scene
from Snake import Snake
import pygame, random
from pygame.locals import *
from feedfoward import feedfoward

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

def ChooseBest(population,offspring,fitness,fitness_offspring):
    fitness_sorted = np.argsort(np.array(fitness+fitness_offspring))[-1:-int(len(population)+1):-1]
    population_merge = population + offspring
    fitness_merge = fitness+fitness_offspring
    #ziped = zip(population + offspring, fitness+fitness_offspring)
    new_population = [population_merge[i] for i in fitness_sorted]
    new_fitness = [fitness_merge[i] for i in fitness_sorted]
    return new_population,new_fitness

def Roulette(population,fitness):

    newParents = []
    ## Criar roleta
    if np.sum(fitness) != 0:
        roulette = fitness/np.sum(fitness) # ver a questão da quantidade de casas numérica
        for i in range(2):

            # Sortear número
            num = rd.random()

            acc = 0
            for index in range(len(fitness)):
                acc += roulette[index]
                if num < acc:
                    newParents.append(population[index])
                    break
    else:
        for i in range(2):
            index = rd.randint(0,len(population) - 1)
            newParents.append(population[index])
    return newParents

def crossoverBlx(parents,tax):
    ##Verificar se deve haver cruzamento
    num = rd.random()

    if num <= tax:
        offspring = []
        ##Gerar dois novos novos filhos
        for index in range(2):
            child = []
            for layer in range(len(parents[0])):
                ## b variando entre -0,5 e 1,5
                b = 2*rd.random() -0.5
                if index == 0:
                    weigth = parents[0][layer] + b*(parents[1][layer] - parents[0][layer])
                else:
                    weigth = parents[1][layer] + b*(parents[0][layer] - parents[1][layer])
                child.append(weigth)
            offspring.append(child)
        
        return offspring
    else:
        return parents
        

def GaussMatation(offspring,tax,mean,std):
    #print(offspring)
    for son in offspring:
        ##Verificar se vai haver mutação
        r = rd.random()
        if r<tax:
            for layer in range(len(son)):
                #print(son)
                #print(son[layer])
                ##Quantidade de elementos da matriz de pesos para todas as linhas e colunas
                for line in range(np.shape(son[layer])[0]):
                    for column in range(np.shape(son[layer])[1]):
                #for index in range(np.size(son[layer])):         
                    ##Etapa de mutação utilizando distribuição gaussiana
                        son[layer][line][column] += std*rd.random() + mean
    return offspring    




def Main(topology,mutation_tax,crossover_tax,qtd_population,qtd_offspring,generations,std):
    x_train_length = 8
    d_train_length = 4
    screen_length = 600
    x_screen = 600
    y_screen = 600
    clock = pygame.time.Clock()

    fps = 1200

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
    for i in range(qtd_offspring):
        offspring_population.append(init_weigth(topology,x_train_length,d_train_length))
        offspring_fitness.append(0)
    
    ##Repetir o sistema pela quantidade de gerações especificadas
    for gen in range(generations):
        print("Começou a geração " + str(gen))
        score_gen = 0
        ## Calcular fitness
        for index in range(qtd_population):
            scene = Scene(x_screen,y_screen)
            snake = Snake()

            while True:
                clock.tick(fps)

                coord = scene.CalculateDistances(snake)
                dir = feedfoward(population[index],topology,coord,4,x_screen)
                direction = ConvertDirection(dir)

                snake.UpdateDirection(direction)

                scene.CheckCatchApple(snake)

                snake.UpdateSnake()

                ret = scene.CheckColisson(snake)
                if ret == False:
                    scene.UpdateScreen(snake)
                else:
                    fit,score = scene.GameOver()
                    #print("score:" + str(score))
                    fitness[index] = fit
                    if (score>max_score): 
                        max_score = score
                    if score > score_gen:
                        score_gen = score
                    break


        ##Gerar novos filhos
        for index in range(int(qtd_offspring/2)):

            ##Roleta
            offspring = Roulette(population,fitness)

            ##Crossover
            offspring = crossoverBlx(offspring,crossover_tax)

            ##Mutação
            offspring = GaussMatation(offspring,mutation_tax,0,std)
            
            for i in range(2):
                offspring_population[i] = offspring[i]

        #print("Fitness dos filhos")
        ## Calcular fitness dos novos filhos
        for index in range(len(offspring_population)):
            scene = Scene(x_screen,y_screen)
            snake = Snake()

            while True:
                clock.tick(fps)

                coord = scene.CalculateDistances(snake)
                dir = feedfoward(offspring_population[index],topology,coord,4,x_screen)
                direction = ConvertDirection(dir)

                snake.UpdateDirection(direction)

                scene.CheckCatchApple(snake)

                snake.UpdateSnake()

                ret = scene.CheckColisson(snake)
                if ret == False and scene.CheckFinalStep() == False:
                    scene.UpdateScreen(snake)
                else:
                    if scene.CheckFinalStep() == True:
                        print("morreu pela quantidade de passos")
                    fit,score = scene.GameOver()
                    #print("score:" + str(score))
                    offspring_fitness[index] = fit
                    if (score>max_score): 
                        max_score = score
                    if score > score_gen:
                        score_gen = score
                    break

        ## Escolher os melhores entre pais e filhos
        population,fitness  = ChooseBest(population,offspring_population,fitness,offspring_fitness)
        print("Média: " + str(sum(fitness)/len(fitness)))
        print("Máximo: " + str(max(fitness)))
        print("Score Máximo: " + str(max_score))
        print("Score Geracao: " + str(score_gen))           
    
def init_weigth(topology,x_train_length,d_train_length):
    weights = []
    # Inicializar as matrizes de pesos e o acumulador
    for index in range(len(topology)+1):
        if index == 0:
            weight = np.random.rand(topology[index], x_train_length+1)-0.5
        elif index == len(topology):
            weight = np.random.rand(d_train_length,topology[index-1] + 1)-0.5
        else:
            weight = np.random.rand(topology[index], topology[index-1]+1)-0.5
        
        weights.append(weight)

    return weights

Main([20,20,20],0.15,0.9,300,600,20,0.1)