import pygame
import math
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

##### PODER DE PARAR O TEMPO #####
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

#### PODER DO INIMIGO ####
class Projetil(PoderGenerico):
    def __init__(self):
        super().__init__(False,0,5,9,40)

    def acao(self, jogador, screen, mapa, velx, vely):
        if jogador.face == 1:
            mapa.lista_de_entidades.append(Bala([jogador.corpo.right,jogador.y], screen, mapa, jogador.face, velx, vely))
        elif jogador.face == -1:
            mapa.lista_de_entidades.append(Bala([jogador.x,jogador.y], screen, mapa, jogador.face, velx, vely))
        self.descanso = self.recarga
        

    def atualizar(self,tela,mapa):
        if self.descanso > 0:
            self.descanso -= 1

##### PODER DE ACELERAR O TEMPO #####
class FeitoNoCeu(PoderGenerico):
    def __init__(self):
        super().__init__(False, 300, 5, 9, 600)
        self.__stamina = 0

    def acao(self, jogador, screen, mapa):
        self.__stamina = 1

    def atualizar(self,tela,mapa):
        self.__mapa = mapa
        if self.__stamina >= 1:
            mapa.escala_tempo += 0.05 * (math.log(mapa.escala_tempo,2)+1)
        return 0

    

##### ITENS DOS PODERES NO MAPA #####

class Coletavel(Movel):
    def __init__(self, nome, x, y, imagem,cor=(0,0,0)):
        largura = 20
        altura = 20
        limite_vel = 4
        super().__init__(nome, x, y, largura, altura, limite_vel, imagem,cor)
    
    def coleta(self, jogador, mapa):
        pass

class BiscoitoNoMapa(Coletavel):
    def __init__(self, nome, x, y, imagem,cor=(0,0,0)):
        super().__init__(nome, x, y, imagem, cor)
    
    def coleta(self, jogador, mapa):
        jogador.coletar_moeda(self)
        mapa.escala_tempo = 1
        self.auto_destruir(mapa)

class PoderNoMapa(Coletavel):
    def __init__(self, nome, x, y, poder_atribuido, imagem,cor=(0,0,0)):
        self.poder_atribuido = poder_atribuido
        super().__init__(nome, x, y, imagem,cor)
    
    def coleta(self, jogador, mapa):
        jogador.coletar_poder(self)
        mapa.escala_tempo = 1
        self.auto_destruir(mapa)

    def sofreu_colisao_outros(self, entidade, direcao):
        return 0

    def sofreu_colisao_jogador(self, jogador, direcao, mapa):
        return 0


class BandanaDoNinja(PoderNoMapa):
    def __init__(self, nome, x, y):
        super().__init__(nome, x, y, PretoDoNinja(), "0",(50, 50, 50))


class CartolaDoMago(PoderNoMapa):
    def __init__(self, nome, x, y):
        super().__init__(nome, x, y, VermelhoDoMago(), "0",(255, 50, 50))


class OculosDoNerd(PoderNoMapa):
    def __init__(self, nome, x, y):
        super().__init__(nome, x, y, AzulDoNerd(), "0",(50, 50, 255))


class BoneMarinheiro(PoderNoMapa):
    def __init__(self, nome, x, y):
        super().__init__(nome, x, y, PlatinaEstelar(), "0",(80, 10, 120))


class VerdeBebe(PoderNoMapa):
    def __init__(self, nome, x, y):
        super().__init__(nome, x, y, FeitoNoCeu(), "0",(5, 200, 40))


##### OBJETOS CRIADOS POR PODERES #####

class PoderManifestado(Entidade):
    def __init__(self, nome, x, y, largura, altura, limiteVel, vida, dano_contato, duracao, imagem,cor=(0,0,0)):
        self.duracao = duracao
        super().__init__(nome, x, y, largura, altura, limiteVel, vida, dano_contato, imagem,cor)

class PoderManifestadoInimigo(Entidade):
    def __init__(self, nome, x, y, largura, altura, limiteVel, vida, dano_contato, duracao, imagem, cor=(0,0,0)):
        self.duracao = duracao
        super().__init__(nome, x, y, largura, altura, limiteVel, vida, dano_contato, imagem, cor)

    def sofreu_colisao_jogador(self, jogador, direcao, mapa):
        self.auto_destruir(mapa)
        return self.dano_contato

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
        obstaculos = self.checar_colisao(mapa.lista_de_entidades, [BolaFogo, PoderNoMapa])

        for i in range(len(obstaculos)):
            if isinstance(obstaculos[i], Entidade):
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
        pygame.draw.rect(tela, [245, min(87 + self.duracao,255), 65],[self.corpo.x - mapa.campo_visivel.x, 
                                                                      self.corpo.y - mapa.campo_visivel.y, 
                                                                      self.corpo.w, 
                                                                      self.corpo.h])

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

class Bala(PoderManifestadoInimigo):
    def __init__(self, pos_inicial , screen, mapa, lado, velx, vely):
        x = pos_inicial[0] + 25 * lado
        largura = 15
        altura = 15
        y = pos_inicial[1] + altura
        vida = 1
        limiteVel = 300
        dano_contato = 50
        duracao = 500
        contatos = ['dano', 'dano', 'dano', 'dano']
        #self.__corpo = pygame.Rect(self.x, self.y, self.largura, self.altura)
        super().__init__("bala",x,y,largura,altura,limiteVel,vida,dano_contato, duracao, "0", contatos)
        self.escala_tempo = 1.0
        self.mapa = mapa
        self.vely = vely
        self.velx = velx

    def mover(self, dimensoesTela, mapa):
        
        #### SE MOVE ####
        self.y += self.vely*self.escala_tempo
        self.x += self.velx*self.escala_tempo

    def renderizar(self, tela, mapa):
        pygame.draw.rect(tela, [245, min(87 + self.duracao,255), 65],[self.corpo.x - mapa.campo_visivel.x, 
                                                                      self.corpo.y - mapa.campo_visivel.y, 
                                                                      self.corpo.w, 
                                                                      self.corpo.h])

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