import random as rd

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