import pygame
from obstaculos import Bloco

class Jogador: 
    def __init__(self, nome: str, x: int, y: int, velocidade: int, vida: int):
        self.__vida = vida
        self.__nome = nome 
        self.__x = x
        self.__y = y
        self.__velocidade = velocidade
        self.__vely = 0
        self.__corpo = pygame.Rect(self.__x , self.__y, 80, 200)

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
    def velocidade (self):
        return self.__velocidade
    
    @velocidade.setter
    def velocidade(self, velocidade):
        self.__velocidade = velocidade

    @property
    def corpo(self):
        return self.__corpo

    def colisao(self, objeto):
        #if self.__x + 80 + self.__velocidade >= objeto[0].bottomleft[0] and self.__x + 80 + self.__velocidade <= objeto[0].bottomright[0] :
            #print("Colidiu")
        
        if isinstance(objeto[1], ObstaculoGenerico):
            if self.__corpo.colliderect(objeto[0]):
                return
        if self.__x + 80 + self.__velocidade >= objeto.bottomleft[0] and self.__x + 80 + self.__velocidade <= objeto.bottomright[0] :
            self.__vida = self.__vida - 1
            self.__x = self.__x - 20
            print(self.__vida)
            self.__corpo = pygame.Rect(self.__x , self.__y, 80, 200)
            if self.__vida == 0:
                self.__x = 1000000000
                self.__y = 1000000000
                self.__corpo = pygame.Rect(self.__x , self.__y, 80, 200)

    
    def atualizar(self, screen):
        pygame.draw.rect(screen, (0,0,0), self.__corpo)
    
    def mover(self, direita, esquerda, espaco, screen):
        self.__velocidade = direita - esquerda

        if espaco and self.__y == screen[1] - 200:
            self.__vely = -20

        if self.__y + self.__vely >= screen[1] - 200:
            self.__y = screen[1] - 200
            self.__vely = 0
        else:
            self.__vely += 1

        self.__y += self.__vely
        self.__x += self.__velocidade

        self.__x = self.__x
        self.__corpo = pygame.Rect(self.__x , self.__y, 80, 200)

