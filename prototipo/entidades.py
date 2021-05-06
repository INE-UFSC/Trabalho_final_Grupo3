#Arquivos com as classes abstratas do jogo
import pygame
from sprites import SpriteSheet

colisao_analisada = "cano3"
renderizar_hitbox = True
renderizar_sprite = True
gravidade = 0.2

class Estatico():

    def __init__(self, nome: str, x:int, y:int, altura: int, largura: int, imagem: str, cor = (0,0,0)):
        self.__nome = nome
        self.__x = x
        self.__y = y
        self.__largura = largura
        self.__altura = altura
        self.__corpo = pygame.Rect(x, y, largura, altura)
        self.__imagem = imagem
        try:
            self.__sprite = SpriteSheet(imagem)
        except FileNotFoundError:
            self.__sprite = [] #nao possui sprite
        self.__cor = cor

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
    def imagem(self):
        return self.__imagem

    @imagem.setter
    def imagem(self, imagem):
        self.__imagem = imagem

    @property
    def sprite(self):
        return self.__sprite

    @sprite.setter
    def sprite(self, sprite):
        self.__sprite = sprite
    
    @property
    def cor(self):
        return self.__cor

    def auto_destruir(self, mapa):
         if self in mapa.lista_de_entidades: #RESOLVE PROVISORIAMENTE
            mapa.lista_de_entidades.remove(self)

    def renderizar(self, tela, mapa):
        if renderizar_hitbox: 
            pygame.draw.rect(tela, self.__cor, [self.corpo.x - mapa.campo_visivel.x, 
                                                self.corpo.y - mapa.campo_visivel.y,
                                                self.corpo.w, 
                                                self.corpo.h])
        if renderizar_sprite:
            try:
                self.sprite.imprimir(self.__imagem, self.x-mapa.campo_visivel.x, self.y - mapa.campo_visivel.y,tela, 1, 0)
            except AttributeError:
                pass #nao possui sprite

    def atualizar(self, tela, mapa, dimensoes_tela):
        if mapa.campo_visivel.colliderect(self.corpo):
            self.renderizar(tela, mapa)
        return False

    def sofreu_colisao_jogador(self, jogador, direcao, mapa):
        ##### COLISAO ESQUERDA #####
        if direcao == "esquerda":
            if jogador.velx <= 0:
                jogador.velx = 0
                aceleracao = 0
                jogador.x = self.corpo.right + 1
        ##### COLISAO DIREITA #####
        elif direcao == "direita":
            if jogador.velx >= 0:
                jogador.velx = 0
                aceleracao = 0
                jogador.x = self.corpo.left - jogador.largura
        ##### COLISAO BAIXO #####
        elif direcao == "baixo":
            jogador.vely = 0
            jogador.y = self.corpo.top - jogador.altura
        ##### COLISAO CIMA #####
        elif direcao == "cima":
            if jogador.vely < 0:
                jogador.vely = 0
                jogador.y = self.corpo.bottom
        return 0

    def sofreu_colisao_outros(self, entidade, direcao):
        if direcao in ["direita","esquerda"]:
            entidade.velx = -entidade.velx
        if direcao in ["baixo"]:
            entidade.vely = 0
            entidade.y = self.corpo.top - entidade.altura

class Movel(Estatico):

    def __init__(self, nome: str, x: int, y: int, largura:int, altura:int, limite_vel: int, imagem: str,cor = (0,0,0)):
        super().__init__(nome, x, y, largura, altura, imagem,cor)
        self.escala_tempo = 1.0
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

    def checar_colisao(self, lista_de_entidades, tipos_transparentes):
        ##### COLISOES #####
        obsBaixo, obsCima, obsEsquerda, obsDireita = 0, 0, 0, 0

        ##### COLISOES COM OBSTACULOS #####
        for entidade in lista_de_entidades:
            transparente = False
            for tipo in tipos_transparentes:
                transparente = transparente or isinstance(entidade,tipo)
            if entidade != self and not transparente:

                cCima, cBaixo, cEsquerda, cDireita = False, False, False, False
                if self.__velx < 0:  # movimento para a esquerda
                    cveloz_left = self.corpo.left - 1 + self.__velx*self.escala_tempo
                    cveloz_largura = self.corpo.right - cveloz_left + 1
                else:  # movimento para a direita
                    cveloz_left = self.corpo.left - 1
                    cveloz_largura = self.corpo.right - cveloz_left + 1 + self.__velx*self.escala_tempo
                if self.__vely < 0:  # movimento para cima
                    cveloz_top = self.corpo.top - 1 + self.__vely*self.escala_tempo
                    cveloz_altura = self.corpo.bottom - cveloz_top + 1
                else:  # movimento para baixo
                    cveloz_top = self.corpo.top
                    cveloz_altura = self.corpo.bottom - cveloz_top + 1 + self.__vely*self.escala_tempo
                self.__corpoveloz = pygame.Rect(cveloz_left, cveloz_top, cveloz_largura, cveloz_altura)
                colisaoVeloz = self.__corpoveloz.colliderect(entidade.corpo)

                if colisaoVeloz:
                    # CALCULO DE O QUAO DENTRO O OBJETO TA HORIZONTALMENTE E VERTICALMENTE
                    ##### VERTICIAIS #####
                    dist_y = 0
                    if not self.__vely:  # parado
                        dist_y = min(self.__corpoveloz.bottom - entidade.corpo.top, entidade.corpo.bottom - self.__corpoveloz.top)
                    elif self.__vely > 0:  # caindo
                        dist_y = self.__corpoveloz.bottom - entidade.corpo.top
                    else:  # subindo
                        dist_y = entidade.corpo.bottom - self.__corpoveloz.top
                    dist_x = 0
                    ##### HORIZONTAL #####
                    if not self.__velx:  # parado
                        dist_x = min(entidade.corpo.right - self.__corpoveloz.left,
                                     self.__corpoveloz.right - entidade.corpo.left)  # colisao a direita = +
                    elif self.__velx > 0:  # movimentacao pra direita
                        dist_x = self.__corpoveloz.right - entidade.corpo.left
                    else:  # movimentacao pra esquerda
                        dist_x = entidade.corpo.right - self.__corpoveloz.left

                    if self.__vely >= 0 and dist_x  >= dist_y + 2:
                        cBaixo = True
                    elif self.__vely < 0 and dist_x  >= dist_y + 2:
                        cCima = True
                    elif self.__velx > 0 and dist_x < dist_y:
                        cDireita = True
                    elif self.__velx < 0 and dist_x < dist_y:
                        cEsquerda = True
                    elif not self.__velx and abs(dist_x) < dist_y:
                        if self.__corpoveloz.right - entidade.corpo.left > entidade.corpo.right - self.__corpoveloz.left:
                            cEsquerda = True
                        else:
                            cDireita = True

                # Essa checagem em dois passos tem que ocorrer por que se nao ele so salva a colisao com o utlimo obstaculo
                if cCima: obsCima = entidade
                if cBaixo: obsBaixo = entidade
                if cEsquerda: obsEsquerda = entidade
                if cDireita: obsDireita = entidade

        return[obsCima,obsBaixo,obsDireita,obsEsquerda]

    def atualizar(self, tela, mapa, dimensoes_tela):
        if self.escala_tempo != mapa.escala_tempo:
            self.escala_tempo += max(min(mapa.escala_tempo-self.escala_tempo,0.05),-0.05)
        self.mover(dimensoes_tela, mapa)
        self.corpo = pygame.Rect(self.x, self.y, self.largura, self.altura)
        if mapa.campo_visivel.colliderect(self.corpo):
            self.renderizar(tela, mapa)
        return False

    # def sofreu_colisao_jogador(self, jogador, direcao, mapa):
    #     pass

    def sofreu_colisao_outros(self, entidade, direcao):
        if direcao in ["direita","esquerda"]:
            entidade.velx = -entidade.velx
            self.velx = -self.velx
        if direcao in ["baixo"]:
            entidade.vely = 0
            entidade.y = self.corpo.top - entidade.altura

class Entidade(Movel):
    def __init__(self, nome: str, x: int, y: int, largura:int, altura:int, limiteVel: int, vida:int, dano_contato:int, imagem:str,cor = (0,0,0)):
        super().__init__(nome, x, y, largura, altura, limiteVel, imagem,cor)
        self.__vida = vida
        self.__dano_contato = dano_contato

    @property
    def vida(self):
        return self.__vida

    @vida.setter
    def vida(self, vida):
        self.__vida = vida

    @property
    def dano_contato(self):
        return self.__dano_contato

    @dano_contato.setter
    def dano_contato(self, dano_contato):
        self.__dano_contato = dano_contato

    @property
    def contato(self):
        return self.__contato
    
    @contato.setter
    def contato(self,contato):
        self.__contato = contato

    def sofreu_colisao_jogador(self, jogador, direcao, mapa):
        ##### COLISAO ESQUERDA #####
        if direcao == "esquerda":
            if jogador.velx <= 0:
                jogador.velx = 0
                jogador.aceleracao = 0
                jogador.x = self.corpo.right + 1
            return self.__dano_contato
        ##### COLISAO DIREITA #####
        elif direcao == "direita":
            if jogador.velx >= 0:
                jogador.velx = 0
                jogador.aceleracao = 0
                jogador.x = self.corpo.left - jogador.largura
            return self.__dano_contato
        ##### COLISAO BAIXO #####
        elif direcao == "baixo":
            jogador.vely = 0
            jogador.y = self.corpo.top - jogador.altura
            self.auto_destruir(mapa)
            return 0
        ##### COLISAO CIMA #####
        elif direcao == "cima":
            if jogador.vely < 0:
                jogador.vely = 0
                jogador.y = self.corpo.bottom
            return self.__dano_contato