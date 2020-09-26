import random as rd
import numpy as np

def Mutation(offspring,mutationRate):
    for weigth in offspring:
        for row in range(len(weigth)):
            for col in  range(len(weigth[0])):
                numb = rd.random()
                if numb <= mutationRate:
                    weigth[row][col] += 0.4*rd.random() -0.2

                    if weigth[row][col] > 1:
                        weigth[row][col] = 1
                    elif weigth[row][col] < -1:
                        weigth[row][col] = -1
    return offspring

def Crossover(parents):

    ##Gerar um filho novo filho
    child = []

    for layer in range(len(parents[0])):
        ## Sortear um ponto na matriz de pesos
        point = rd.randint(0,15)
        ## Inicializar matriz de pesos
        weigth = parents[0][layer]

        for row in range(len(parents[0][layer])):
            for col in range(len(parents[0][layer][0])):
                if point<=0:
                    weigth[row][col] = parents[1][layer][row][col]
                point -= 1
        child.append(weigth)
    
    return child
    
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

    for son in offspring:
        for layer in range(len(son)):
            ##Quantidade de elementos da matriz de pesos para todas as linhas e colunas
            for line in range(np.shape(son[layer])[0]):
                for column in range(np.shape(son[layer])[1]):
                    ##Verificar se vai haver mutação
                    r = rd.random()
                    if r<tax:       
                        ##Etapa de mutação utilizando distribuição gaussiana
                        son[layer][line][column] += std*rd.random() + mean
    return offspring