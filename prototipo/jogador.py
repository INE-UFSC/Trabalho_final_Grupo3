import pygame
from obstaculos import Bloco
from entidades import gravidade

class Jogador: 
    def __init__(self, nome: str, x: int, y: int, velx: int, vida: int):
        self.__vida = vida
        self.__nome = nome 
        self.__x = x
        self.__y = y
        #Modifiquei pra altura e largura serem variaveis - Bernardo
        self.__altura = 50
        self.__largura = 25
        self.__pulo = 20
        self.__velx = velx
        self.__vely = 0
        self.__corpo = pygame.Rect(self.__x , self.__y, self.__largura, self.__altura)

    @property
    def nome (self):
        return self.__nome
    
    @nome.setter
    def nome (self, nome):
        self.__nome = nome

    @property
    def x (self):
        return self.__x
    
    @property
    def y (self):
        return self.__y

    @property
    def velx (self):
        return self.__velx
    
    @velx.setter
    def velx(self, velx):
        self.__velx = velx

    @property
    def corpo(self):
        return self.__corpo

    def checar_colisao(self, corpo, nome):
        colisaoBaixo, colisaoCima, colisaoEsquerda, colisaoDireita = False, False, False, False
        corpoLargo = pygame.Rect(self.__x-1, self.__y-1, self.__largura+2,self.__altura+2)
        colisaoAjustada = corpoLargo.colliderect(corpo)
        if colisaoAjustada:
            ##### VERTICAIS #####
            if self.corpo.left in range(corpo.left+1, corpo.right-1) or self.corpo.right in range(corpo.left+1, corpo.right-1):
                if corpoLargo.bottom in range(corpo.top+1, corpo.bottom-1 + int(self.__vely)):
                    colisaoBaixo = True
                elif corpoLargo.top in range(corpo.top+1+ int(self.__vely), corpo.bottom-1):
                    colisaoCima = True
            ##### HORIZONTAIS #####
            if (self.corpo.top in range(corpo.top+1, corpo.bottom-1) or self.corpo.bottom in range(corpo.top+1, corpo.bottom-1)) and (not colisaoCima and not colisaoBaixo):
                if nome == "cano1": print(True, corpoLargo.left, range(corpo.left+1 + int(self.__velx), corpo.right-1))
                if corpoLargo.right in range(corpo.left+1, corpo.right-1 + int(self.__velx)):
                    colisaoDireita = True
                if corpoLargo.left in range(corpo.left+1 + int(self.__velx), corpo.right):
                    colisaoEsquerda = True
        return [colisaoCima, colisaoBaixo, colisaoDireita, colisaoEsquerda]

    # def colisao(self, objeto):
    #     #if self.__x + 80 + self.__velocidade >= objeto[0].bottomleft[0] and self.__x + 80 + self.__velocidade <= objeto[0].bottomright[0] :
    #         #print("Colidiu")
    #
    #     #Obstaculo generico nao existe, tem que arrumar, ve como eu faco no goomba - Bernardo
    #     if isinstance(objeto[1], ObstaculoGenerico):
    #         if self.__corpo.colliderect(objeto[0]):
    #             return
    #     if self.__x + self.__largura + self.__velx >= objeto.bottomleft[0] and self.__x + self.__largura + self.__velx <= objeto.bottomright[0] :
    #         self.__vida = self.__vida - 1
    #         self.__x = self.__x - 20
    #         print(self.__vida)
    #         self.__corpo = pygame.Rect(self.__x , self.__y, self.__largura, self.__altura)
    #         if self.__vida == 0:
    #             self.__x = 1000000000
    #             self.__y = 1000000000
    #             self.__corpo = pygame.Rect(self.__x , self.__y, self.__largura, self.__altura)

    
    def atualizar(self, screen):
        pygame.draw.rect(screen, (0,0,0), self.__corpo)
    
    def mover(self, direita, esquerda, espaco, screen, mapa):

        ##### MOVIMENTO HORIZONTAL #####
        self.__velx = direita - esquerda

        ##### COLISOES #####
        colisaoCima, colisaoBaixo, colisaoEsquerda, colisaoDireita = False, False, False, False
        cCima, cBaixo, cEsquerda, cDireita = False, False, False, False
        obsBaixo, obsCima, obsEsquerda, obsDireita = 0,0,0,0

        ##### COLISOES COM OBSTACULOS #####
        for obstaculo in mapa.listaDeObstaculos:

            cCima, cBaixo, cDireita, cEsquerda = self.checar_colisao(obstaculo.corpo, obstaculo.nome)

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
                obsDireita = obstaculo

            # if cEsquerda or cDireita:
            #     print(obstaculo.nome, colisaoBaixo, colisaoEsquerda, colisaoDireita)

        ##### HORIZONTAIS #####
        if colisaoEsquerda:
            if self.__velx < 0:
                self.__velx = 0
                self.__x = obsEsquerda.corpo.right

        if colisaoDireita:
            if self.__velx > 0:
                self.__velx = 0
                self.__x = obsDireita.corpo.left - self.__largura

        ##### VERTICAIS #####
        if colisaoBaixo:
            self.__vely = 0
            self.__y = obsBaixo.corpo.top - self.__altura
            if espaco:
                self.__vely = -self.__pulo

        ##### GRAVIDADE ######
        if not colisaoBaixo: self.__vely += gravidade

        ##### ATUALIZACAO DE POSICOES #####
        self.__y += self.__vely
        self.__x += self.__velx

        #print(self.__x, self.__y)

        self.__corpo = pygame.Rect(self.__x , self.__y, self.__largura, self.__altura)