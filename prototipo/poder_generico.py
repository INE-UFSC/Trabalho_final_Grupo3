import mapa
import pygame
from entidades import *

class Poder_Generico:
    def __init__(self,tem_tempo: bool, duracao: int):
        self.__tem_tempo = tem_tempo
        self.__duracao = duracao 
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
    
    def atirar(self, jogador, screen, mapa):   ### ERA PRA SER ABSTRATO MAS FDS
        pass

class VermelhoDoMago(Poder_Generico):
    def __init__(self):
        super().__init__(False,0)

    def atirar(self, jogador, screen, mapa):
        mapa.lista_de_entidades.append(BolaFogo([jogador.x,jogador.y], screen, mapa, jogador.face))

    def atualizar(self,tela,campo_visivel):
        pass
        # for fogo in self.__bolas:
        #     if fogo.atualizar(tela,campo_visivel):
        #         self.__bolas.remove(fogo)

class BolaFogo(Entidade):
    def __init__(self, pos_inicial , screen, mapa, vel):
        vida = 1
        largura = 15
        altura = 15
        limiteVel = 3 * vel
        dano_contato = 0
        x = pos_inicial[0] + 25 * vel
        y = pos_inicial[1]
        #self.__corpo = pygame.Rect(self.x, self.y, self.largura, self.altura)
        super().__init__("bola de fogo",x,y,largura,altura,limiteVel,vida,dano_contato)
        self.duracao = 100
        self.mapa = mapa
        self.vely = 0
        self.velx = 3 * vel

    def mover(self, dimensoesTela, mapa):

        ##### COLISOES #####
        colisaoCima, colisaoBaixo, colisaoEsquerda, colisaoDireita = False, False, False, False
        cCima, cBaixo, cEsquerda, cDireita = False, False, False, False
        obsBaixo, obsCima, obsEsquerda, obsDireita = 0,0,0,0

        ##### COLISOES COM OBSTACULOS #####
        
        for obstaculo in self.mapa.lista_de_entidades:

            cCima, cBaixo, cDireita, cEsquerda = self.checar_colisao(obstaculo.corpo)
            #print(f'{cDireita}')

            # Essa checagem em dois passos tem que ocorrer por que se nao ele so salva a colisao com o utlimo obstaculo
            ## Inutil enquanto a bola so vai reto e so 
            '''if cCima:
                colisaoCima = True
                obsCima = obstaculo
            if cBaixo:
                colisaoBaixo = True
                obsBaixo = obstaculo'''
            if cEsquerda:
                colisaoEsquerda = True
                obsEsquerda = obstaculo
            if cDireita:
                colisaoDireita = True
                obsDireta = obstaculo
                print('ENTROU NA 109')
            

        ##### HORIZONTAIS #####
        if colisaoEsquerda or colisaoDireita:
            self.duracao = 0
            #self.velx = 0

        ##### VERTICAIS #####
        '''if colisaoBaixo:
            self.vely = 0
            #self.y = obsBaixo.corpo.top - self.altura'''

        self.y += self.vely
        self.x += self.velx

    def renderizar(self, tela, mapa):
        pygame.draw.rect(tela, [245, 87 + self.duracao, 65],[self.corpo.x - mapa.campo_visivel.x - 50, self.corpo.y, self.corpo.w, self.corpo.h])

    def atualizar(self, tela, mapa, dimensoes_tela):
        self.corpo = pygame.Rect(self.x, self.y, self.largura, self.altura)
        if (self.duracao >  0):
            self.mover(dimensoes_tela, mapa)
            self.renderizar(tela, mapa)
            self.duracao -= 1
            return False
        return True