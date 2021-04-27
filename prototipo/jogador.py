import pygame
from obstaculos import Bloco
from entidades import gravidade, colisao_analisada
from poder_generico import BolaFogo,VermelhoDoMago

class Jogador: 
    def __init__(self, nome: str, x: int, y: int, velx: int, vida: int):
        self.__vida = vida
        self.__nome = nome
        self.__cor = (0,0,0)
        self.__x = x
        self.__y = y
        self.__altura = 50
        self.__largura = 25
        self.__pulo = 9
        self.__velx = velx
        self.__vely = 0
        self.__corpo = pygame.Rect(self.__x , self.__y, self.__largura, self.__altura)
        self.__corpoveloz = pygame.Rect(self.__x , self.__y, self.__largura, self.__altura)
        self.__poder = VermelhoDoMago()
        self.__velocidade_max = 5
        self.__velocidade_min = -5
        self.__recarga = 0
        self.__face = 1

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
    def vida(self):
        return self.__vida
    
    @property
    def face(self):
        return self.__face

    def checar_colisao(self, corpo, nome):
        colisaoBaixo, colisaoCima, colisaoEsquerda, colisaoDireita = False, False, False, False
        if self.__velx < 0: # movimento para a esquerda
            cveloz_left = self.__corpo.left-1+self.__velx
            cveloz_largura = self.__corpo.right - cveloz_left + 1
        else: # movimento para a direita
            cveloz_left = self.__corpo.left - 1
            cveloz_largura = self.__corpo.right - cveloz_left + 1 + self.__velx
        if self.__vely < 0: # movimento para cima
            cveloz_top = self.__corpo.top - 1 + self.__vely
            cveloz_altura = self.__corpo.bottom - cveloz_top + 1
        else: #  movimento para baixo
            cveloz_top = self.__corpo.top
            cveloz_altura = self.__corpo.bottom - cveloz_top + 1 + self.__vely
        self.__corpoveloz = pygame.Rect(cveloz_left, cveloz_top, cveloz_largura, cveloz_altura)
        colisaoVeloz = self.__corpoveloz.colliderect(corpo)

        if colisaoVeloz:
            # CALCULO DE O QUAO DENTRO O OBJETO TA HORIZONTALMENTE E VERTICALMENTE
            ##### VERTICIAIS #####
            dist_y = 0
            if not self.__vely: #parado
                if nome == colisao_analisada: print("parado")
                dist_y = min(self.__corpoveloz.bottom-corpo.top,corpo.bottom-self.__corpoveloz.top)
            elif self.__vely > 0: #caindo
                if nome == colisao_analisada: print("caindo")
                dist_y = self.__corpoveloz.bottom-corpo.top
            else: #subindo
                if nome == colisao_analisada: print("subindo")
                dist_y = corpo.bottom-self.__corpoveloz.top
            dist_x = 0
            ##### HORIZONTAL #####
            if not self.__velx: #parado
                dist_x = min(corpo.right - self.__corpoveloz.left,self.__corpoveloz.right - corpo.left) #colisao a direita = +
            elif self.__velx > 0: #movimentacao pra direita
                dist_x = self.__corpoveloz.right - corpo.left
            else: #movimentacao pra esquerda
                dist_x = corpo.right - self.__corpoveloz.left

            if nome == colisao_analisada: print(nome, dist_x, dist_y, self.__velx, self.__vely)
            if self.__vely >= 0 and dist_x + self.__largura/2 >= dist_y:
                colisaoBaixo = True
            elif self.__vely < 0 and dist_x + self.__largura/2 >= dist_y:
                colisaoCima = True
            elif self.__velx > 0 and dist_x < dist_y:
                colisaoDireita = True
            elif self.__velx < 0 and dist_x < dist_y:
                colisaoEsquerda = True
            elif not self.__velx and abs(dist_x) < dist_y:
                print("buff", dist_x)
                if self.__corpoveloz.right - corpo.left > corpo.right - self.__corpoveloz.left:
                    colisaoEsquerda = True
                else: colisaoDireita = True
            if nome == colisao_analisada: print("------")

        if colisaoVeloz and nome == colisao_analisada: print(int(colisaoCima), int(colisaoBaixo), int(colisaoDireita), int(colisaoEsquerda))
        return [colisaoCima, colisaoBaixo, colisaoDireita, colisaoEsquerda]

    @property
    def poder(self):
        return self.__poder
    
    def poder(self, poder):
        self.__poder = poder
    
    def atualizar(self, screen):
        pygame.draw.rect(screen, (0, 0, 255), self.__corpoveloz)
        pygame.draw.rect(screen, self.__cor, self.__corpo)
        if self.__recarga > 0:
            self.__recarga -= 1
        if self.__poder != '':
            self.__poder.atualizar(screen)
    
    def mover(self, direita, esquerda, espaco, screen, mapa, atrito):

        ##### MOVIMENTO HORIZONTAL #####
        aceleracao = direita - esquerda
        self.__velx += aceleracao

        ##### COLISOES #####
        colisaoCima, colisaoBaixo, colisaoEsquerda, colisaoDireita = False, False, False, False
        cCima, cBaixo, cEsquerda, cDireita = False, False, False, False
        obsBaixo, obsCima, obsEsquerda, obsDireita = 0,0,0,0

        ##### COLISOES COM OBSTACULOS #####
        for obstaculo in mapa.lista_de_obstaculos:

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

        for inimigo in mapa.lista_de_inimigos:
            cCima, cBaixo, cDireita, cEsquerda = self.checar_colisao(inimigo.corpo, inimigo.nome)

            # Essa checagem em dois passos tem que ocorrer por que se nao ele so salva a colisao com o utlimo obstaculo
            if cCima:
                colisaoCima = True
                obsCima = inimigo
            if cBaixo:
                colisaoBaixo = True
                obsBaixo = inimigo
            if cEsquerda:
                colisaoEsquerda = True
                obsEsquerda = inimigo
            if cDireita:
                colisaoDireita = True
                obsDireita = inimigo

        ##### REPOSICIONAMENTO POS COLISAO #####
        if colisaoDireita and colisaoEsquerda: #ESMAGAMENTO
            self.__vida = "morto" #AQUI EH TESTE N SEI SE ESSA VARIAVEL VAI FICAR COMO STRING MSM

        if colisaoEsquerda:
            if self.__velx <= 0:
                self.__velx = 0
                aceleracao = 0
                self.__x = obsEsquerda.corpo.right

        if colisaoDireita:
            if self.__velx >= 0:
                self.__velx = 0
                aceleracao = 0
                self.__x = obsDireita.corpo.left - self.__largura

        if colisaoBaixo:
            self.__vely = 0
            self.__y = obsBaixo.corpo.top - self.__altura
            if espaco:
                self.__vely = -self.__pulo

        if colisaoCima:
            if self.__vely < 0:
                print("AQUI")
                self.__vely = 0
                self.__y = obsCima.corpo.bottom

        ##### GRAVIDADE ######
        if not colisaoBaixo: self.__vely += gravidade

        ##### ATRITO ######
        if aceleracao == 0:
            if self.__velx < 0:
                self.__velx += atrito
            elif self.__velx > 0:
                self.__velx -= atrito
        #else:
            #self.__velx = 0
        if self.__velx >= self.__velocidade_max:
            self.__velx = self.__velocidade_max
        elif self.__velx <= self.__velocidade_min:
            self.__velx = self.__velocidade_min 

        ##### ATUALIZACAO DE POSICOES #####
        self.__y += self.__vely
        self.__x += self.__velx

        ##### MATA O JOGADOR SE CAIR NO BURACO #####
        if self.__y > screen[1]: self.__vida = "morto"

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