import pygame
from obstaculos import Bloco, Vitoria
from entidades import gravidade, colisao_analisada, renderizar_hitbox, renderizar_sprite
from inimigos import Goomba
from poderes import *
from sprites import SpriteSheet

class Jogador(Movel):
    def __init__(self, nome: str, x: int, y: int, velx: int, vida: int):
        ##### ATRIBUTOS GERAIS #####
        self.__vida = 10
        self.__nome = nome
        self.__imagem = SpriteSheet("andando")

        ##### ATRIBUTOS POSICIONAIS #####
        altura = 46
        largura = 46
        limite_vel = 5
        self.__velx = velx
        self.__vely = 0
        self.__face = 1

        ##### ATRIBUTOS COMPORTAMENTAIS #####
        self.__poder = PretoDoNinja()
        self.__recarga = 0

        super().__init__(nome, x, y, largura, altura, limite_vel)

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

    def coletar(self, item):
        if isinstance(item,PoderNoMapa):
            self.poder = item.poder_atribuido

    def renderizar(self, tela, campo_visivel, ciclo):
        if renderizar_hitbox: pygame.draw.rect(tela, (0,0,0), [self.corpo.x-campo_visivel.x,self.corpo.y,self.corpo.w,self.corpo.h])
        if renderizar_sprite: self.__imagem.imprimir("andando"+str(ciclo%12), self.x-campo_visivel.x, self.y, tela, self.__face)

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
        self.velx += aceleracao

        ##### COLISOES #####
        coletaveis = [OrbeDoMago, ShurikenDoNinja] #Tipos coletaveis

        #0-Cima, 1-Baixo, 2-Direita, 3-Esquerda
        obstaculos = self.checar_colisao(mapa.lista_de_entidades, [BolaFogo])

        ##### COLETA ITENS #####
        for i in range(len(obstaculos)):
            if type(obstaculos[i]) in coletaveis:
                self.coletar(obstaculos[i])
                obstaculos[i].auto_destruir(mapa)
                obstaculos[i] = False

        ##### REPOSICIONAMENTO POS COLISAO #####
        if obstaculos[2] and obstaculos[3]: #ESMAGAMENTO
            self.__vida = 0 #AQUI EH TESTE N SEI SE ESSA VARIAVEL VAI FICAR COMO STRING MSM

        if obstaculos[3]:
            #print("COLISAO PELA ESQUERDA", obsEsquerda.nome)
            if self.velx <= 0:
                self.velx = 0
                aceleracao = 0
                self.x = obstaculos[3].corpo.right+1

        if obstaculos[2]:
            #print("COLISAO PELA DIREITA", obsDireita.nome)
            if self.velx >= 0:
                self.velx = 0
                aceleracao = 0
                self.x = obstaculos[2].corpo.left - self.largura

        if obstaculos[1]:
            self.vely = 0
            self.y = obstaculos[1].corpo.top - self.altura
            if espaco:
                self.vely = -self.poder.pulo

        if obstaculos[0]:
            if self.vely < 0:
                self.vely = 0
                self.y = obstaculos[0].corpo.bottom

        #### COLISAO GOOMBA ####
        for cada_termo in mapa.lista_de_entidades: 
            if isinstance (cada_termo, Goomba):
                entidade = cada_termo
        
                if obstaculos[3] != 0:
                    if isinstance(obstaculos[3], Goomba):
                        self.__vida -= entidade.dano_contato
                
                if obstaculos[2] != 0:
                    if isinstance(obstaculos[2], Goomba):
                        self.__vida -= entidade.dano_contato

        ### CHECANDO VITÓRIA ###
        for cada_termo in mapa.lista_de_entidades: 
            if isinstance (cada_termo, Vitoria):
                entidade = cada_termo

                if obstaculos[3] != 0:
                    if isinstance(obstaculos[3], Vitoria):
                        mapa.ganhou = True

                if obstaculos[2] != 0:
                    if isinstance(obstaculos[2], Vitoria):
                        mapa.ganhou = True

                if obstaculos[1] != 0:
                    if isinstance(obstaculos[1], Vitoria):
                        mapa.ganhou = True

        ##### GRAVIDADE ######
        if not obstaculos[1]: self.vely += gravidade

        ##### ATRITO ######
        if aceleracao == 0:
            if self.velx < 0:
                self.velx += atrito
            elif self.velx > 0:
                self.velx -= atrito

        ##### AJUSTE DE VELOCIDADE MAXIMA #####
        if self.velx > self.poder.limite_vel:
            if self.velx > self.poder.limite_vel + 1:
                self.velx -= 1
            else:
                self.velx = self.poder.limite_vel

        elif self.velx < -self.poder.limite_vel:
            if self.velx < -self.poder.limite_vel - 1:
                self.velx += 1
            else:
                self.velx = -self.poder.limite_vel

        ##### ATUALIZACAO DE POSICOES #####
        self.y += self.vely
        self.x += self.velx

        ##### MATA O JOGADOR SE CAIR NO BURACO #####
        if self.y > screen[1]: self.__vida = 0

        ##### INDICA A DIRECAO DO JOGADOR PARA DIRECIONAR PODERES #####
        if self.velx > 0:
            self.__face = 1
        elif self.velx < 0:
            self.__face = -1

        ##### ATUALIZACAO DO CORPO DO JOGADOR #####
        self.corpo = pygame.Rect(self.x , self.y, self.largura, self.altura)

    def poderes(self, screen, mapa, acao = False, outros_poderes = False):
        ##### ATIRA BOLA DE FOGO SE ESTIVER DISPONIVEL
        if acao and not self.__recarga:
            self.__poder.acao(self,screen,mapa)
            self.__recarga = self.poder.recarga        # TORNAR ESSA PARTE MAIS GENERICA