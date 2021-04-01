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

    def Mover(self, tela):
        #Faz ele correr pros dois lados
        if self.x <= self.xinicial: self.velx = self.velx = 1
        if self.x >= self.xinicial + 400: self.velx = self.velx = -1

        #Gravidade
        if self.corpo.bottom + self.vely >= tela[1]:
            self.corpo.bottom = tela[1] - self.altura
            self.vely = 0
        else:
            self.vely += 1

        self.y += self.vely
        self.x += self.velx

    def Atualizar(self, tela):
        self.corpo.x = self.x
        self.corpo.y = self.y
        pygame.draw.rect(tela, (88,51,0), self.corpo)#88, 51, 0