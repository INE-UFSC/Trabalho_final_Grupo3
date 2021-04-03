import pygame
from obstaculos import *
class Mapa:
    def __init__(self, tamanho):
        self.__tamanho = tamanho
        #self.__desenho = desenho
        self.__listaDeObstaculos = []

    def iniciar(self):
        self.__listaDeObstaculos.append(Cano_vertical('cano1', 100, 300, 800))
        self.__listaDeObstaculos.append(Cano_vertical('cano2', 400, 300, 800))
        self.__listaDeObstaculos.append(Bloco('bloco1', 100, 100))
        self.__listaDeObstaculos.append(Cano_horizontal('cano3', 0, 400, 800))


    def atualizar(self, tela):
        for obstaculo in self.__listaDeObstaculos:
            obstaculo.atualizar(tela)

    def mocao(self):
        pass
