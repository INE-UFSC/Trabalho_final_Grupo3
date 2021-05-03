import mapa
import pygame
from entidades import *

class PoderGenerico:
    def __init__(self,tem_tempo: bool, duracao: int, velmax: int, pulo: int):
        self.__tem_tempo = tem_tempo
        self.__duracao = duracao
        self.velmax = velmax
        self.pulo = pulo
        'self.__nome_funcionalidade = nome_funcionalidade'

    @property
    def tem_tempo (self):
        return self.__tem_tempo
    
    @tem_tempo.setter
    def tem_tempo (self, tem_tempo):
        self.__tem_tempo = tem_tempo
    
    @property
    def duracao (self):
        return self.__duracao
    
    @duracao.setter
    def duracao (self, duracao):
        self.__duracao = duracao
    '''@property
    def nome_funcionalidade (self):
        return self.__nome_funcionalidade
    
    @nome_funcionalidade.setter
    def nome_funcionalidade (self, nome_funcionalidade):
        self.__nome_funcionalidade = nome_funcionalidade'''
    
    def acao(self, jogador, screen, mapa):   ### ERA PRA SER ABSTRATO MAS FDS
        pass

##### FORMA PADRAO DO JOGADOR #####
class FormaPadrao(PoderGenerico):
    def __init__(self):
        super().__init__(False,0,5,9)

    def acao(self, jogador, tela, mapa):
        pass

##### PODER DO DASH #####
class PretoDoNinja(PoderGenerico):
    def __init__(self):
        super().__init__(False, 0,8,10)
        self.boost = 30

    def acao(self, jogador, screen, mapa):
        #jogador.velocidade_max =
        jogador.velx = 20
        pass

    def atualizar(self, tela, campo_visivel):
        pass

class VermelhoDoMago(PoderGenerico):
    def __init__(self):
        super().__init__(False,0,5,9)

    def acao(self, jogador, screen, mapa):
        mapa.lista_de_entidades.append(BolaFogo([jogador.x,jogador.y], screen, mapa, jogador.face))

    def atualizar(self,tela,campo_visivel):
        pass
        # for fogo in self.__bolas:
        #     if fogo.atualizar(tela,campo_visivel):
        #         self.__bolas.remove(fogo)

class PoderManifestado(Entidade):
    def __init__(self, nome, x, y, largura, altura, limiteVel, vida, dano_contato, duracao):
        self.duracao = duracao
        super().__init__(nome, x, y, largura, altura, limiteVel, vida, dano_contato)

class BolaFogo(PoderManifestado):
    def __init__(self, pos_inicial , screen, mapa, vel):
        x = pos_inicial[0] + 25 * vel
        y = pos_inicial[1]
        largura = 15
        altura = 15
        vida = 1
        limiteVel = 3 * vel
        dano_contato = 0
        duracao = 500
        #self.__corpo = pygame.Rect(self.x, self.y, self.largura, self.altura)
        super().__init__("bola de fogo",x,y,largura,altura,limiteVel,vida,dano_contato, duracao)
        self.mapa = mapa
        self.vely = -1
        self.velx = 6 * vel

    def mover(self, dimensoesTela, mapa):

        ##### COLISOES #####
        obsCima, obsBaixo, obsDireita, obsEsquerda = self.checar_colisao(mapa.lista_de_entidades, [BolaFogo])
            

        ##### HORIZONTAIS #####
        if obsEsquerda or obsDireita:
            #self.duracao = 0
            self.velx = -self.velx

        ##### VERTICAIS #####
        if obsBaixo or obsCima:
            self.vely = -max(self.vely*4/5,8)
            #self.y = obsBaixo.corpo.top - self.altura'''

        if not obsBaixo: self.vely += gravidade*7

        #print(colisaoBaixo, obsBaixo)

        self.y += self.vely
        self.x += self.velx

    def renderizar(self, tela, mapa):
        pygame.draw.rect(tela, [245, min(87 + self.duracao,255), 65],[self.corpo.x - mapa.campo_visivel.x, self.corpo.y, self.corpo.w, self.corpo.h])

    def atualizar(self, tela, mapa, dimensoes_tela):
        self.corpo = pygame.Rect(self.x, self.y, self.largura, self.altura)
        if (self.duracao >  0):
            self.mover(dimensoes_tela, mapa)
            self.renderizar(tela, mapa)
            self.duracao -= 1
            return False
        return True