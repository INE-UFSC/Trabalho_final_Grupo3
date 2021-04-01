class Menu:
    def __init__(self, tela):
        self.__tela = tela
    
    @property
    def tela(self):
        return self.__tela
    
    @tela.setter
    def tela (self, tela):
        self.__tela = tela
    
    def trocar_tela():
        pass
    
class Tela:
    def __init__(self,listabotoes:list,fundo):
        self.__listabotoes = listabotoes
        self.__fundo = fundo
    
class Botao:
    def __init__(self,x,y,w,h,cor,corhover,texto):
        self.__x = x
        self.__y = y
        self.__w = w
        self.__h = h
        self.__cor = cor
        self.__corhover = corhover
        self.__texto = texto
    
    def destaque():
        pass
    
    def click():
        pass
