import pygame
from entidades import Estatico

# mudar no UML- Sem parametro
class Bloco(Estatico):
    def __init__(self, nome: str, x: int, y: int):
        largura = 100
        altura = 100
        super().__init__(nome, x, y, largura, altura)

    def atualizar(self, tela):
        pygame.draw.rect(tela, (255, 102, 0), self.corpo)

class Cano_vertical(Estatico):
    def __init__(self, nome: str, x: int, topo: int, base: int):
        largura = 100
        super().__init__(nome, x, topo, base-topo, largura)

    def atualizar(self, tela):
        pygame.draw.rect(tela, (11, 137, 0), self.corpo)

class Cano_horizontal(Estatico):
    def __init__(self, nome: str, y: int, esquerda: int, direita: int):
        largura = 100
        ##O que e esse 100????? aqui nao esta herdando? -Victor
        super().__init__(nome, esquerda, y, 100, direita-esquerda)

    def atualizar(self, tela):
        pygame.draw.rect(tela, (11, 137, 0), self.corpo)


##teste
class Chao(Estatico): 
    def __init__(self, nome: str, y: int, esquerda: int, direita: int):
        largura = 50
        super().__init__(nome, esquerda, y, largura, direita-esquerda)

    def atualizar(self, tela):
        pygame.draw.rect(tela, (184, 20, 20), self.corpo)