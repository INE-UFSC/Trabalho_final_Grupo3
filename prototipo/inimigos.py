#Arquivo destinado a fazer todos os inimigos
import pygame
from entidades import Entidade, gravidade

class Goomba(Entidade):
    def __init__(self, nome: str, x: int, y: int):
        vida = 1
        danoContato = 1
        largura = 30
        altura = 30
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
                if corpoLargo.bottom in range(corpo.top+1, corpo.bottom-1 + int(self.vely)):
                    colisaoBaixo = True
                elif corpoLargo.top in range(corpo.top+1+ int(self.vely), corpo.bottom-1):
                    colisaoCima = True
            ##### HORIZONTAIS #####
            if (self.corpo.top in range(corpo.top+1, corpo.bottom-1) or self.corpo.bottom in range(corpo.top+1, corpo.bottom-1))\
                    and (not colisaoCima and not colisaoBaixo):
                if corpoLargo.right in range(corpo.left+1, corpo.right-1 + int(self.velx)):
                    colisaoDireita = True
                if corpoLargo.left in range(corpo.left+1 + int(self.velx), corpo.right-1):
                    colisaoEsquerda = True
        return [colisaoCima, colisaoBaixo, colisaoDireita, colisaoEsquerda]

    def mover(self, dimensoesTela, mapa):

        ##### COLISOES #####
        colisaoCima, colisaoBaixo, colisaoEsquerda, colisaoDireita = False, False, False, False
        cCima, cBaixo, cEsquerda, cDireita = False, False, False, False
        obsBaixo, obsCima, obsEsquerda, obsDireita = 0,0,0,0

        ##### COLISOES COM OBSTACULOS #####
        for obstaculo in mapa.lista_de_obstaculos:

            cCima, cBaixo, cDireita, cEsquerda = self.checar_colisao(obstaculo.corpo)

            # Essa checagem em dois passos tem que ocorrer por que se nao ele so salva a colisao com o utlimo obstaculo
            if cCima:
                colisaoCima = True
                obsCima = obstaculo
            if cBaixo:
                colisaoBaixo = True
                obsBaixo = obstaculo
            if cEsquerda:
                colisaoEsquerda = True
                obsEsquerda = obstaculo
            if cDireita:
                colisaoDireita = True
                obsDireta = obstaculo

        ##### HORIZONTAIS #####
        if colisaoEsquerda or colisaoDireita:
            self.velx = self.velx * -1

        ##### VERTICAIS #####
        if colisaoBaixo:
            self.vely = 0
            self.y = obsBaixo.corpo.top - self.altura

        ##### GRAVIDADE ######
        if not colisaoBaixo: self.vely += gravidade

        self.y += self.vely
        self.x += self.velx

    def atualizar(self, tela, dimensoesTela,mapa):
        self.mover(dimensoesTela, mapa)
        self.corpo.x = self.x
        self.corpo.y = self.y
        pygame.draw.rect(tela, (88,51,0), [self.corpo.x-mapa.campo_visivel.x-50,self.corpo.y,self.corpo.w,self.corpo.h])#88, 51, 0
