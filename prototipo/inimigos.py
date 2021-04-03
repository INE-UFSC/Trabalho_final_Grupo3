#Arquivo destinado a fazer todos os inimigos
import pygame
from entidades import Entidade

class Goomba(Entidade):
    def __init__(self, nome: str, x: int, y: int):
        vida = 1
        danoContato = 1
        largura = 20
        altura = 20
        limiteVel = 4
        super().__init__(nome, x, y, largura, altura, limiteVel, vida, danoContato)
        self.vely = 0
        self.velx = 1
        self.xinicial = x

    def checar_colisao(self, corpo):
        colisaoBaixo, colisaoCima, colisaoEsquerda, colisaoDireita = False, False, False, False
        corpoLargo = pygame.Rect(self.x-1, self.y-1, self.largura+2,self.altura+2)
        colisaoAjustada = corpoLargo.colliderect(corpo)
        if colisaoAjustada:
            ##### VERTICAIS #####
            if self.corpo.left in range(corpo.left+1, corpo.right-1) or self.corpo.right in range(corpo.left+1, corpo.right-1):
                if corpoLargo.bottom >= corpo.top and self.vely >= 0:
                    colisaoBaixo = True
                elif corpoLargo.top <= corpo.bottom and self.vely <= 0:
                    colisaoCima = True
            ##### HORIZONTAIS #####
            if (self.corpo.top in range(corpo.top+1, corpo.bottom-1) or self.corpo.bottom in range(corpo.top+1, corpo.bottom-1))\
                    and (not colisaoCima and not colisaoBaixo):
                if corpoLargo.right >= corpo.left and self.velx >= 0:
                    colisaoDireita = True
                if corpoLargo.left <= corpo.right and self.velx <= 0:
                    colisaoEsquerda = True
        return [colisaoCima, colisaoBaixo, colisaoDireita, colisaoEsquerda]

    def mover(self, dimensoesTela, mapa):

        ##### COLISOES #####
        colisaoCima, colisaoBaixo, colisaoEsquerda, colisaoDireita = False, False, False, False
        cCima, cBaixo, cEsquerda, cDireita = False, False, False, False

        ##### COLISAO COM O CHAO #####
        if self.corpo.bottom + self.vely >= dimensoesTela[1]:
            self.corpo.bottom = dimensoesTela[1] - self.altura
            self.vely = 0

        ##### COLISOES COM OBSTACULOS #####
        for obstaculo in mapa.listaDeObstaculos:

            cCima, cBaixo, cDireita, cEsquerda = self.checar_colisao(obstaculo.corpo)

            # Essa checagem em dois passos tem que ocorrer por que se nao ele so salva a colisao com o utlimo obstaculo
            if cCima: colisaoDireita = True
            if cBaixo: colisaoBaixo = True
            if cEsquerda: colisaoEsquerda = True
            if cDireita: colisaoDireita = True

        ##### HORIZONTAIS #####
        if colisaoEsquerda or colisaoDireita:
            self.velx = self.velx * -1

        ##### VERTICAIS #####
        if colisaoBaixo:
            self.vely = 0
            self.y = obstaculo.corpo.top - self.altura

        ##### GRAVIDADE ######
        if not colisaoBaixo: self.vely += 1

        self.y += self.vely
        self.x += self.velx

    def atualizar(self, tela):
        self.corpo.x = self.x
        self.corpo.y = self.y
        pygame.draw.rect(tela, (88,51,0), self.corpo)#88, 51, 0
