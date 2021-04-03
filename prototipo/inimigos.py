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
        corpoLargo = pygame.Rect(self.x-1, self.y-1, self.largura+2,self.altura+2)
        colisao = corpoLargo.colliderect(corpo)
        return colisao

    def mover(self, dimensoesTela, mapa):
        #Faz ele correr pros dois lados
        if self.x <= self.xinicial: self.velx = self.velx = 1
        if self.x >= self.xinicial + 400: self.velx = self.velx = -1

        ##### COLISOES #####
        colisao = False

        contatoComChao = False

        ##### COLISAO COM O CHAO #####
        if self.corpo.bottom + self.vely >= dimensoesTela[1]:
            self.corpo.bottom = dimensoesTela[1] - self.altura
            self.vely = 0
            contatoComChao = True

        ##### COLISOES COM OBSTACULOS #####
        for obstaculo in mapa.listaDeObstaculos:

            colisao = self.checar_colisao(obstaculo.corpo)

            ##### VERTICAIS #####
            if colisao and self.corpo.bottom >= obstaculo.corpo.top:
                self.vely = 0
                self.y = obstaculo.corpo.top - self.altura
                contatoComChao = True
                break

        ##### GRAVIDADE ######
        if not contatoComChao: self.vely += 1

        self.y += self.vely
        self.x += self.velx

    def atualizar(self, tela):
        self.corpo.x = self.x
        self.corpo.y = self.y
        pygame.draw.rect(tela, (88,51,0), self.corpo)#88, 51, 0
