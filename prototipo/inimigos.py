#Arquivo destinado a fazer todos os inimigos
import pygame
from entidades import Entidade, gravidade, renderizar_hitbox, renderizar_sprite
from poderes import *

class Rato(Entidade):
    def __init__(self, nome: str, x: int, y: int):
        vida = 1
        danoContato = 50
        largura = 46
        altura = 46
        limiteVel = 4
        contatos = ['dano', 'morrer', 'dano', 'dano']
        super().__init__(nome, x, y, largura, altura, limiteVel, vida, danoContato, "0", contatos,(88, 51, 0))
        self.vely = 0
        self.velx = 1
        self.xinicial = x
        self.escala_tempo = 1

    def mover(self, dimensoesTela, mapa):

        ##### COLISOES #####
        obsCima, obsBaixo, obsDireita, obsEsquerda = self.checar_colisao(mapa.lista_de_entidades,[])

        ##### HORIZONTAIS #####
        if obsEsquerda or obsDireita:
            self.velx = self.velx * -1

        ##### VERTICAIS #####
        if obsBaixo:
            self.vely = 0
            self.y = obsBaixo.corpo.top - self.altura

        ##### GRAVIDADE ######
        if not obsBaixo: self.vely += gravidade * self.escala_tempo

        self.y += self.vely * self.escala_tempo
        self.x += self.velx * self.escala_tempo

class Voador(Entidade):
    def __init__(self, nome: str, x: int, y: int,altitude: int):
        vida = 1
        danoContato = 50
        largura = 26
        altura = 26
        limiteVel = 4
        contatos = ['dano', 'morrer', 'dano', 'dano']
        super().__init__(nome, x, y, largura, altura, limiteVel, vida, danoContato, "0", contatos,(88, 51, 0))
        self.altitude = pygame.Rect(x,y+largura+2,largura,altura+altitude) # CAMPO UTILIZADO PARA CHECAR ALTURA DE VOO
        self.vely = 0
        self.velx = 1
        self.xinicial = x
        self.escala_tempo = 1
        

    def mover(self, dimensoesTela, mapa):

        ##### COLISOES #####
        obsCima, obsBaixo, obsDireita, obsEsquerda = self.checar_colisao(mapa.lista_de_entidades, [CartolaDoMago, BandanaDoNinja, OculosDoNerd, BoneMarinheiro, VerdeBebe])

        ##### HORIZONTAIS #####
        if obsEsquerda or obsDireita:
            self.velx = self.velx * -1

        ##### VERTICAIS #####
        if obsBaixo or obsCima:
            self.vely = -self.vely
            '''if self.y < 100: 
                self.y = obsBaixo.corpo.top - self.altura'''


        ##### GRAVIDADE ######
        if (self.altitude.collidelist([x.corpo for x in mapa.lista_de_entidades if x != self]) != -1
            or self.altitude.y+self.altitude.h > dimensoesTela[1]):
            self.vely -= gravidade * self.escala_tempo * 0.2
        else:
            self.vely += gravidade * self.escala_tempo * 0.2

        if self.vely < -1:
            self.vely = -1
        self.y += self.vely * self.escala_tempo
        self.x += self.velx * self.escala_tempo
        self.altitude.x = self.x
        self.altitude.y = self.y + self.largura + 2
        

       
class Atirador(Entidade):
    def __init__(self, nome: str, x: int, y: int):
        vida = 1
        danoContato = 10
        largura = 40
        altura = 66
        limiteVel = 4
        contatos = ['dano', 'morrer', 'dano', 'dano']
        super().__init__(nome, x, y, largura, altura, limiteVel, vida, danoContato, "0", contatos)
        self.vely = 0
        self.velx = 1
        self.xinicial = x
        self.escala_tempo = 1
        self.__poder = Projetil()
        self.__descanso_poder = 300
        self.__face = 1

    @property
    def face(self):
        return self.__face

    def atualizar(self, tela, mapa, dimensoes_tela):
        if self.escala_tempo != mapa.escala_tempo:
            self.escala_tempo += max(min(mapa.escala_tempo-self.escala_tempo,0.05),-0.05)
        self.mover(dimensoes_tela, mapa)
        self.corpo = pygame.Rect(self.x, self.y, self.largura, self.altura)
        if mapa.campo_visivel.colliderect(self.corpo):
            self.renderizar(tela, mapa)
        
        if self.__descanso_poder == 0:
            self.__poder.acao(self,tela, mapa)
            self.__descanso_poder = 300
        else:
            self.__descanso_poder -= 1
        return False

    def mover(self, dimensoesTela, mapa):
        ##### COLISOES #####
        obsCima, obsBaixo, obsDireita, obsEsquerda = self.checar_colisao(mapa.lista_de_entidades,[])

        ##### HORIZONTAIS #####
        if obsEsquerda or obsDireita:
            self.velx = self.velx * -1

        ##### VERTICAIS #####
        if obsBaixo:
            self.vely = 0
            self.y = obsBaixo.corpo.top - self.altura

        ##### GRAVIDADE ######
        if not obsBaixo: self.vely += gravidade * self.escala_tempo

        self.y += self.vely * self.escala_tempo
        self.x += self.velx * self.escala_tempo

        if self.corpo.colliderect(mapa.campo_visivel):
            self.velx = 0
            dist_x_jogador = self.x - mapa.jogador.x
            if dist_x_jogador > 0:
                self.__face = -1
            elif dist_x_jogador < 0:
                self.__face = 1