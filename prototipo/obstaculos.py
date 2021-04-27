import pygame
from entidades import Estatico

# mudar no UML- Sem parametro
class Bloco(Estatico):
    def __init__(self, nome: str, x: int, y: int):
        largura = 30
        altura = 30
        super().__init__(nome, x, y, altura, largura)

    def atualizar(self, tela, mapa):
        pygame.draw.rect(tela, (255, 102, 0), [self.corpo.x-mapa.campo_visivel.x-50,self.corpo.y,self.corpo.w,self.corpo.h])

class CanoVertical(Estatico):
    def __init__(self, nome: str, x: int, topo: int, base: int):
        largura = 50
        altura= base-topo
        super().__init__(nome, x, topo, altura, largura)

    def atualizar(self, tela, mapa):
        pygame.draw.rect(tela, (11, 137, 0), [self.corpo.x-mapa.campo_visivel.x-50,self.corpo.y,self.corpo.w,self.corpo.h])

class CanoHorizontal(Estatico):
    def __init__(self, nome: str, y: int, esquerda: int, direita: int):
        altura = 50
        largura = direita-esquerda
        super().__init__(nome, esquerda, y, altura, largura)

    def atualizar(self, tela, mapa):
        pygame.draw.rect(tela, (11, 137, 0), [self.corpo.x-mapa.campo_visivel.x-50,self.corpo.y,self.corpo.w,self.corpo.h])

class Chao(Estatico): 
    def __init__(self, nome: str, y: int, esquerda: int, direita: int):
        altura = 10
        super().__init__(nome, esquerda, y, altura, direita-esquerda)

    def atualizar(self, tela, mapa):
        pygame.draw.rect(tela, (184, 20, 20), [self.corpo.x-mapa.campo_visivel.x-50,self.corpo.y,self.corpo.w,self.corpo.h])

class Vida(Estatico):
    def __init__(self, nome: str, x: int, y: int):
        altura = 30
        largura = 60
        super().__init__(nome, x, y, altura, largura)

    def atualizar(self, tela,mapa):
        pygame.draw.rect(tela, (10, 237, 0), self.corpo)

class Tempo(Estatico):
    def __init__(self, nome: str, x: int, y: int):
        altura = 30
        largura = 60
        super().__init__(nome, x, y, altura, largura)

    def atualizar(self, tela,mapa):
        pygame.draw.rect(tela, (160, 160, 160), self.corpo)

class Moeda(Estatico):
    def __init__(self, nome: str, x: int, y: int):
        altura = 30
        largura = 60
        super().__init__(nome, x, y, altura, largura)

    def atualizar(self, tela,mapa):
        pygame.draw.rect(tela, (254, 254, 0), self.corpo)