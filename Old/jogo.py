from pandas import read_csv
import random
import numpy as np


def inicio(Dados):
    i, j = random.randrange(11), random.randrange(11)
    while True:
        if str(Dados[i][j]) == "v":
            break
        i, j = random.randrange(11), random.randrange(11)
    Dados[i][j] = "i"
    return Dados
        
def acharInicio(lista):
    localizou = False
    for i in range(len(lista)):
        if localizou:
            break
        for j in range(len(lista[i])):
            if str(lista[i][j])=="i":
                coluna, linha = i,  j
                localizou = True
    return  coluna, linha


def move(lista, coluna, linha, direcao):
    #Esquerda
    if direcao == 3:
        return lista[coluna-1][linha], coluna-1, linha
    #Direita
    elif direcao == 2:
        return lista[coluna+1][linha], coluna+1, linha    
    #Cima
    elif direcao == 1:
        return lista[coluna][linha-1], coluna, linha-1
    #Baixo
    elif direcao == 0:
        return lista[coluna][linha+1], coluna, linha+1


def movimento(lista, coluna, linha, mover):
    resultado,  colunaNova, linhaNova = move(lista,coluna,linha,mover)
    
    if str(resultado)=="c" or str(resultado)=="p" or str(resultado)=="f":
        lista[colunaNova][linhaNova] = lista[coluna][linha]
        lista[coluna][linha] = "v"
        return lista, colunaNova, linhaNova, resultado
    
    elif str(resultado)=="l":
        return resultado

    lista[colunaNova][linhaNova] = lista[coluna][linha]
    lista[coluna][linha] = resultado
    return lista, colunaNova, linhaNova

def jogada(Dados, coluna, linha, digitado):
    valor = movimento(Dados,coluna,linha,digitado)
    if len(valor) == 1:
            return Dados, coluna, linha, 0, True
    elif len(valor) == 4:
            if valor[len(valor)-1] == "p":
                coluna = valor[len(valor)-3]
                linha = valor[len(valor)-2]
                score = -1000
                return Dados, coluna, linha, score, True
            elif valor[len(valor)-1] == "c":
                coluna = valor[len(valor)-3]
                linha = valor[len(valor)-2]
                score = -100
                return Dados, coluna, linha, score, True
            elif valor[len(valor)-1] == "f":
                coluna = valor[len(valor)-3]
                linha = valor[len(valor)-2]
                score = 500
                return Dados, coluna, linha, score, False
    elif len(valor) == 3:
            coluna = valor[len(valor)-3]
            linha = valor[len(valor)-2]
            score = 100
            return Dados, coluna, linha, score, True

def jogarJogoManual():
    Dados = read_csv("./Data/Dados.csv", sep=";", header=None, index_col = False)
    Dados = inicio(Dados)
    coluna, linha = acharInicio(Dados) 
    pontua????o = 0
    print(Dados)
    Teste = True
    while Teste:
        digitado = int(input("Digite:\n0 para Descer\n1 para Subir\n2 para Direita\n3 para Esquerda\n"))
        Dados, coluna, linha, score, teste = jogada(Dados, coluna, linha, digitado)
        pontua????o += score
        print("\nPontua????o Atual: " + str(pontua????o) + " Pontua????o adquirida: " + str(score) + "\r\n")
        print(Dados)

def jogarQlearning():
    # Inicializa????o com a tabela de valores Q
    q_table = np.zeros([100, 4])
    
    
    # Hiperpar??metros
    alpha = 0.1   # taxa de aprendizagem
    gamma = 0.6   # fator de desconto
    epsilon = 0.1  # chance de escolha aleat??ria  
    
    # Total geral de a????es executadas e penalidades recebidas durante a aprendizagem
    epochs, penalties = 0,0
    
    for i in range(1, 100001): # Vai rodar 100000 diferentes vers??es do problema
        Dados = read_csv("./Data/Dados.csv", sep=";", header=None, index_col = False)
        Dados = inicio(Dados)
        coluna, linha = acharInicio(Dados) 
        done = False
        
        while not done:
            if random.uniform(0, 1) < epsilon:
                action = random.randrange(4) # Escolhe a????o aleatoriamente
            else:
                action = np.argmax(q_table[Dados]) # Escolhe a????o com base no que j?? aprendeu
    
                next_state, coluna, linha, reward, done= jogada(Dados, coluna, linha, action) # Aplica a a????o
            
                old_value = q_table[Dados, action]  # Valor da a????o escolhida no estado atual
                next_max = np.max(q_table[next_state]) # Melhor valor no pr??ximo estado
            
                # Atualize o valor Q usando a f??rmula principal do Q-Learning
                new_value = (1 - alpha) * old_value + alpha * (reward + gamma * next_max)
                q_table[Dados, action] = new_value
    
                if reward <= 0:  # Contabiliza as puni????es por pegar ou deixar no lugar errado
                    penalties += 1
    
                Dados = next_state # Muda de estado
                epochs += 1
        state = 329
        epochs, penalties = 0, 0
    
        done = False

    while not done:
        action = np.argmax(q_table[Dados])
        state, coluna, linha, reward, done= jogada(Dados, coluna, linha, action)
        print(Dados)
        if reward <= 0:
            penalties += 1
        epochs += 1

    print("Total de a????es executadas: {}".format(epochs))
    print("Total de penaliza????es recebidas: {}".format(penalties))


jogarQlearning()