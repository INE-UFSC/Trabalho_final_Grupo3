#Arquivos com as classes abstratas do jogo
import pygame
class Estatico():

    def __init__(self, nome: str, x:int, y:int, altura: int, largura: int):
        self.__nome = nome 
        self.__x = x
        self.__y = y
        self.__largura = largura
        self.__altura = altura
        self.__corpo = pygame.Rect(x, y, largura, altura)

    @property
    def nome (self):
        return self.__nome 

    @nome.setter
    def nome (self, nome):
         self.__nome = nome

    @property
    def x(self):
        return self.__x
     
    @x.setter
    def x(self, x):
         self.__x = x

    @property
    def y(self):
        return self.__y

    @y.setter
    def y(self, y):
        self.__y = y

    @property
    def largura(self):
        return self.__largura

    @largura.setter
    def largura(self, lagura):
        self.__lagura = lagura

    @property
    def altura(self):
        return self.__altura

    @altura.setter
    def altura(self, altura):
        self.__altura = altura

    def Inicializar(self):
        pass

    def Atualizar(self):
        pass

class Movel(Estatico):

    def __init__(self, nome: str, x: int, y: int, largura:int, altura:int, limiteVel: int):
        super().__init__(nome, x, y, largura, altura)
        self.__velx = 0
        self.__vely = 0
        self.__limiteVel = limiteVel

    @property
    def velx(self):
        return self.__velx

    @velx.setter
    def velx(self, velx):
        self.__velx = velx

    @property
    def vely(self):
        return self.__vely

    @vely.setter
    def vely(self, vely):
        self.__vely = vely

    @property
    def limiteVel(self):
        return self.__limiteVel

    @limiteVel.setter
    def limiteVel(self, limiteVel):
        self.__limiteVel = limiteVel

    def Mover(self):
        pass

class Entidade(Movel):
    def __init__(self, nome: str, x: int, y: int, largura:int, altura:int, limiteVel: int, vida:int, danoContato:int):
        super().__init__(nome, x, y, largura, altura, limiteVel)
        self.__vida = vida
        self.__danoContato = danoContato

    @property
    def vida(self):
        return self.__vida

    @vida.setter
    def vida(self, vida):
        self.__vida = vida

    @property
    def danoContato(self):
        return self.__danoContato

    @danoContato.setter
    def danoContato(self, danoContato):
        self.__danoContato = danoContato

    def Sumir(self):
        pass