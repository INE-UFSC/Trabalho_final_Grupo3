import pygame
from entidades import *
from inimigos import *

##### PODERES NO JOGADOR #####
class PoderGenerico:
    def __init__(self,tem_tempo: bool, duracao: int, velmax: int, pulo: int, recarga: int):
        self.__tem_tempo = tem_tempo
        self.__duracao = duracao
        self.limite_vel = velmax
        self.pulo = pulo
        self.recarga = recarga
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

    def atualizar(self, tela, campo_visivel):
        pass

##### PODER DO DASH #####
class PretoDoNinja(PoderGenerico):
    def __init__(self):
        super().__init__(False, 0,7,10,60)
        self.boost = 30

    def acao(self, jogador, screen, mapa):
        jogador.velx = jogador.face * 20
        pass

    def atualizar(self, tela, campo_visivel):
        pass

##### PODER DA BOLA DE FOGO #####
class VermelhoDoMago(PoderGenerico):
    def __init__(self):
        super().__init__(False,0,5,9,30)

    def acao(self, jogador, screen, mapa):
        mapa.lista_de_entidades.append(BolaFogo([jogador.x,jogador.y], screen, mapa, jogador.face))

    def atualizar(self,tela,campo_visivel):
        pass
        # for fogo in self.__bolas:
        #     if fogo.atualizar(tela,campo_visivel):
        #         self.__bolas.remove(fogo)


##### ITENS DOS PODERES NO MAPA #####
class PoderNoMapa(Movel):
    def __init__(self, nome, x, y, poder_atribuido):
        largura = 20
        altura = 20
        limite_vel = 4
        self.poder_atribuido = poder_atribuido
        super().__init__(nome, x, y, largura, altura, limite_vel)

class ShurikenDoNinja(PoderNoMapa):
    def __init__(self, nome, x, y):
        super().__init__(nome, x, y, PretoDoNinja())

    def mover(self, dimensoesTela, mapa):
        pass

    def renderizar(self, tela, mapa):
        if renderizar_hitbox:
            if renderizar_hitbox: pygame.draw.rect(tela, (50, 50, 50),
                    [self.corpo.x - mapa.campo_visivel.x, self.corpo.y, self.corpo.w, self.corpo.h])

class OrbeDoMago(PoderNoMapa):
    def __init__(self, nome, x, y):
        super().__init__(nome, x, y, VermelhoDoMago())

    def mover(self, dimensoesTela, mapa):
        pass

    def renderizar(self, tela, mapa):
        if renderizar_hitbox:
            if renderizar_hitbox: pygame.draw.rect(tela, (255, 50, 50),
                    [self.corpo.x - mapa.campo_visivel.x, self.corpo.y, self.corpo.w, self.corpo.h])

##### OBJETOS CRIADOS POR PODERES #####
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

        # 0-Cima, 1-Baixo, 2-Direita, 3-Esquerda
        obstaculos = self.checar_colisao(mapa.lista_de_entidades, [BolaFogo])

        for i in range(len(obstaculos)):
            if isinstance(obstaculos[i], Goomba):
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

        if not obstaculos[1]: self.vely += gravidade*7

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