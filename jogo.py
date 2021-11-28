from pandas import read_csv

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
    teste,  colunaNova, linhaNova = move(lista,coluna,linha,mover)
    if str(teste)=="l" or str(teste)=="c" or str(teste)=="p" or str(teste)=="f":
        return str(teste)
    else:
        lista[colunaNova][linhaNova] = lista[coluna][linha]
        lista[coluna][linha] = teste
        return lista, colunaNova, linhaNova

def jogarJogoManual():
    Dados = read_csv("./Data/Dados.csv", sep=";", header=None)
    coluna, linha = acharInicio(Dados) 
    pontuação = 0
    fim = "i"    
    while fim != "f":
        digitado = int(input())
        jogada = movimento(Dados,coluna,linha,digitado)
        if type(jogada) == type(""):
            if jogada == "p":
                pontuação -= 1000
            elif jogada == "c":
                pontuação -= 100
            elif jogada == "f":
                pontuação += 500
                fim = "f"
            print(Dados)
            print("")
            print("Pontuação: ", pontuação)
        else:
            pontuação += 100
            Dados, coluna, linha = jogada
            print(Dados)
            print("")
            print("Pontuação: ", pontuação)

jogarJogoManual()
            