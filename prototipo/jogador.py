import pygame
from obstaculos import Bloco, Vitoria
from entidades import gravidade, colisao_analisada, renderizar_hitbox, renderizar_sprite
from inimigos import Goomba
from poderes import PoderManifestado,VermelhoDoMago,BolaFogo
from sprites import SpriteSheet

class Jogador: 
    def __init__(self, nome: str, x: int, y: int, velx: int, vida: int):
        ##### ATRIBUTOS GERAIS #####
        self.__vida = 10
        self.__nome = nome
        self.__imagem = SpriteSheet("andando")

        ##### ATRIBUTOS POSICIONAIS #####
        self.__x = x
        self.__y = y
        self.__altura = 46
        self.__largura = 46
        self.__pulo = 9
        self.__velx = velx
        self.__vely = 0
        self.__velocidade_max = 5
        self.__face = 1
        self.__corpo = pygame.Rect(self.__x , self.__y, self.__largura, self.__altura)

        ##### ATRIBUTOS COMPORTAMENTAIS #####
        self.__poder = VermelhoDoMago()
        self.__recarga = 0

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

    @property
    def poder(self):
        return self.__poder

    @poder.setter
    def poder(self, poder):
        self.__poder = poder

    @property
    def vida(self):
        return self.__vida

    @property
    def face(self):
        return self.__face
    
    def vida_pra_zero(self):
        self.__vida = 0

    def checar_colisao(self, lista_de_entidades, tipos_transparentes):
        ##### COLISOES #####
        obsBaixo, obsCima, obsEsquerda, obsDireita = 0, 0, 0, 0

        ##### COLISOES COM OBSTACULOS #####
        for entidade in lista_de_entidades:
            if entidade != self and not type(entidade) in tipos_transparentes:

                cCima, cBaixo, cEsquerda, cDireita = False, False, False, False
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
                colisaoVeloz = self.__corpoveloz.colliderect(entidade.corpo)

                if colisaoVeloz:
                    # CALCULO DE O QUAO DENTRO O OBJETO TA HORIZONTALMENTE E VERTICALMENTE
                    ##### VERTICIAIS #####
                    dist_y = 0
                    if not self.__vely:  # parado
                        dist_y = min(self.__corpoveloz.bottom - entidade.corpo.top,
                                     entidade.corpo.bottom - self.__corpoveloz.top)
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

                    if self.__vely >= 0 and dist_x + self.__largura / 2 >= dist_y:
                        cBaixo = True
                    elif self.__vely < 0 and dist_x + self.__largura / 2 >= dist_y:
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

        return [obsCima, obsBaixo, obsDireita, obsEsquerda]

    def renderizar(self, tela, campo_visivel, ciclo):
        if renderizar_hitbox: pygame.draw.rect(tela, (0,0,0), [self.corpo.x-campo_visivel.x,self.corpo.y,self.corpo.w,self.corpo.h])
        if renderizar_sprite: self.__imagem.imprimir("andando"+str(ciclo%12), self.__x-campo_visivel.x, self.__y, tela, self.__face)

    def atualizar(self, screen, campo_visivel, ciclo): ### REQUER AREA VISIVEL PARA RENDERIZAR
        self.renderizar(screen, campo_visivel, ciclo)
        if self.__recarga > 0: self.__recarga -= 1
        if self.__poder != '':
            self.__poder.atualizar(screen,campo_visivel)
        if self.x > campo_visivel.x + 600:
            return pygame.Rect(self.x-600,0,campo_visivel.w,campo_visivel.h)
        elif self.x < campo_visivel.x + 400:
            return pygame.Rect(self.x-400,0,campo_visivel.w,campo_visivel.h) if campo_visivel.x > 0 else pygame.Rect(0,0,campo_visivel.w,campo_visivel.h)
        return campo_visivel

    def mover(self, direita, esquerda, espaco, screen, mapa, atrito):

        ##### MOVIMENTO HORIZONTAL #####
        aceleracao = (direita - esquerda)
        self.__velx += aceleracao

        ##### COLISOES #####
        ##### COLISOES #####
        obsCima, obsBaixo, obsDireita, obsEsquerda = self.checar_colisao(mapa.lista_de_entidades, [BolaFogo])

        ##### REPOSICIONAMENTO POS COLISAO #####
        if obsDireita and obsEsquerda: #ESMAGAMENTO
            self.__vida = 0 #AQUI EH TESTE N SEI SE ESSA VARIAVEL VAI FICAR COMO STRING MSM

        if obsEsquerda:
            #print("COLISAO PELA ESQUERDA", obsEsquerda.nome)
            if self.__velx <= 0:
                self.__velx = 0
                aceleracao = 0
                self.__x = obsEsquerda.corpo.right+1

        if obsDireita:
            #print("COLISAO PELA DIREITA", obsDireita.nome)
            if self.__velx >= 0:
                self.__velx = 0
                aceleracao = 0
                self.__x = obsDireita.corpo.left - self.__largura

        if obsBaixo:
            self.__vely = 0
            self.__y = obsBaixo.corpo.top - self.__altura
            if espaco:
                self.__vely = -self.__pulo

        if obsCima:
            if self.__vely < 0:
                self.__vely = 0
                self.__y = obsCima.corpo.bottom

        #### COLISAO GOOMBA ####
        for cada_termo in mapa.lista_de_entidades: 
            if isinstance (cada_termo, Goomba):
                entidade = cada_termo
        
                if obsEsquerda != 0:
                    if isinstance(obsEsquerda, Goomba):
                        self.__vida -= entidade.dano_contato
                
                if obsDireita != 0: 
                    if isinstance(obsDireita, Goomba):
                        self.__vida -= entidade.dano_contato

        ### CHECANDO VITÓRIA ###
        for cada_termo in mapa.lista_de_entidades: 
            if isinstance (cada_termo, Vitoria):
                entidade = cada_termo

                if obsEsquerda != 0:
                    if isinstance(obsEsquerda, Vitoria):
                        mapa.ganhou = True

                if obsDireita != 0: 
                    if isinstance(obsDireita, Vitoria):
                        mapa.ganhou = True

                if obsBaixo != 0: 
                    if isinstance(obsBaixo, Vitoria):
                        mapa.ganhou = True

        ##### GRAVIDADE ######
        if not obsBaixo: self.__vely += gravidade

        ##### ATRITO ######
        if aceleracao == 0:
            if self.__velx < 0:
                self.__velx += atrito
            elif self.__velx > 0:
                self.__velx -= atrito

        if self.__velx >= self.__velocidade_max: self.__velx = self.__velocidade_max
        elif self.__velx <= -self.__velocidade_max: self.__velx = -self.__velocidade_max

        ##### ATUALIZACAO DE POSICOES #####
        self.__y += self.__vely
        self.__x += self.__velx

        ##### MATA O JOGADOR SE CAIR NO BURACO #####
        if self.__y > screen[1]: self.__vida = 0

        ##### INDICA A DIRECAO DO JOGADOR PARA DIRECIONAR PODERES #####
        if self.__velx > 0:
            self.__face = 1
        elif self.__velx < 0:
            self.__face = -1

        ##### ATUALIZACAO DO CORPO DO JOGADOR #####
        self.__corpo = pygame.Rect(self.__x , self.__y, self.__largura, self.__altura)

    def poderes(self, screen, mapa, bola_fogo = False, outros_poderes = False):
        ##### ATIRA BOLA DE FOGO SE ESTIVER DISPONIVEL
        if bola_fogo == True and self.__recarga == 0: 
            self.__poder.atirar(self,screen,mapa)
            self.__recarga = 24        # TORNAR ESSA PARTE MAIS GENERICA