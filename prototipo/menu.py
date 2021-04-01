import pygame

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
    def __init__(self,x,y,w,h,cor,corhover,texto,borda):
        self.__x = x
        self.__y = y
        self.__w = w
        self.__h = h
        self.__cor = cor
        self.__corhover = corhover
        self.__texto = texto
    
    def renderizar(self,surface):
        pos = pygame.mouse.get_pos()
        pygame.draw.rect(surface,(0,0,0),[self.__x,self.__y,self.__w,self.__h])
        if self.__x <= pos[0] <= self.__x + self.__w and self.__y <= pos[1] <= self.__y + self.__h:
            pygame.draw.rect(surface,corhover,[self.__x+borda,self.__y+borda,self.__w-2*borda,self.__h-2*borda])
        else:
            pygame.draw.rect(surface,cor,[self.__x+borda,self.__y+borda,self.__w-2*borda,self.__h-2*borda])

    def clicar():
        if self.__x <= pos[0] <= self.__x + self.__w and self.__y <= pos[1] <= self.__y + self.__h:
            return True
        else:
            return False
