import numpy as np

def preparateInputData(inputData, length):
    #Normalização dos dados e guardar os maiores e menores valores por coluna
    #print(inputData)
    for column in range(len(inputData)):
        #inputData[column]+=-0.5
        
        if column in [2,5,8,11,14,17,20,23]:
            inputData[column] = ( inputData[column]  / length) - 0.5
            #inputData[column] = ( inputData[column] - (-length) ) / ( 2*length) -0.5
            #inputData[column] = ( inputData[column] - (-length) ) / ( 2*length)
        elif column in [24,25]:
            #print(str(column) + " " + str(inputData[column]))
            #print(length)
            inputData[column] = ( (inputData[column] + length) / (2*length)) - 0.5
            #print(inputData[column])
        else:
            inputData[column]+=-0.5
        
    #Concatenar uma matriz coluna igual a -1
    aux_matrix = -1 * np.ones( (1,1) )

    new_inputData = np.concatenate((aux_matrix,inputData[np.newaxis]),axis=1)

    return new_inputData