import pygame
from obstaculos import Bloco, Vitoria
from entidades import gravidade, colisao_analisada, renderizar_hitbox, renderizar_sprite
from inimigos import Rato
from poderes import *
from sprites import SpriteSheet

class Jogador(Movel):
    def __init__(self, nome: str, x: int, y: int, velx: int, vida: int):
        ##### ATRIBUTOS GERAIS #####
        self.__vida = 100
        self.__nome = nome
        self.__sprite = SpriteSheet("guri")
        self.__posicao_comeco = (x, y)

        ##### ATRIBUTOS POSICIONAIS #####
        altura = 46
        largura = 46
        limite_vel = 5
        self.__face = 1

        ##### ATRIBUTOS COMPORTAMENTAIS #####
        self.__poder = CinzaDoGuri()
        self.__recarga = 0
        self.__invisivel = 0

        super().__init__(nome, x, y, largura, altura, limite_vel, "0")

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
        if renderizar_hitbox: pygame.draw.rect(tela, (50,50,255), [self.corpo.x-campo_visivel.x,self.corpo.y-campo_visivel.y,self.corpo.w,self.corpo.h])
        if renderizar_sprite: self.__sprite.imprimir("guri"+str(ciclo%12), self.x-campo_visivel.x, self.y-campo_visivel.y, tela, self.__face, self.velx)

    def atualizar(self, screen, mapa, campo_visivel, ciclo, entradas, atrito): ### REQUER AREA VISIVEL PARA RENDERIZAR
        self.mover(entradas[0],entradas[1],entradas[2],screen.get_size(),mapa,atrito)

        self.renderizar(screen, campo_visivel, ciclo)

        ##### ATUALIZACAO DOS PODERES #####
        if self.__recarga > 0: self.__recarga -= 1
        self.__invisivel = self.__poder.atualizar(screen,mapa)

        ##### SIDESCROLL #####
        x_min = min(0,campo_visivel.x)
        x_max = max(mapa.tamanho[0]-campo_visivel.w,campo_visivel.x)
        y_min = min(0,campo_visivel.y)
        y_max = max(mapa.tamanho[1]-campo_visivel.h,campo_visivel.y)
        if self.x > campo_visivel.x + 600:
            campo_x = max(0,min((mapa.tamanho[0]-campo_visivel.w,self.x-600)))
            #if campo_visivel.x < mapa.tamanho[0] - campo_visivel.w:
            #    return pygame.Rect(self.x-600,0,campo_visivel.w,campo_visivel.h)
            #else:
            #    return pygame.Rect(mapa.tamanho[0]-campo_visivel.w,0,campo_visivel.w,campo_visivel.h)
        elif self.x < campo_visivel.x + 400:
            campo_x = max(0,min((mapa.tamanho[0]-campo_visivel.w,self.x-400)))
            #if campo_visivel.x > 0:
            #    return pygame.Rect(self.x-400,0,campo_visivel.w,campo_visivel.h)
            #else:
            #    return pygame.Rect(0,0,campo_visivel.w,campo_visivel.h)
        else:
            campo_x = campo_visivel.x
        if self.y > campo_visivel.y + 300:
            campo_y = max(0,min((mapa.tamanho[1]-campo_visivel.h,self.y-300)))
        elif self.y < campo_visivel.y + 200:
            campo_y = max(0,min((mapa.tamanho[1]-campo_visivel.h,self.y-200)))
        else:
            campo_y = campo_visivel.y
        return pygame.Rect(campo_x,campo_y,campo_visivel.w,campo_visivel.h)

    def mover(self, direita, esquerda, espaco, screen, mapa, atrito):

        ##### MOVIMENTO HORIZONTAL #####
        aceleracao = (direita - esquerda)
        self.velx += aceleracao

        ##### COLISOES #####
        coletaveis = [CartolaDoMago, BandanaDoNinja, OculosDoNerd, BoneMarinheiro, VerdeBebe] #Tipos coletaveis

        #0-Cima, 1-Baixo, 2-Direita, 3-Esquerda
        obstaculos = self.checar_colisao(mapa.lista_de_entidades, [BolaFogo, Vitoria])

        ##### PERMITE
        if self.__invisivel:
            for i in range(len(obstaculos)):
                if isinstance(obstaculos[i],Entidade): 
                    obstaculos[i] = 0


        ##### COLETA ITENS #####
        for i in range(len(obstaculos)):
            if type(obstaculos[i]) in coletaveis:
                self.coletar(obstaculos[i])
                mapa.escala_tempo = 1
                obstaculos[i].auto_destruir(mapa)
                obstaculos[i] = False

        ##### REPOSICIONAMENTO POS COLISAO #####
        if obstaculos[2] and obstaculos[3]: #ESMAGAMENTO
            self.__vida = 0 #AQUI EH TESTE N SEI SE ESSA VARIAVEL VAI FICAR COMO STRING MSM

        ##### COLISAO ESQUERDA #####
        if obstaculos[3]:
            #print("COLISAO PELA ESQUERDA", obsEsquerda.nome)
            if self.velx <= 0:
                self.velx = 0
                aceleracao = 0
                self.x = obstaculos[3].corpo.right+1
        if self.x <= 0:
            if self.velx <= 0:
                self.velx = 0
                aceleracao = 0
                self.x = 0
        ##### COLISAO DIREITA #####
        if obstaculos[2]:
            #print("COLISAO PELA DIREITA", obsDireita.nome)
            if self.velx >= 0:
                self.velx = 0
                aceleracao = 0
                self.x = obstaculos[2].corpo.left - self.largura
        if self.x >= mapa.tamanho[0]-self.largura:
            if self.velx >= 0:
                self.velx = 0
                aceleracao = 0
                self.x = mapa.tamanho[0]-self.largura

        ##### COLISAO BAIXO #####
        if obstaculos[1]:
            self.vely = 0
            self.y = obstaculos[1].corpo.top - self.altura
            if espaco:
                self.vely = -self.poder.pulo

        ##### COLISAO CIMA #####
        if obstaculos[0]:
            if self.vely < 0:
                self.vely = 0
                self.y = obstaculos[0].corpo.bottom

        #### COLISAO INIMIGOS ####
        if not self.__invisivel:
            for entidade in mapa.lista_de_entidades:
                for i in range (len(obstaculos)):
                    if isinstance(obstaculos[i], Entidade):
                        if obstaculos[i] == entidade:
                            if entidade.contato[i] == 'morrer':
                                entidade.auto_destruir(mapa)

                            elif entidade.contato[i] == 'dano':
                                ##EMPURRA O JOGGADOR
                                if self.face == 1:
                                    self.x = self.__posicao_comeco[0]
                                    self.y = self.__posicao_comeco[1]
                                else: 
                                    self.x = self.__posicao_comeco[0]
                                    self.y = self.__posicao_comeco[1]
 
                                if self.__poder != CinzaDoGuri():
                                    self.__poder = CinzaDoGuri()
                                self.__vida -= entidade.dano_contato

        ### CHECANDO VITÓRIA ###
        entidade_vitoria = 0
        for ganhar in mapa.lista_de_entidades:
            if isinstance(ganhar, Vitoria):
                entidade_vitoria = ganhar

        if self.corpo.colliderect(entidade_vitoria.corpo):
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
        # entrando no castelo #
        if mapa.ganhou:
            dist_meio_vitoria = entidade_vitoria.corpo.centerx - self.corpo.right
            if dist_meio_vitoria < 0:
                self.velx = -1
            elif dist_meio_vitoria > 0:
                self.velx = 1
            else:
                self.velx = 0

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
        if self.y > mapa.tamanho[1]: self.__vida = 0

        ##### INDICA A DIRECAO DO JOGADOR PARA DIRECIONAR PODERES #####
        if self.velx > 0:
            self.__face = 1
        elif self.velx < 0:
            self.__face = -1

        ##### ATUALIZACAO DO CORPO DO JOGADOR #####
        self.corpo = pygame.Rect(self.x , self.y, self.largura, self.altura)

    def poderes(self, screen, mapa, acao = False, outros_poderes = False):
        ##### ATIRA BOLA DE FOGO SE ESTIVER DISPONIVEL
        if acao and not self.poder.descanso:
            self.__poder.acao(self,screen,mapa)
