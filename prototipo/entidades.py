#Arquivos com as classes abstratas do jogo
import pygame

colisao_analisada = "cano3"
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

    @corpocor.setter
    def corpocor(self, corpocor):
        self.__corpocor = corpocor

    def renderizar(self, tela, mapa):
        pass

    def atualizar(self, tela, mapa, dimensoes_tela):
        if mapa.campo_visivel.colliderect(self.corpo):
            self.renderizar(tela, mapa)
        return False

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

    def mover(self, dimensoesTela, mapa):
        pass

    def checar_colisao(self, corpo):
        colisaoBaixo, colisaoCima, colisaoEsquerda, colisaoDireita = False, False, False, False
        if self.__velx < 0:  # movimento para a esquerda
            cveloz_left = self.corpo.left - 1 + self.__velx
            cveloz_largura = self.corpo.right - cveloz_left + 1
        else:  # movimento para a direita
            cveloz_left = self.corpo.left - 1
            cveloz_largura = self.corpo.right - cveloz_left + 1 + self.__velx
        if self.__vely < 0:  # movimento para cima
            cveloz_top = self.corpo.top - 1 + self.__vely
            cveloz_altura = self.corpo.bottom - cveloz_top + 1
        else:  # movimento para baixo
            cveloz_top = self.corpo.top
            cveloz_altura = self.corpo.bottom - cveloz_top + 1 + self.__vely
        self.__corpoveloz = pygame.Rect(cveloz_left, cveloz_top, cveloz_largura, cveloz_altura)
        colisaoVeloz = self.__corpoveloz.colliderect(corpo)

        if colisaoVeloz:
            # CALCULO DE O QUAO DENTRO O OBJETO TA HORIZONTALMENTE E VERTICALMENTE
            ##### VERTICIAIS #####
            dist_y = 0
            if not self.__vely:  # parado
                dist_y = min(self.__corpoveloz.bottom - corpo.top, corpo.bottom - self.__corpoveloz.top)
            elif self.__vely > 0:  # caindo
                dist_y = self.__corpoveloz.bottom - corpo.top
            else:  # subindo
                dist_y = corpo.bottom - self.__corpoveloz.top
            dist_x = 0
            ##### HORIZONTAL #####
            if not self.__velx:  # parado
                dist_x = min(corpo.right - self.__corpoveloz.left,
                             self.__corpoveloz.right - corpo.left)  # colisao a direita = +
            elif self.__velx > 0:  # movimentacao pra direita
                dist_x = self.__corpoveloz.right - corpo.left
            else:  # movimentacao pra esquerda
                dist_x = corpo.right - self.__corpoveloz.left

            if self.__vely >= 0 and dist_x + self.largura / 2 >= dist_y:
                colisaoBaixo = True
            elif self.__vely < 0 and dist_x + self.largura / 2 >= dist_y:
                colisaoCima = True
            elif self.__velx > 0 and dist_x < dist_y:
                colisaoDireita = True
            elif self.__velx < 0 and dist_x < dist_y:
                colisaoEsquerda = True
            elif not self.__velx and abs(dist_x) < dist_y:
                if self.__corpoveloz.right - corpo.left > corpo.right - self.__corpoveloz.left:
                    colisaoEsquerda = True
                else:
                    colisaoDireita = True
        return [colisaoCima, colisaoBaixo, colisaoDireita, colisaoEsquerda]

    def atualizar(self, tela, mapa, dimensoes_tela):
        self.mover(dimensoes_tela, mapa)
        self.corpo = pygame.Rect(self.x, self.y, self.largura, self.altura)
        if mapa.campo_visivel.colliderect(self.corpo):
            self.renderizar(tela, mapa)
        return False

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