import pygame
from obstaculos import *
from inimigos import *

class Mapa:
    def __init__(self, tamanho):
        self.__tamanho = tamanho
        self.__lista_de_obstaculos = []
        self.__lista_de_inimigos = []
        self.__lista_de_display = []
        self.__campo_visivel = pygame.Rect(-50,-50,tamanho[0]+100,tamanho[1]+100)

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
    
    @property
    def campo_visivel(self):
        return self.__campo_visivel

    def iniciar(self):

        ##### OBSTACULOS ##### (FUTURAMENTE UMA FUNCAO VAI LER ISSO DE UM ARQUIVO)

        self.__lista_de_obstaculos.append(CanoVertical('cano1', 550, 475, self.__tamanho[1]))
        self.__lista_de_obstaculos.append(CanoVertical('cano2', 800, 475, self.__tamanho[1]))
        self.__lista_de_obstaculos.append(CanoVertical('cano3', 1300, 475, self.__tamanho[1]))
        self.__lista_de_obstaculos.append(CanoVertical('cano4', 1900, 475, self.__tamanho[1]))
        self.__lista_de_obstaculos.append(CanoVertical('cano5', 2150, 350, self.__tamanho[1]))

        self.__lista_de_obstaculos.append(Bloco('bloco1', 200, 400))
        self.__lista_de_obstaculos.append(Bloco('bloco2', 250, 400))
        self.__lista_de_obstaculos.append(Bloco('bloco3', 300, 400))
        self.__lista_de_obstaculos.append(Bloco('bloco4', 350, 400))

        self.__lista_de_obstaculos.append(Chao('chao1', self.__tamanho[1]-10, 0, 350))
        self.__lista_de_obstaculos.append(Chao('chao2', self.__tamanho[1]-10, 450, 1600))
        self.__lista_de_obstaculos.append(Chao('chao3', self.__tamanho[1]-10, 1700, 2400))

        ##### HUD COM VIDA, TEMPO, MOEDA #####

        self.__lista_de_display.append(Vida('vida', 140, 50))
        self.__lista_de_display.append(Tempo('tempo', 470, 50))
        self.__lista_de_display.append(Moeda('moeda', 800, 50))

        ##### INIMIGOS #####

        self.__lista_de_inimigos.append(Goomba('goomba',600,self.__tamanho[1]-50))

    def atualizar(self, tela,campo_visivel):
        # O CAMPO_VISIVEL FAZ COM QUE APENAS OBJETOS NA TELA SEJAM RENDERIZADOS
        # PODE AJUDAR CASO OS MAPAS FIQUEM MUITO GRANDES
        self.__campo_visivel = campo_visivel
        for obstaculo in self.__lista_de_obstaculos:
            if campo_visivel.colliderect(obstaculo.corpo):
                obstaculo.atualizar(tela,self)
        for inimigo in self.__lista_de_inimigos:
            if campo_visivel.colliderect(inimigo.corpo):
                inimigo.atualizar(tela, self.__tamanho, self)
        for elementohud in self.__lista_de_display:
            elementohud.atualizar(tela)

    def mocao(self):
        pass
