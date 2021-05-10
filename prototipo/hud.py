from entidades import *
import pygame

class Hud:
    def __init__(self):
        self.__vida = Vida(60,30)
        self.__tempo = Tempo(220,30)
        self.__biscoitos = []
        self.__barra_poder = BarraPoder(700,50)
        self.__paleta = []

    def atualizar(self, tela, mapa, dimensoes_tela, tempo, vida):
        self.__vida.atualizar(tela, mapa, dimensoes_tela, vida)
        self.__tempo.atualizar(tela, mapa, dimensoes_tela, tempo)
        self.__barra_poder.atualizar(tela, mapa, dimensoes_tela)


class Vida(Estatico):
    def __init__(self, x: int, y: int):
        altura = 30
        largura = 100
        self.__fonte = pygame.font.SysFont('Arial', 20)
        self.__vida = ""
        super().__init__("vida", x, y, altura, largura, "sprites", (10, 237, 0))

    def renderizar(self, tela, mapa):
        nome = self.nome+"_"+str(self.__vida)
        self.sprite.imprimir(tela, nome, self.x, self.y, 0, 0, 0, 0)

    def atualizar(self, tela, mapa, dimensoes_tela, vida):
        self.__vida = vida
        self.renderizar(tela, mapa)
        return False


class Tempo(Estatico):
    pygame.init()

    def __init__(self, x: int, y: int):
        altura = 30
        largura = 70
        self.tempomax = 320
        self.__fonte = pygame.font.SysFont('Arial', 40)
        self.__tempo = 0
        self.__contador = self.__fonte.render('time :' + " " + str(self.__tempo), False, (0, 0, 0))
        super().__init__("tempo", x, y, altura, largura, "sprites", (160, 160, 160))

    def renderizar(self, tela, mapa):
        #print(self.__tempo, self.tempomax)
        if type(self.__tempo) == int  :
            nome = "tempo_"+str(int(self.__tempo/max((self.tempomax/5),1)))
        else:
            nome = "tempo_"
        self.sprite.imprimir(tela, nome, self.x, self.y, 0, 0, 0, 0)

    def atualizar(self, tela, mapa, dimensoes_tela, tempo):
        self.__tempo = tempo
        self.renderizar(tela, mapa)
        self.__contador = self.__fonte.render(str(self.__tempo), False, (0, 0, 0))
        tela.blit(self.__contador, (self.x+70, self.y+35))
        return False


class Biscoitos(Estatico):
    def __init__(self, nome: str, x: int, y: int):
        altura = 30
        largura = 60
        super().__init__(nome, x, y, altura, largura, "0", (254, 254, 0))

    def renderizar(self, tela, mapa):
        if renderizar_hitbox: pygame.draw.rect(tela, self.cor, self.corpo)

    def atualizar(self, tela, mapa, dimensoes_tela):
        self.renderizar(tela, mapa)
        return False


class BarraPoder(Estatico):
    def __init__(self, x: int, y: int):
        altura = 40
        largura = 188
        self.__largura_atual = largura
        self.__cor_poder = (0, 0, 0)
        self.__corpo_poder = []
        super().__init__("poder_barra", x, y, altura, largura, "sprites", (205, 133, 63))
        #self.sprite = SpriteSheetBarras()

    def atualizar(self, tela, mapa, dimensoes_tela):
        self.__cor_poder = mapa.jogador.poder.cor
        self.__largura_atual = (abs(mapa.jogador.poder.descanso - mapa.jogador.poder.recarga))/mapa.jogador.poder.recarga * self.largura
        self.__corpo_poder = pygame.Rect(self.x, self.y, self.__largura_atual, self.altura)
        self.renderizar(tela, mapa)
        return False

    def renderizar(self, tela, mapa):
        pygame.draw.rect(tela, self.cor, self.corpo)
        pygame.draw.rect(tela, self.__cor_poder, self.__corpo_poder)
        nome = self.nome+"_"+mapa.jogador.poder.nome
        self.sprite.imprimir(tela, nome, self.x-70, self.y-18, 0, 0, 0, 0)


class Paleta(Estatico):
    def __init__(self, x: int, y: int):
        altura = 40
        largura = 40
        self.__largura_atual = largura
        self.__coletadas = 0
        super().__init__("paletas", x, y, altura, largura, "0", (205, 133, 63))
        #self.sprite = SpriteSheetBarras()

    def atualizar(self, tela, mapa, dimensoes_tela):
        self.__coletadas = mapa.jogador.paleta
        return False