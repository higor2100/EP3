from pandas import read_csv

def acharInicio(lista):
    localizou = False
    for i in range(len(teste)):
        if localizou:
            break
        for j in range(len(teste[i])):
            if str(teste[i][j])=="i":
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
        return lista[coluna][linha+1], coluna, linha+1
    #Baixo
    elif direcao == 0:
        return lista[coluna][linha-1], coluna, linha-1

        


def movimento(lista, coluna, linha, mover):
    teste,  colunaNova, linhaNova = move(lista,coluna,linha,mover)
    if str(teste)=="l" or str(teste)=="c" or str(teste)=="p" or str(teste)=="f":
        return str(teste)
    else:
        lista[colunaNova][linhaNova] = lista[coluna][linha]
        lista[coluna][linha] = teste
        return lista, linhaNova, colunaNova

teste = read_csv("./Data/Dados.csv", sep=";", header=None)
coluna, linha = acharInicio(teste)


jogada = movimento(teste,coluna,linha,3)
print(type(jogada) == type(""))
jogada = movimento(teste,coluna,linha,2)
print(type(jogada)==type(()))
