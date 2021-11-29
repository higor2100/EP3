from pandas import read_csv
from random import randrange

def inicio(Dados):
    i, j = randrange(11), randrange(11)
    while True:
        if str(Dados[i][j]) == "v":
            break
        i, j = randrange(11), randrange(11)
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
    if str(resultado)=="l" or str(resultado)=="c" or str(resultado)=="p" or str(resultado)=="f":
        return str(resultado)
    else:
        lista[colunaNova][linhaNova] = lista[coluna][linha]
        lista[coluna][linha] = resultado
        return lista, colunaNova, linhaNova

def jogarJogoManual():
    Dados = read_csv("./Data/Dados.csv", sep=";", header=None, index_col = False)
    Dados = inicio(Dados)
    coluna, linha = acharInicio(Dados) 
    pontuação = 0
    fim = "i"    
    while fim != "f":
        print(Dados)
        digitado = int(input("Digite:\n0 para Descer\n1 para Subir\n2 para Direita\n3 para Esquerda\n"))
        score = 0
        jogada = movimento(Dados,coluna,linha,digitado)
        if type(jogada) == type(""):
            if jogada == "p":
                pontuação -= 1000
                score = -1000
            elif jogada == "c":
                pontuação -= 100
                score = -100
            elif jogada == "f":
                pontuação += 500
                score = 500
                fim = "f"
            print(Dados)
            print("\nPontuação Atual: " + str(pontuação) + " Pontuação adquirida: " + str(score))
        else:
            pontuação += 100
            score = 100
            Dados, coluna, linha = jogada
            print(Dados)
            print("")
            print("\nPontuação Atual: " + str(pontuação) + " Pontuação adquirida: " + str(score))

jogarJogoManual()
            