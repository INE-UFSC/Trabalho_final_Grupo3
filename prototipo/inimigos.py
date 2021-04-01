#Arquivo destinado a fazer todos os inimigos
import pygame
from entidades import Entidade
class Goomba(Entidade):
    def __init__(self, nome: str, x: int, y: int, largura:int, altura:int, limiteVel: int):
        vida = 1
        danoContato = 1
        super().__init__(nome, x, y, largura, altura, limiteVel, self.vida, self.danoContato)

    def Atualizar(self, tela):
        self.__y += self.__vely
        self.__x += self.__velx
        pygame.draw.rect(tela, (88,51,0), self.__corpo)#88, 51, 0