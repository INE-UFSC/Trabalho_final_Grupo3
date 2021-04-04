import pygame
from obstaculos import *
from inimigos import *

class Mapa:
    def __init__(self, tamanho):
        self.__tamanho = tamanho
        self.__listaDeObstaculos = []
        self.__listaDeInimigos = []

    @property
    def listaDeObstaculos(self):
        return self.__listaDeObstaculos

    @listaDeObstaculos.setter
    def listaDeObstaculos(self, listaDeObstaculos):
        self.__listaDeObstaculos = listaDeObstaculos

    @property
    def listaDeInimigos(self):
        return self.__listaDeInimigos

    @listaDeInimigos.setter
    def listaDeInimigos(self, listaDeInimigos):
        self.__listaDeInimigos = listaDeInimigos

    def iniciar(self):

        ##### OBSTACULOS ##### (FUTURAMENTE UMA FUNCAO VAI LER ISSO DE UM ARQUIVO)

        self.__listaDeObstaculos.append(Cano_vertical('cano1', 550, 475, self.__tamanho[1]))
        self.__listaDeObstaculos.append(Cano_vertical('cano2', 800, 475, self.__tamanho[1]))

        self.__listaDeObstaculos.append(Bloco('bloco1', 200, 400))
        self.__listaDeObstaculos.append(Bloco('bloco2', 250, 400))
        self.__listaDeObstaculos.append(Bloco('bloco3', 300, 400))
        self.__listaDeObstaculos.append(Bloco('bloco4', 350, 400))

        self.__listaDeObstaculos.append(Chao('chao1', self.__tamanho[1]-10, 0, 350))
        self.__listaDeObstaculos.append(Chao('chao2', self.__tamanho[1]-10, 450, 1000))

        ##### INIMIGOS #####

        self.__listaDeInimigos.append(Goomba('goomba',600,self.__tamanho[1]-50))

    def atualizar(self, tela):
        for obstaculo in self.__listaDeObstaculos:
            obstaculo.atualizar(tela)
        for inimigo in self.__listaDeInimigos:
            inimigo.atualizar(tela, self.__tamanho, self)

    def mocao(self):
        pass
