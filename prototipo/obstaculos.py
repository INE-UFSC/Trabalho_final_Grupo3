import pygame
from entidades import *
from sprites import *

lista_obstaculos = {"obstaculos",}


# FUNCOES DE ATUALIZAR NECESSITAM DA AREA VISIVEL PARA RENDERIZAR CORRETAMENTE
class Obstaculo(Estatico):
    def __init__(self, nome: str, x: int, y: int, altura: int, largura: int, arquivo: str, cor: tuple):
        super().__init__(nome, x, y, altura, largura, arquivo, cor)


@instanciavel
class Bloco(Obstaculo):
    def __init__(self, nome: str, x: int, y: int):
        lista_obstaculos.add(Bloco)
        largura = 30
        altura = 30
        super().__init__(nome, x, y, altura, largura, "0", (255, 102, 0))


@instanciavel
class Muro(Obstaculo):
    def __init__(self, nome: str, x: int, topo: int, base: int):
        largura = 45
        altura = base - topo
        super().__init__(nome, x, topo, altura, largura, "muro", (11, 137, 0))


@instanciavel
class Cano(Obstaculo):
    def __init__(self, nome: str, y: int, esquerda: int, direita: int):
        altura = 50
        largura = direita - esquerda
        super().__init__(nome, esquerda, y, altura, largura, "0", (11, 137, 0))


@instanciavel
class Chao(Obstaculo):
    def __init__(self, nome: str, y: int, esquerda: int, direita: int):
        altura = 25
        super().__init__(nome, esquerda, y, altura, direita - esquerda, "0", (184, 20, 20))


@instanciavel
class Vida(Obstaculo):
    def __init__(self, nome: str, x: int, y: int):
        altura = 30
        largura = 100
        self.__fonte = pygame.font.SysFont('Arial', 20)
        self.__vida = ""
        super().__init__(nome, x, y, altura, largura, "0", (10, 237, 0))

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
        mostra_vida = self.__fonte.render('vida :' + " " + str(self.__vida), False, (0, 0, 0))
        tela.blit(mostra_vida, (self.x, self.y))
        return False


@instanciavel
class Tempo(Obstaculo):
    pygame.init()

    def __init__(self, nome: str, x: int, y: int):
        altura = 30
        largura = 70
        self.__fonte = pygame.font.SysFont('Arial', 20)
        self.__tempo = 0
        self.__contador = self.__fonte.render('time :' + " " + str(self.tempo), False, (0, 0, 0))
        super().__init__(nome, x, y, altura, largura, "0", (160, 160, 160))

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
        self.__contador = self.__fonte.render('time :' + " " + str(self.__tempo), False, (0, 0, 0))
        tela.blit(self.__contador, (self.x, self.y))
        return False


@instanciavel
class Biscoitos(Obstaculo):
    def __init__(self, nome: str, x: int, y: int):
        altura = 30
        largura = 60
        super().__init__(nome, x, y, altura, largura, "0", (254, 254, 0))

    def renderizar(self, tela, mapa):
        if renderizar_hitbox: pygame.draw.rect(tela, self.cor, self.corpo)

    def atualizar(self, tela, mapa, dimensoes_tela):
        self.renderizar(tela, mapa)
        return False


@instanciavel
class Vitoria(Obstaculo):
    def __init__(self, x: int, y: int, largura: int, altura: int):
        super().__init__("vitoria", x, y, altura, largura, "0", (254, 254, 0))

    def atualizar(self, tela, mapa, dimensoes_tela):
        self.renderizar(tela, mapa)
        return False


@instanciavel
class Borda(Obstaculo):
    def __init__(self, nome: str, x: int):
        y = -1000
        altura = 2000
        largura = 1
        super().__init__(nome, x, y, altura, largura, "0", (0, 0, 0))

@instanciavel
class BarraPoder(Obstaculo):
    def __init__(self, x: int, y: int):
        altura = 40
        largura = 188
        self.__largura_atual = largura
        self.__cor_poder = (0, 0, 0)
        self.__corpo_poder = []
        super().__init__("barrapoder", x, y, altura, largura, "0", (205, 133, 63))
        self.sprite = SpriteSheetBarras()

    def atualizar(self, tela, mapa, dimensoes_tela):
        self.__cor_poder = mapa.jogador.poder.cor
        self.__largura_atual = (abs(mapa.jogador.poder.descanso - mapa.jogador.poder.recarga))/mapa.jogador.poder.recarga * self.largura
        self.__corpo_poder = pygame.Rect(self.x, self.y, self.__largura_atual, self.altura)
        self.renderizar(tela, mapa)
        return False

    def renderizar(self, tela, mapa):
        pygame.draw.rect(tela, self.cor, self.corpo)
        pygame.draw.rect(tela, self.__cor_poder, self.__corpo_poder)
        self.sprite.imprimir(tela, self.x-70, self.y-18, mapa.jogador.poder.nome)
        #self.sprite.imprimir(self.imagem, self.x-40, self.y-6, tela, 0, 0)
       # except AttributeError:
        #    pass