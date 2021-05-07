import pygame
from entidades import Estatico, renderizar_hitbox, renderizar_sprite
from sprites import *

# FUNCOES DE ATUALIZAR NECESSITAM DA AREA VISIVEL PARA RENDERIZAR CORRETAMENTE
class Obstaculo(Estatico):
    def __init__(self, nome:str, x: int, y:int, altura: int, largura: int, arquivo: str, cor:tuple):
        super().__init__(nome, x, y, altura, largura, arquivo ,cor)

class Bloco(Obstaculo):
    def __init__(self, nome: str, x: int, y: int):
        largura = 30
        altura = 30
        super().__init__(nome, x, y, altura, largura, "0",(255, 102, 0))

class Muro(Obstaculo):
    def __init__(self, nome: str, x: int, topo: int, base: int):
        largura = 45
        altura= base-topo
        super().__init__(nome, x, topo, altura, largura, "muro",(11, 137, 0))

class CanoHorizontal(Obstaculo):
    def __init__(self, nome: str, y: int, esquerda: int, direita: int):
        altura = 50
        largura = direita-esquerda
        super().__init__(nome, esquerda, y, altura, largura, "0",(11, 137, 0))

class Chao(Obstaculo):
    def __init__(self, nome: str, y: int, esquerda: int, direita: int):
        altura = 25
        super().__init__(nome, esquerda, y, altura, direita-esquerda, "0",(184, 20, 20))

class Vida(Obstaculo):
    def __init__(self, nome: str, x: int, y: int):
        altura = 30
        largura = 100
        self.__fonte = pygame.font.SysFont('Arial',20)
        self.__vida = ""
        super().__init__(nome, x, y, altura, largura, "0",(10, 237, 0))

    @property
    def vida(self):
        return self.__vida
    
    @vida.setter
    def vida(self, vida):
        self.__vida = vida

    def renderizar(self, tela, mapa):
        if renderizar_hitbox: pygame.draw.rect(tela, self.cor, self.corpo)
    
    def atualizar(self, tela, mapa, dimensoes_tela):
        self.renderizar(tela, mapa)
        mostra_vida = self.__fonte.render('vida :'+" "+str(self.__vida),False,(0,0,0))
        tela.blit(mostra_vida, (self.x, self.y))
        return False

class Tempo(Obstaculo):
    pygame.init()
    def __init__(self, nome: str, x: int, y: int):
        altura = 30
        largura = 70
        self.__fonte = pygame.font.SysFont('Arial',20)
        self.__tempo = 0
        self.__contador = self.__fonte.render('time :'+" "+str(self.tempo),False,(0,0,0))
        super().__init__(nome, x, y, altura, largura, "0",(160, 160, 160))
    @property
    def tempo(self):
        return self.__tempo
    
    @tempo.setter
    def tempo(self, tempo):
        self.__tempo = tempo

    def renderizar(self, tela, mapa):
        if renderizar_hitbox: pygame.draw.rect(tela, self.cor, self.corpo)

    def atualizar(self, tela, mapa, dimensoes_tela):
        self.renderizar(tela, mapa)
        self.__contador = self.__fonte.render('time :'+" "+str(self.__tempo),False,(0,0,0))
        tela.blit(self.__contador, (self.x, self.y))
        return False

class Biscoitos(Obstaculo):
    def __init__(self, nome: str, x: int, y: int):
        altura = 30
        largura = 60
        super().__init__(nome, x, y, altura, largura, "0",(254, 254, 0))

    def renderizar(self, tela, mapa):
        if renderizar_hitbox: pygame.draw.rect(tela,self.cor, self.corpo)

    def atualizar(self, tela, mapa, dimensoes_tela):
        self.renderizar(tela, mapa)
        return False

class Vitoria(Obstaculo):
    def __init__(self, x,y,largura,altura):
        super().__init__("vitoria", x, y, altura, largura, "0",(254, 254, 0))
    
    def atualizar(self, tela, mapa, dimensoes_tela):
        self.renderizar(tela, mapa)
        return False

class Borda(Obstaculo):
    def __init__(self, nome: str, x: int):
        y = -1000
        altura = 2000
        largura = 1
        super().__init__(nome, x, y, altura, largura, "0")