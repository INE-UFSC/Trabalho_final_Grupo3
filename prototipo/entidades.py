#Arquivos com as classes abstratas do jogo
import pygame

gravidade = 0.2

class Estatico():

    def __init__(self, nome: str, x:int, y:int, altura: int, largura: int):
        self.__nome = nome 
        self.__x = x
        self.__y = y
        self.__largura = largura
        self.__altura = altura
        self.__corpo = pygame.Rect(x, y, largura, altura)
        self.__corpocor = pygame.Rect(x+2, y+2, largura-4, altura-4)

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

    @property
    def corpo(self):
        return self.__corpo

    @corpo.setter
    def corpo(self, corpo):
        self.__corpo = corpo
    
    @property
    def corpocor(self):
        return self.__corpocor

    @corpo.setter
    def corpocor(self, corpocor):
        self.__corpocor = corpocor

    def iniciar(self):
        pass

    def atualizar(self):
        pass

class Movel(Estatico):

    def __init__(self, nome: str, x: int, y: int, largura:int, altura:int, limite_vel: int):
        super().__init__(nome, x, y, largura, altura)
        self.__velx = 0
        self.__vely = 0
        self.__limite_vel = limite_vel

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
    def limite_vel(self):
        return self.__limite_vel

    @limite_vel.setter
    def limite_vel(self, limite_vel):
        self.__limite_vel = limite_vel

    def mover(self):
        pass

    def checar_colisao(self):
        pass

class Entidade(Movel):
    def __init__(self, nome: str, x: int, y: int, largura:int, altura:int, limiteVel: int, vida:int, dano_contato:int):
        super().__init__(nome, x, y, largura, altura, limiteVel)
        self.__vida = vida
        self.__dano_contato = dano_contato

    @property
    def vida(self):
        return self.__vida

    @vida.setter
    def vida(self, vida):
        self.__vida = vida

    @property
    def danoContato(self):
        return self.__dano_contato

    @danoContato.setter
    def danoContato(self, dano_contato):
        self.__dano_contato = dano_contato

    def sumir(self):
        pass