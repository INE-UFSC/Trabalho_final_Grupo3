import pygame
from entidades import Estatico, renderizar_hitbox, renderizar_sprite
from sprites import *

# FUNCOES DE ATUALIZAR NECESSITAM DA AREA VISIVEL PARA RENDERIZAR CORRETAMENTE
class Bloco(Estatico):
    def __init__(self, nome: str, x: int, y: int):
        largura = 30
        altura = 30
        super().__init__(nome, x, y, altura, largura, "0")

    def renderizar(self, tela, mapa):
        if renderizar_hitbox: pygame.draw.rect(tela, (255, 102, 0), [self.corpo.x-mapa.campo_visivel.x,self.corpo.y,self.corpo.w,self.corpo.h])

class CanoVertical(Estatico):
    def __init__(self, nome: str, x: int, topo: int, base: int):
        largura = 45
        altura= base-topo
        super().__init__(nome, x, topo, altura, largura, "muro")

    def renderizar(self, tela, mapa):
        if renderizar_hitbox: pygame.draw.rect(tela, (11, 137, 0), [self.corpo.x-mapa.campo_visivel.x,self.corpo.y,self.corpo.w,self.corpo.h])
        if renderizar_sprite: self.imagem.imprimir("muro", self.x-mapa.campo_visivel.x, self.y,tela, 1, 0)

class CanoHorizontal(Estatico):
    def __init__(self, nome: str, y: int, esquerda: int, direita: int):
        altura = 50
        largura = direita-esquerda
        super().__init__(nome, esquerda, y, altura, largura, "0")

    def renderizar(self, tela, mapa):
        if renderizar_hitbox: pygame.draw.rect(tela, (11, 137, 0), [self.corpo.x-mapa.campo_visivel.x,self.corpo.y,self.corpo.w,self.corpo.h])

class Chao(Estatico): 
    def __init__(self, nome: str, y: int, esquerda: int, direita: int):
        altura = 10
        super().__init__(nome, esquerda, y, altura, direita-esquerda, "0")

    def renderizar(self, tela, mapa):
        if renderizar_hitbox: pygame.draw.rect(tela, (184, 20, 20), [self.corpo.x-mapa.campo_visivel.x,self.corpo.y,self.corpo.w,self.corpo.h])

class Vida(Estatico):
    def __init__(self, nome: str, x: int, y: int):
        altura = 30
        largura = 60
        self.__fonte = pygame.font.SysFont('Arial',20)
        self.__vida = ""
        super().__init__(nome, x, y, altura, largura, "0")

    @property
    def vida(self):
        return self.__vida
    
    @vida.setter
    def vida(self, vida):
        self.__vida = vida

    def renderizar(self, tela, mapa):
        if renderizar_hitbox: pygame.draw.rect(tela, (10, 237, 0), self.corpo)
    
    def atualizar(self, tela, mapa, dimensoes_tela):
        self.renderizar(tela, mapa)
        mostra_vida = self.__fonte.render('vida :'+" "+str(self.__vida),0,(0,0,0))
        tela.blit(mostra_vida, (self.x, self.y))
        return False

class Tempo(Estatico):
    pygame.init()
    def __init__(self, nome: str, x: int, y: int):
        altura = 30
        largura = 70
        self.__fonte = pygame.font.SysFont('Arial',20)
        self.__tempo = 0
        self.__contador = self.__fonte.render('time :'+" "+str(self.tempo),0,(0,0,0))
        super().__init__(nome, x, y, altura, largura, "0")
    @property
    def tempo(self):
        return self.__tempo
    
    @tempo.setter
    def tempo(self, tempo):
        self.__tempo = tempo

    def renderizar(self, tela, mapa):
        if renderizar_hitbox: pygame.draw.rect(tela, (160, 160, 160), self.corpo)

    def atualizar(self, tela, mapa, dimensoes_tela):
        self.renderizar(tela, mapa)
        self.__contador = self.__fonte.render('time :'+" "+str(self.__tempo),0,(0,0,0))
        tela.blit(self.__contador, (self.x, self.y))
        return False

class Moeda(Estatico):
    def __init__(self, nome: str, x: int, y: int):
        altura = 30
        largura = 60
        super().__init__(nome, x, y, altura, largura, "0")

    def renderizar(self, tela, mapa):
        if renderizar_hitbox: pygame.draw.rect(tela, (254, 254, 0), self.corpo)

    def atualizar(self, tela, mapa, dimensoes_tela):
        self.renderizar(tela, mapa)
        return False

class Vitoria(Estatico):
    def __init__(self, x):
        altura = 190
        y = 590 - altura
        largura = 100
        super().__init__("vitoria", x, y, altura, largura, "0")
    
    def renderizar(self, tela, mapa):
        if renderizar_hitbox: pygame.draw.rect(tela, (254, 254, 0), [self.corpo.x-mapa.campo_visivel.x,self.corpo.y,self.corpo.w,self.corpo.h])

    def atualizar(self, tela, mapa, dimensoes_tela):
        self.renderizar(tela, mapa)
        return False

class Borda(Estatico):
    def __init__(self, nome: str, x: int):
        y = -1000
        altura = 2000
        largura = 1
        super().__init__(nome, x, y, altura, largura, "0")

    def renderizar(self, tela, mapa):
        if renderizar_hitbox: pygame.draw.rect(tela, (0,0,0), self.corpo)