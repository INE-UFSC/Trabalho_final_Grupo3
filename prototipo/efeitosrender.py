
def colorwheel(value):              # transforma um valor continuo em um arco em graus
    return max(0,min(2-abs(120-value%360)/60,1))

def psicodelico(cor):               # retorna a cor rbg correspondente ao arco
    r = 255 * colorwheel(cor-120)
    g = 255 * colorwheel(cor)
    b = 255 * colorwheel(cor+120)
    return [r,g,b]

def misturacor(cor1,cor2,peso1=1,peso2=1):                      # retorna uma media entre duas cores
    r = (cor1[0] * peso1 + cor2[0] * peso2)/(peso1+peso2)       # como a visao humana eh logaritmica
    g = (cor1[1] * peso1 + cor2[1] * peso2)/(peso1+peso2)       # o resultado pode nao ser perfeito
    b = (cor1[2] * peso1 + cor2[2] * peso2)/(peso1+peso2)
    return [r,g,b]