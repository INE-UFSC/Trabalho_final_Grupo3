import pygame
from obstaculos import *
from inimigos import *

class Mapa:
    def __init__(self, tamanho):
        self.__tamanho = tamanho
        self.__lista_de_obstaculos = []
        self.__lista_de_inimigos = []

    @property
    def lista_de_obstaculos(self):
        return self.__lista_de_obstaculos

    @lista_de_obstaculos.setter
    def lista_de_obstaculos(self, lista_de_obstaculos):
        self.__lista_de_obstaculos = lista_de_obstaculos

    @property
    def lista_de_inimigos(self):
        return self.__lista_de_inimigos

    @lista_de_inimigos.setter
    def lista_de_inimigos(self, lista_de_inimigos):
        self.__lista_de_inimigos = lista_de_inimigos

    def iniciar(self):

        ##### OBSTACULOS ##### (FUTURAMENTE UMA FUNCAO VAI LER ISSO DE UM ARQUIVO)

        self.__lista_de_obstaculos.append(CanoVertical('cano1', 550, 475, self.__tamanho[1]))
        self.__lista_de_obstaculos.append(CanoVertical('cano2', 800, 475, self.__tamanho[1]))
        self.__lista_de_obstaculos.append(CanoVertical('cano2', 1500, 475, self.__tamanho[1]))

        self.__lista_de_obstaculos.append(Bloco('bloco1', 200, 400))
        self.__lista_de_obstaculos.append(Bloco('bloco2', 250, 400))
        self.__lista_de_obstaculos.append(Bloco('bloco3', 300, 400))
        self.__lista_de_obstaculos.append(Bloco('bloco4', 350, 400))

        self.__lista_de_obstaculos.append(Chao('chao1', self.__tamanho[1]-10, -200, 350))
        self.__lista_de_obstaculos.append(Chao('chao2', self.__tamanho[1]-10, 450, 2000))

        self.__lista_de_obstaculos.append(Vida('vida', 140, 50))
        self.__lista_de_obstaculos.append(Tempo('tempo', 470, 50))
        self.__lista_de_obstaculos.append(Moeda('moeda', 800, 50))

        ##### INIMIGOS #####

        self.__lista_de_inimigos.append(Goomba('goomba',600,self.__tamanho[1]-50))

    def atualizar(self, tela, velocidade):
        for obstaculo in self.__lista_de_obstaculos:
            obstaculo.x += velocidade
            if obstaculo.nome == "cano1": print(obstaculo.x)
            obstaculo.atualizar(tela)

        for inimigo in self.__lista_de_inimigos:
            inimigo.x += velocidade
            inimigo.atualizar(tela, self.__tamanho, self)