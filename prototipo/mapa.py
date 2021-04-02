import pygame
from obstaculo_generico import ObstaculoGenerico
class Mapa: 

    def __init__(self, tamanho):
        self.__tamanho = tamanho
        #self.__desenho = desenho 

    def inicializacao(self):
        bloco1 = ObstaculoGenerico('bloco')
        #print(bloco1.__tipo)
        return (pygame.Rect((550,350), (75, 75)), bloco1)

    def mocao():
        pass
