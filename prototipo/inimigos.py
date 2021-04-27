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

    def mover(self, dimensoesTela, mapa):

        ##### COLISOES #####
        colisaoCima, colisaoBaixo, colisaoEsquerda, colisaoDireita = False, False, False, False
        cCima, cBaixo, cEsquerda, cDireita = False, False, False, False
        obsBaixo, obsCima, obsEsquerda, obsDireita = 0,0,0,0

        ##### COLISOES COM OBSTACULOS #####
        for entidade in mapa.lista_de_entidades:
            if entidade != self:

                cCima, cBaixo, cDireita, cEsquerda = self.checar_colisao(entidade.corpo)

                # Essa checagem em dois passos tem que ocorrer por que se nao ele so salva a colisao com o utlimo obstaculo
                if cCima:
                    colisaoCima = True
                    obsCima = entidade
                if cBaixo:
                    colisaoBaixo = True
                    obsBaixo = entidade
                if cEsquerda:
                    colisaoEsquerda = True
                    obsEsquerda = entidade
                if cDireita:
                    colisaoDireita = True
                    obsDireta = entidade

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

    def renderizar(self, tela, mapa):
        pygame.draw.rect(tela, (88, 51, 0), [self.corpo.x - mapa.campo_visivel.x - 50, self.corpo.y, self.corpo.w, self.corpo.h])  # 88, 51, 0