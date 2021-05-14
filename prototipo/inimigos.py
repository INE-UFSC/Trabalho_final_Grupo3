# Arquivo destinado a fazer todos os inimigos
import pygame
from entidades import *
from poderes import *
from random import randrange


class Inimigo(Entidade):
    def __init__(self, nome, x, y, altura, largura, limiteVel, vida, danoContato, imagem, cor, frames, fogo = False):
        super().__init__(nome, x, y, altura, largura, limiteVel, vida, danoContato, imagem, cor, frames, fogo)


@visivel
@instanciavel
class Bolota(Inimigo):
    "Inimigo comum, anda em uma direcao e muda quando bate"
    nome_imagem = "bolota"
    def __init__(self, x: int, y: int):
        vida = 1
        danoContato = 1
        largura = 46
        altura = 46
        limiteVel = 1
        super().__init__("bolota", x, y, altura, largura, limiteVel, vida, danoContato, "bolota", (88, 51, 0), 25)
        self.vely = 0
        self.velx = 1
        self.xinicial = x
        self.escala_tempo = 1

    def mover(self, dimensoesTela, mapa):
        "Atualiza posicao e velocidade"

        ##### COLISOES #####
        obsCima, obsBaixo, obsDireita, obsEsquerda = self.checar_colisao(mapa.lista_de_entidades, [Bala, PoderNoMapa])

        if obsEsquerda: obsEsquerda.sofreu_colisao_outros(self, "esquerda", mapa)
        if obsDireita: obsDireita.sofreu_colisao_outros(self, "direita", mapa)
        if obsCima: obsCima.sofreu_colisao_outros(self, "cima", mapa)
        if obsBaixo:
            obsBaixo.sofreu_colisao_outros(self, "baixo", mapa)

        ##### GRAVIDADE ######
        else:
            self.vely += gravidade * self.escala_tempo

        self.y += self.vely * self.escala_tempo
        self.x += self.velx * self.escala_tempo


@visivel
@instanciavel
class Espinhento(Inimigo):
    "Inimigo que da dano quando esmagado"
    nome_imagem = "espinhento"
    def __init__(self, x: int, y: int):
        vida = 1
        danoContato = 2
        largura = 48
        altura = 45
        limiteVel = 1
        super().__init__("espinhento", x, y, altura, largura, limiteVel, vida, danoContato, "espinhento", (50, 50, 50), 8)
        self.vely = 0
        self.velx = 0.5
        self.xinicial = x
        self.escala_tempo = 1

    def sofreu_colisao_jogador(self, jogador, direcao, mapa):
        "Detecta colisao com jogador, return dano caso valido"
        ##### COLISAO ESQUERDA #####
        if not jogador.invisivel:
            if direcao == "esquerda":
                if jogador.velx <= 0:
                    jogador.velx = 0
                    jogador.aceleracao = 0
                    jogador.x = self.corpo.right + 1
                return self.dano_contato
            ##### COLISAO DIREITA #####
            elif direcao == "direita":
                if jogador.velx >= 0:
                    jogador.velx = 0
                    jogador.aceleracao = 0
                    jogador.x = self.corpo.left - jogador.largura
                return self.dano_contato
            ##### COLISAO BAIXO #####
            elif direcao == "baixo":
                jogador.vely = 0
                jogador.y = self.corpo.top - jogador.altura
                return self.dano_contato
            ##### COLISAO CIMA #####
            elif direcao == "cima":
                if jogador.vely < 0:
                    jogador.vely = 0
                    jogador.y = self.corpo.bottom
                return self.dano_contato
        else:
            return 0

    def mover(self, dimensoesTela, mapa):
        "Atualiza posicao e velocidade"
        ##### COLISOES #####
        obsCima, obsBaixo, obsDireita, obsEsquerda = self.checar_colisao(mapa.lista_de_entidades, [Bala, PoderNoMapa])

        if obsEsquerda: obsEsquerda.sofreu_colisao_outros(self, "esquerda", mapa)
        if obsDireita: obsDireita.sofreu_colisao_outros(self, "direita", mapa)
        if obsCima: obsCima.sofreu_colisao_outros(self, "cima", mapa)
        if obsBaixo:
            obsBaixo.sofreu_colisao_outros(self, "baixo", mapa)

        ##### GRAVIDADE ######
        else:
            self.vely += gravidade * self.escala_tempo

        self.y += self.vely * self.escala_tempo
        self.x += self.velx * self.escala_tempo


@visivel
@instanciavel
class Voador(Inimigo):
    "Inimigo que voa, ignora o jogador por maior parte"
    nome_imagem = "0"
    def __init__(self, nome: str, x: int, y: int, altitude: int):
        vida = 1
        danoContato = 1
        largura = 26
        altura = 26
        limiteVel = 4
        super().__init__(nome, x, y, altura, largura, limiteVel, vida, danoContato, "0", (88, 51, 0), 0)
        self.altitude = pygame.Rect(x, y + largura + 2, largura,
                                    altura + altitude)  # CAMPO UTILIZADO PARA CHECAR ALTURA DE VOO
        self.vely = 0
        self.velx = 1
        self.xinicial = x
        self.escala_tempo = 1

    def mover(self, dimensoesTela, mapa):
        "Atualiza posicao e velocidade"
        ##### COLISOES #####
        obsCima, obsBaixo, obsDireita, obsEsquerda = self.checar_colisao(mapa.lista_de_entidades,
                                                                         [Bala, PoderNoMapa, Estatico])

        ##### HORIZONTAIS #####
        if obsEsquerda or obsDireita:
            self.velx = self.velx * -1

        ##### VERTICAIS #####
        if obsBaixo or obsCima:
            self.vely = -self.vely

        ##### GRAVIDADE ######
        if (self.altitude.collidelist([x.corpo for x in mapa.lista_de_entidades if x != self]) != -1
                or self.altitude.y + self.altitude.h > dimensoesTela[1]):
            self.vely -= gravidade * self.escala_tempo * 0.2
        else:
            self.vely += gravidade * self.escala_tempo * 0.2

        if self.vely < -1:
            self.vely = -1
        self.y += self.vely * self.escala_tempo
        self.x += self.velx * self.escala_tempo
        self.altitude.x = self.x
        self.altitude.y = self.y + self.largura + 2


@visivel
@instanciavel
class Atirador(Inimigo):
    "Inimigo que atira bolas de fogo periodicamente"
    nome_imagem = "atirador"
    def __init__(self, x: int, y: int, anda = True):
        vida = 1
        danoContato = 1
        largura = 90
        altura = 44
        limiteVel = 4
        super().__init__("atirador", x, y, altura, largura, limiteVel, vida, danoContato, "atirador", (255, 25, 25), 8, True)
        self.vely = 0
        self.velx = 2
        self.__vel_projetil = 3
        self.__anda = anda
        self.xinicial = x
        self.escala_tempo = 1
        self.__poder = Projetil()
        self.__descanso_poder_max = 125
        self.__descanso_poder = randrange(0,25)
        self.__gravidade = 1


    def atualizar(self, tela, mapa, dimensoes_tela):
        "Determina se atira ou nao"
        if self.escala_tempo != mapa.escala_tempo:
            self.escala_tempo += max(min(mapa.escala_tempo - self.escala_tempo, 0.05), -0.05)
        self.mover(dimensoes_tela, mapa)
        self.corpo = pygame.Rect(self.x, self.y, self.largura, self.altura)
        if mapa.campo_visivel.colliderect(self.corpo):
            self.renderizar(tela, mapa)

        #### DETERMINA A VELOCIDADE DO PROJETIL PRA SEGUIR O JOGADOR ####
        if self.corpo.colliderect(mapa.campo_visivel):
            altura_random = 0 #randrange(0, self.altura - 26)
            
            if mapa.jogador.x <= self.x:
                dstancia = (((mapa.jogador.y + mapa.jogador.altura) - (self.y + self.altura)) ** 2 + (
                        mapa.jogador.x - self.x -15*self.face) ** 2) ** (1 / 2)
                divisor = max(dstancia / self.__vel_projetil,0.001)
                velx = (mapa.jogador.x - self.x -15*self.face) / divisor
            else:
                dstancia = (((mapa.jogador.y + mapa.jogador.altura) - (self.y + self.altura)) ** 2 + (
                        mapa.jogador.x - self.corpo.bottomright[0] -15*self.face) ** 2) ** (1 / 2)
                divisor = max(dstancia / self.__vel_projetil,0.001)
                velx = (mapa.jogador.x - self.corpo.bottomright[0] -15*self.face) / divisor
            vely = ((mapa.jogador.y) - (self.y )) / divisor

            if self.__descanso_poder <= 0:
                self.__poder.acao(self, tela, mapa, velx, vely, altura_random)
                self.__descanso_poder = self.__descanso_poder_max + randrange(0, 50)
            else:
                self.__descanso_poder -= 1 * self.escala_tempo
        return False

    def mover(self, dimensoesTela, mapa):
        "Atualiza posicao e velocidade"
        ##### COLISOES #####
        obsCima, obsBaixo, obsDireita, obsEsquerda = self.checar_colisao(mapa.lista_de_entidades, [Bala])

        if obsEsquerda: obsEsquerda.sofreu_colisao_outros(self, "esquerda", mapa)
        if obsDireita: obsDireita.sofreu_colisao_outros(self, "direita", mapa)
        if obsCima: obsCima.sofreu_colisao_outros(self, "cima", mapa)
        if obsBaixo:
            obsBaixo.sofreu_colisao_outros(self, "baixo", mapa)

        ##### GRAVIDADE ######
        else:
            self.vely += self.__gravidade * self.escala_tempo

        

        #### SE NÃO TA NO CAMPO VISIVEL FICA PARADO ####
        if self.corpo.colliderect(mapa.campo_visivel):
            self.velx = 0
            dist_x_jogador = self.x - mapa.jogador.x
            if self.escala_tempo:
                if dist_x_jogador > 0:
                    self.face = -1
                elif dist_x_jogador < 0:
                    self.face = 1
        else:
            self.x += 2 * self.escala_tempo * self.face * self.__anda
        self.y += self.vely * self.escala_tempo


@visivel
@instanciavel
class Saltante(Inimigo):
    "Inimigo que pula de um lado pro outro"
    nome_imagem = "saltante"
    def __init__(self, x: int, y: int):
        vida = 1
        danoContato = 1
        largura = 54
        altura = 99
        limiteVel = 1
        super().__init__("saltante", x, y, altura, largura, limiteVel, vida, danoContato, "saltante", (128, 0, 0), 6)
        #self.vely = 0
        #self.velx = 0
        self.xinicial = x
        self.escala_tempo = 1
        self.__descanso_pulo_max = 145
        self.__descanso_pulo = self.__descanso_pulo_max
        self.__pulo_lado = True
        self.face = -1

    def mover(self, dimensoesTela, mapa):
        "Atualiza posicao e velocidade"
        ##### COISA PRO PULO MAIS PRA FRENTE #####
        vely_buff = self.vely

        ##### COLISOES #####
        obsCima, obsBaixo, obsDireita, obsEsquerda = self.checar_colisao(mapa.lista_de_entidades, [Bala, PoderNoMapa])

        if obsEsquerda: obsEsquerda.sofreu_colisao_outros(self, "esquerda", mapa)
        if obsDireita: obsDireita.sofreu_colisao_outros(self, "direita", mapa)
        if obsCima: obsCima.sofreu_colisao_outros(self, "cima", mapa)
        if obsBaixo:
            obsBaixo.sofreu_colisao_outros(self, "baixo", mapa)


        ##### GRAVIDADE ######
        else:
            self.vely += gravidade * self.escala_tempo

        ##### GERENCIADOR DO PULO #####
        self.__descanso_pulo = (self.__descanso_pulo-1) % self.__descanso_pulo_max

        if not self.__descanso_pulo and obsBaixo:
            self.vely -= 9

        if self.vely : self.velx = self.face * 3 * self.__pulo_lado
        else: self.velx = 0

        if not self.vely and vely_buff:
            if self.__pulo_lado: self.face = -self.face
            self.__pulo_lado = not(self.__pulo_lado)

        ##### REPOSICIONAMENTO #####
        self.y += self.vely * self.escala_tempo
        self.x += self.velx * self.escala_tempo


@visivel
@instanciavel
class Gelatina(Inimigo):
    "Inimigo que nem eh solido, mas deixa lento ao atravessar"
    nome_imagem = "gelatina"
    def __init__(self, x: int, y: int, anda = True):
        vida = 1
        danoContato = 1
        largura = 150
        altura = 150
        limiteVel = 1
        super().__init__("gelatina", x, y, altura, largura, limiteVel, vida, danoContato, "gelatina", (50, 50, 255), 9, True)
        self.vely = 0
        self.velx = 1
        self.xinicial = x
        self.escala_tempo = 1
        self.__anda = anda

    def mover(self, dimensoesTela, mapa):
        "Atualiza posicao e velocidade"
        ##### COLISOES #####
        obsCima, obsBaixo, obsDireita, obsEsquerda = self.checar_colisao(mapa.lista_de_entidades, [Bala, PoderNoMapa, Inimigo])

        if obsEsquerda: obsEsquerda.sofreu_colisao_outros(self, "esquerda", mapa)
        if obsDireita: obsDireita.sofreu_colisao_outros(self, "direita", mapa)
        if obsCima: obsCima.sofreu_colisao_outros(self, "cima", mapa)
        if obsBaixo:
            obsBaixo.sofreu_colisao_outros(self, "baixo", mapa)

        ##### GRAVIDADE ######
        else:
            self.vely += gravidade * self.escala_tempo

        self.y += self.vely * self.escala_tempo
        self.x += self.velx * self.escala_tempo * self.__anda

    def sofreu_colisao_jogador(self, jogador, direcao, mapa):
        "Determina que o jogador fique mais lento ao passar"
        if not jogador.invisivel:
            jogador.escala_tempo = 0.25
        return 0

    def sofreu_colisao_outros(self, entidade, direcao, mapa):
        pass


@visivel
@instanciavel
class Temporal(Inimigo):
    """Inimigo com o mesmo tipo de stand

    Permanece estatico maior parte do tempo, mas eh muito agressivo
    e rapido quando o tempo esta parado, para fazer com que o
    jogador use o poder apenas quando necessario
    """
    nome_imagem = "temporal"
    def __init__(self, x: int, y: int):
        vida = 1
        danoContato = 1
        largura = 59
        altura = 59
        limiteVel = 4
        super().__init__("temporal", x, y, altura, largura, limiteVel, vida, danoContato, "temporal", (80, 10, 120), 15)
        self.vely = 0
        self.xinicial = x
        self.escala_tempo = 0
        self.aceleracao = 1

    def sofreu_colisao_jogador(self, jogador, direcao, mapa):
        ##### COLISAO ESQUERDA #####
        if not jogador.invisivel:
            if direcao == "esquerda":
                if jogador.velx <= 0:
                    jogador.velx = 0
                    jogador.aceleracao = 0
                    jogador.x = self.corpo.right + 1
                return self.dano_contato * (mapa.escala_tempo < 1)
            ##### COLISAO DIREITA #####
            elif direcao == "direita":
                if jogador.velx >= 0:
                    jogador.velx = 0
                    jogador.aceleracao = 0
                    jogador.x = self.corpo.left - jogador.largura
                return self.dano_contato * (mapa.escala_tempo < 1)
            ##### COLISAO BAIXO #####
            elif direcao == "baixo":
                jogador.vely = 0
                jogador.y = self.corpo.top - jogador.altura
                return self.dano_contato * (mapa.escala_tempo < 1)
            ##### COLISAO CIMA #####
            elif direcao == "cima":
                if jogador.vely < 0:
                    jogador.vely = 0
                    jogador.y = self.corpo.bottom
                return self.dano_contato * (mapa.escala_tempo < 1)
        else:
            return 0

    def mover(self, dimensoesTela, mapa):
        "Atualiza posicao e velocidade,mas no tempo parado"
        ##### COLISOES #####
        obsCima, obsBaixo, obsDireita, obsEsquerda = self.checar_colisao(mapa.lista_de_entidades, [Bala, PoderNoMapa])

        if obsEsquerda: obsEsquerda.sofreu_colisao_outros(self, "esquerda", mapa)
        if obsDireita: obsDireita.sofreu_colisao_outros(self, "direita", mapa)
        if obsCima: obsCima.sofreu_colisao_outros(self, "cima", mapa)
        if obsBaixo:
            obsBaixo.sofreu_colisao_outros(self, "baixo", mapa)
            if mapa.jogador.vely < 0 or obsDireita or obsEsquerda:
                self.vely = -10

        ##### GRAVIDADE ######
        else:
            self.vely += gravidade * max(0,(-self.escala_tempo+1))

        if not self.escala_tempo:
            if mapa.jogador.x > self.x:
                self.face = 1
            else:
                self.face = -1

        ##### ACELERACAO #####
        self.velx += self.aceleracao * self.face
        if self.escala_tempo: self.velx = 0
        if self.velx > self.limite_vel:
            self.velx = self.limite_vel
        elif self.velx < - self.limite_vel:
            self.velx = - self.limite_vel

        ##### REPOSICIONALMENTO #####
        self.y += self.vely * max(0,(-self.escala_tempo+1))
        self.x += self.velx * max(0,(-self.escala_tempo+1))

    def renderizar(self, tela, mapa):

        if renderizar_hitbox:
            pygame.draw.rect(tela, self.cor, [self.corpo.x - mapa.campo_visivel.x, self.corpo.y - mapa.campo_visivel.y,
                                              self.corpo.w, self.corpo.h])
        if renderizar_sprite and type(self.sprite) != list:
            self.sprite.imprimir(tela, self.nome, self.x - mapa.campo_visivel.x, self.y - mapa.campo_visivel.y,
                                 self.face, self.velx, self.vely,
                                 int(mapa.ciclo / 6) % self.frames)