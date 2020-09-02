import numpy as np

def feedfoward(weights,topology,inputData,d_length,length):

    I,Y = init_variables(topology,len(inputData),d_length)
    newData = preparateInputData(inputData,length)
    #print("input: " + str(newData))
    for ctr in range( len(topology) + 1 ):
        if ctr == 0:
            I[ctr] = np.dot(weights[ctr] , newData.transpose())
            Y[ctr] = np.concatenate( (-1*np.ones((1,1)), np.tanh(I[ctr])) )
        elif ctr == len(topology):
            I[ctr] = np.dot(weights[ctr],Y[ctr-1])
            Y[ctr] = np.tanh(I[ctr])
        else:
            I[ctr] = np.dot(weights[ctr],Y[ctr-1])
            Y[ctr] = np.concatenate( (-1*np.ones((1,1)), np.tanh(I[ctr])) )
    #print("saida: " + str(Y[len(topology)]))
    return realizeProbability(Y[len(topology)])

def preparateInputData(inputData, length):
        #Normalização dos dados e guardar os maiores e menores valores por coluna
        for column in range(len(inputData)):
            inputData[column] = ( inputData[column] - (-length) ) / ( 2*length) -0.5
        #Concatenar uma matriz coluna igual a -1
        aux_matrix = -1 * np.ones( (1,1) )

        new_inputData = np.concatenate((aux_matrix,inputData[np.newaxis]),axis=1)

        return new_inputData

def init_variables(topology,x_train_length,d_train_length):
    I = []
    Y = []
    accumulator = []
    gradient = []

    # Inicializar as entradas e saídas de cada camada e o gradiente ( que possui as mesmas dimensões da entrada da camada)
    for index in range(len(topology) +1):
        if index == len(topology):
            Iaux = np.zeros((d_train_length,1))
            Yaux = np.zeros((d_train_length,1))
        else:
            Iaux = np.zeros((topology[index],1))
            Yaux = np.zeros((topology[index]+1,1))

        I.append(Iaux)
        Y.append(Yaux)
        
    return I,Y

def realizeProbability(vector):
    result = []
    for index in range(len(vector)):
        if vector[index] == max(vector):
            result.append(1)
        else:
            result.append(-1)
    
    return result