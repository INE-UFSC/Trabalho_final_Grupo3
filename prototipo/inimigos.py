#Arquivo destinado a fazer todos os inimigos
import pygame
from entidades import Entidade, gravidade, renderizar_hitbox, renderizar_sprite

class Rato(Entidade):
    def __init__(self, nome: str, x: int, y: int):
        vida = 1
        danoContato = 1
        largura = 46
        altura = 46
        limiteVel = 4
        contatos = ['dano', 'morrer', 'dano', 'dano']
        super().__init__(nome, x, y, largura, altura, limiteVel, vida, danoContato, "0", contatos)
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

    def renderizar(self, tela, mapa):
        if renderizar_hitbox: pygame.draw.rect(tela, (88, 51, 0), [self.corpo.x - mapa.campo_visivel.x, self.corpo.y, self.corpo.w, self.corpo.h])  # 88, 51, 0