import pygame
from obstaculos import *
from inimigos import *

class Mapa:
    def __init__(self, tamanho):
        self.__tamanho = tamanho
        self.__lista_de_entidades = []
        self.__lista_de_display = []
        self.__campo_visivel = pygame.Rect(-50,-50,tamanho[0]+100,tamanho[1]+100)

    @property
    def lista_de_entidades(self):
        return self.__lista_de_entidades

    @lista_de_entidades.setter
    def lista_de_entidades(self, lista_de_entidades):
        self.__lista_de_entidades = lista_de_entidades
    
    @property
    def campo_visivel(self):
        return self.__campo_visivel

    def iniciar(self, entidades):
        self.__lista_de_entidades = entidades

    def atualizar(self, tela,campo_visivel,dimensoes_tela):
        # O CAMPO_VISIVEL FAZ COM QUE APENAS OBJETOS NA TELA SEJAM RENDERIZADOS
        # PODE AJUDAR CASO OS MAPAS FIQUEM MUITO GRANDES
        self.__campo_visivel = campo_visivel
        for entidade in self.__lista_de_entidades:
            if campo_visivel.colliderect(entidade.corpo):
                if entidade.atualizar(tela, self, dimensoes_tela):
                    self.__lista_de_entidades.remove(entidade)
        for elemento_hud in self.__lista_de_display:
            elemento_hud.atualizar(tela)

##### INSTANCIAS DE MAPAS #####

width = 1000
height = 600

fase1 = [
    CanoVertical('cano1', 550, 475, height),
    CanoVertical('cano2', 800, 475, height),
    CanoVertical('cano2', 1500, 475, height),

    Bloco('bloco1', 200, 400),
    Bloco('bloco2', 250, 400),
    Bloco('bloco3', 300, 400),
    Bloco('bloco4', 350, 400),

    Chao('chao1', height-10, -200, 350),
    Chao('chao2', height-10, 450, 2000),

    Vida('vida', 140, 50),
    Tempo('tempo', 470, 50),
    Moeda('moeda', 800, 50),

    Borda('borda1', 0),
    Borda('borda1', 2000),

    ##### INIMIGOS #####

    Goomba('goomba1', 600, height - 50)
]

fase2 = [
    CanoVertical('cano1', -9000, 475, height),
    CanoVertical('cano2', 1600, 475, height),

    Chao('chao1', height - 10, -1000, 2000),

    ##### INIMIGOS #####
    Goomba('goomba',100,height-50),
    Goomba('goomba',600,height-50),
    Goomba('goomba',1000,height-50),
    Goomba('goomba',1200,height-50),
    Goomba('goomba',1400,height-50),
    Goomba('goomba',1600,height-50)
]