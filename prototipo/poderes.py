import pygame
from entidades import *
from obstaculos import *
from inimigos import *

##### PODERES NO JOGADOR #####
class PoderGenerico:
    def __init__(self,tem_tempo: bool, duracao: int, velmax: int, pulo: int, recarga: int):
        self.__tem_tempo = tem_tempo
        self.__duracao = duracao
        self.limite_vel = velmax
        self.pulo = pulo
        self.recarga = recarga
        self.descanso = 0
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
class CinzaDoGuri(PoderGenerico):
    def __init__(self):
        super().__init__(False,0,5,9,0)

    def acao(self, jogador, tela, mapa):
        pass

    def atualizar(self, tela, mapa):
        pass

##### PODER DO DASH #####
class PretoDoNinja(PoderGenerico):
    def __init__(self):
        super().__init__(False, 0,7,10,80)

    def acao(self, jogador, screen, mapa):
        jogador.velx = jogador.face * 23
        self.descanso = self.recarga
        

    def atualizar(self, tela, mapa):
        if self.descanso > 0:
            self.descanso -= 1
        return 0

##### PODER DA BOLA DE FOGO #####
class VermelhoDoMago(PoderGenerico):
    def __init__(self):
        super().__init__(False,0,5,9,40)

    def acao(self, jogador, screen, mapa):
        mapa.lista_de_entidades.append(BolaFogo([jogador.x,jogador.y], screen, mapa, jogador.face))
        self.descanso = self.recarga
        

    def atualizar(self,tela,mapa):
        if self.descanso > 0:
            self.descanso -= 1
        return 0
        # for fogo in self.__bolas:
        #     if fogo.atualizar(tela,campo_visivel):
        #         self.__bolas.remove(fogo)

##### PODER DA INTANGIBILIDADE #####
class AzulDoNerd(PoderGenerico):
    def __init__(self):
        super().__init__(False, 0,5,9,600)
        self.__stamina = 0

    def acao(self, jogador, screen, mapa):
        self.descanso = self.recarga
        self.__stamina = 300  

    def atualizar(self, tela, campo_visivel):
        if self.descanso > 0:
            self.descanso -= 1
        if self.__stamina > 0:
            self.__stamina -= 1
            return True
        else:
            return 0

### PODER DE PARAR O TEMPO ###
class PlatinaEstelar(PoderGenerico):
    def __init__(self):
        super().__init__(False, 300, 5, 9, 600)
        self.__stamina = 0
    
    def acao(self, jogador, screen, mapa):
        mapa.escala_tempo = 0
        self.__stamina = 300
        self.descanso = self.recarga

    def atualizar(self,tela,mapa):
        self.__mapa = mapa
        if self.__stamina > 0:
            self.__stamina -= 1
        if self.__stamina <= 0:
            mapa.escala_tempo = 1
        if self.descanso > 0:
            self.descanso -= 1
        return 0

class FeitoNoCeu(PoderGenerico):
    def __init__(self):
        super().__init__(False, 300, 5, 9, 600)
        self.__stamina = 0

    def acao(self, jogador, screen, mapa):
        self.__stamina = 1

    def atualizar(self,tela,mapa):
        self.__mapa = mapa
        if self.__stamina >= 1:
            mapa.escala_tempo += 0.05
        return 0

##### ITENS DOS PODERES NO MAPA #####
class PoderNoMapa(Movel):
    def __init__(self, nome, x, y, poder_atribuido, imagem):
        largura = 20
        altura = 20
        limite_vel = 4
        self.poder_atribuido = poder_atribuido
        super().__init__(nome, x, y, largura, altura, limite_vel, imagem)

class BandanaDoNinja(PoderNoMapa):
    def __init__(self, nome, x, y):
        super().__init__(nome, x, y, PretoDoNinja(), "0")

    def renderizar(self, tela, mapa):
        if renderizar_hitbox:
            if renderizar_hitbox: pygame.draw.rect(tela, (50, 50, 50),
                    [self.corpo.x - mapa.campo_visivel.x, self.corpo.y, self.corpo.w, self.corpo.h])

class CartolaDoMago(PoderNoMapa):
    def __init__(self, nome, x, y):
        super().__init__(nome, x, y, VermelhoDoMago(), "0")

    def renderizar(self, tela, mapa):
        if renderizar_hitbox:
            if renderizar_hitbox: pygame.draw.rect(tela, (255, 50, 50),
                    [self.corpo.x - mapa.campo_visivel.x, self.corpo.y, self.corpo.w, self.corpo.h])

class OculosDoNerd(PoderNoMapa):
    def __init__(self, nome, x, y):
        super().__init__(nome, x, y, AzulDoNerd(), "0")

    def renderizar(self, tela, mapa):
        if renderizar_hitbox:
            pygame.draw.rect(tela, (50, 50, 255),
                             [self.corpo.x - mapa.campo_visivel.x, self.corpo.y, self.corpo.w, self.corpo.h])

class BoneMarinheiro(PoderNoMapa):
    def __init__(self, nome, x, y):
        super().__init__(nome, x, y, PlatinaEstelar(), "0")
    
    def mover(self, dimensoesTela, mapa):
        pass

    def renderizar(self, tela, mapa):
        if renderizar_hitbox:
            if renderizar_hitbox: pygame.draw.rect(tela, (80, 10, 120),
                    [self.corpo.x - mapa.campo_visivel.x, self.corpo.y, self.corpo.w, self.corpo.h])

class BebeVerde(PoderNoMapa):
    def __init__(self, nome, x, y):
        super().__init__(nome, x, y, FeitoNoCeu(), "0")
    
    def mover(self, dimensoesTela, mapa):
        pass

    def renderizar(self, tela, mapa):
        if renderizar_hitbox:
            if renderizar_hitbox: pygame.draw.rect(tela, (5, 200, 40),
                    [self.corpo.x - mapa.campo_visivel.x, self.corpo.y, self.corpo.w, self.corpo.h])

##### OBJETOS CRIADOS POR PODERES #####
class PoderManifestado(Entidade):
    def __init__(self, nome, x, y, largura, altura, limiteVel, vida, dano_contato, duracao, imagem):
        self.duracao = duracao
        super().__init__(nome, x, y, largura, altura, limiteVel, vida, dano_contato, imagem, [0,0,0,0])

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
        super().__init__("bola de fogo",x,y,largura,altura,limiteVel,vida,dano_contato, duracao, "0")
        self.escala_tempo = 1.0
        self.mapa = mapa
        self.vely = -1
        self.velx = 6 * vel

    def mover(self, dimensoesTela, mapa):

        ##### COLISOES #####

        # 0-Cima, 1-Baixo, 2-Direita, 3-Esquerda
        obstaculos = self.checar_colisao(mapa.lista_de_entidades, [BolaFogo, CartolaDoMago, BandanaDoNinja])

        for i in range(len(obstaculos)):
            if isinstance(obstaculos[i], Rato):
                obstaculos[i].auto_destruir(mapa)
                self.auto_destruir(mapa)

        ##### HORIZONTAIS #####
        if obstaculos[3] or obstaculos[2]:
            #self.duracao = 0
            self.velx = -self.velx

        ##### VERTICAIS #####
        if obstaculos[1] or obstaculos[0]:
            self.vely = -max(self.vely*4/5,8)
            #self.y = obsBaixo.corpo.top - self.altura'''
        if not obstaculos[1]: self.vely += gravidade*7*self.escala_tempo

        self.y += self.vely*self.escala_tempo
        self.x += self.velx*self.escala_tempo

    def renderizar(self, tela, mapa):
        pygame.draw.rect(tela, [245, min(87 + self.duracao,255), 65],[self.corpo.x - mapa.campo_visivel.x, self.corpo.y, self.corpo.w, self.corpo.h])

    def atualizar(self, tela, mapa, dimensoes_tela):
        if self.escala_tempo != mapa.escala_tempo:
            self.escala_tempo += max(min(mapa.escala_tempo-self.escala_tempo,0.05),-0.05)
        self.corpo = pygame.Rect(self.x, self.y, self.largura, self.altura)
        if (self.duracao >  0):
            self.mover(dimensoes_tela, mapa)
            self.renderizar(tela, mapa)
            self.duracao -= 1*self.escala_tempo
            return False
        return True