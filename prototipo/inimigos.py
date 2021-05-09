# Arquivo destinado a fazer todos os inimigos
import pygame
from entidades import *
from poderes import *


@instanciavel
class Rato(Entidade):
    def __init__(self, nome: str, x: int, y: int):
        vida = 1
        danoContato = 1
        largura = 46
        altura = 46
        limiteVel = 1
        super().__init__(nome, x, y, largura, altura, limiteVel, vida, danoContato, "0", (88, 51, 0))
        self.vely = 0
        self.velx = 1
        self.xinicial = x
        self.escala_tempo = 1

    def mover(self, dimensoesTela, mapa):

        ##### COLISOES #####
        obsCima, obsBaixo, obsDireita, obsEsquerda = self.checar_colisao(mapa.lista_de_entidades, [Bala, PoderNoMapa])

        if obsEsquerda: obsEsquerda.sofreu_colisao_outros(self, "esquerda")
        if obsDireita: obsDireita.sofreu_colisao_outros(self, "direita")
        if obsCima: obsCima.sofreu_colisao_outros(self, "cima")
        if obsBaixo:
            obsBaixo.sofreu_colisao_outros(self, "baixo")

        ##### GRAVIDADE ######
        else:
            self.vely += gravidade * self.escala_tempo

        self.y += self.vely * self.escala_tempo
        self.x += self.velx * self.escala_tempo


@instanciavel
class PorcoEspinho(Entidade):
    def __init__(self, nome: str, x: int, y: int):
        vida = 1
        danoContato = 2
        largura = 46
        altura = 46
        limiteVel = 1
        super().__init__(nome, x, y, largura, altura, limiteVel, vida, danoContato, "0", (50, 50, 50))
        self.vely = 0
        self.velx = 0.5
        self.xinicial = x
        self.escala_tempo = 1

    def sofreu_colisao_jogador(self, jogador, direcao, mapa):
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
                self.auto_destruir(mapa)
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
        ##### COLISOES #####
        obsCima, obsBaixo, obsDireita, obsEsquerda = self.checar_colisao(mapa.lista_de_entidades, [Bala, PoderNoMapa])

        if obsEsquerda: obsEsquerda.sofreu_colisao_outros(self, "esquerda")
        if obsDireita: obsDireita.sofreu_colisao_outros(self, "direita")
        if obsCima: obsCima.sofreu_colisao_outros(self, "cima")
        if obsBaixo:
            obsBaixo.sofreu_colisao_outros(self, "baixo")

        ##### GRAVIDADE ######
        else:
            self.vely += gravidade * self.escala_tempo

        self.y += self.vely * self.escala_tempo
        self.x += self.velx * self.escala_tempo


@instanciavel
class Voador(Entidade):
    def __init__(self, nome: str, x: int, y: int, altitude: int):
        vida = 1
        danoContato = 1
        largura = 26
        altura = 26
        limiteVel = 4
        super().__init__(nome, x, y, largura, altura, limiteVel, vida, danoContato, "0", (88, 51, 0))
        self.altitude = pygame.Rect(x, y + largura + 2, largura,
                                    altura + altitude)  # CAMPO UTILIZADO PARA CHECAR ALTURA DE VOO
        self.vely = 0
        self.velx = 1
        self.xinicial = x
        self.escala_tempo = 1

    def mover(self, dimensoesTela, mapa):

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


@instanciavel
class Atirador(Entidade):
    def __init__(self, nome: str, x: int, y: int):
        vida = 1
        danoContato = 1
        largura = 40
        altura = 66
        limiteVel = 4
        super().__init__(nome, x, y, largura, altura, limiteVel, vida, danoContato, "0", (255, 25, 25))
        self.vely = 0
        self.velx = 2
        self.__vel_projetil = 3
        self.xinicial = x
        self.escala_tempo = 1
        self.__poder = Projetil()
        self.__descanso_poder = 300
        self.__gravidade = 1


    def atualizar(self, tela, mapa, dimensoes_tela):
        if self.escala_tempo != mapa.escala_tempo:
            self.escala_tempo += max(min(mapa.escala_tempo - self.escala_tempo, 0.05), -0.05)
        self.mover(dimensoes_tela, mapa)
        self.corpo = pygame.Rect(self.x, self.y, self.largura, self.altura)
        if mapa.campo_visivel.colliderect(self.corpo):
            self.renderizar(tela, mapa)

        #### DETERMINA A VELOCIDADE DO PROJETIL PRA SEGUIR O JOGADOR ####
        dstancia = (((mapa.jogador.y + mapa.jogador.altura) - (self.y + self.altura)) ** 2 + (
                mapa.jogador.x - self.x) ** 2) ** (1 / 2)
        divisor = max(dstancia / self.__vel_projetil,0.001)
        vely = ((mapa.jogador.y + mapa.jogador.altura) - (self.y + self.altura)) / divisor
        velx = (mapa.jogador.x - self.x) / divisor
        if self.corpo.colliderect(mapa.campo_visivel):
            if self.__descanso_poder <= 0:
                self.__poder.acao(self, tela, mapa, velx, vely)
                self.__descanso_poder = 300
            else:
                self.__descanso_poder -= 1 * self.escala_tempo
        return False

    def mover(self, dimensoesTela, mapa):
        ##### COLISOES #####
        obsCima, obsBaixo, obsDireita, obsEsquerda = self.checar_colisao(mapa.lista_de_entidades, [Bala])

        if obsEsquerda: obsEsquerda.sofreu_colisao_outros(self, "esquerda")
        if obsDireita: obsDireita.sofreu_colisao_outros(self, "direita")
        if obsCima: obsCima.sofreu_colisao_outros(self, "cima")
        if obsBaixo:
            obsBaixo.sofreu_colisao_outros(self, "baixo")

        ##### GRAVIDADE ######
        else:
            self.vely += self.__gravidade * self.escala_tempo

        

        #### SE NÃO TA NO CAMPO VISIVEL FICA PARADO ####
        if self.corpo.colliderect(mapa.campo_visivel):
            self.velx = 0
            dist_x_jogador = self.x - mapa.jogador.x
            if dist_x_jogador > 0:
                self.face = -1
            elif dist_x_jogador < 0:
                self.face = 1
        else:
            self.x += 2 * self.escala_tempo * self.face
        self.y += self.vely * self.escala_tempo


@instanciavel
class Coelho(Entidade):
    def __init__(self, nome: str, x: int, y: int):
        vida = 1
        danoContato = 1
        largura = 46
        altura = 60
        limiteVel = 1
        super().__init__(nome, x, y, altura, largura, limiteVel, vida, danoContato, "0", (128, 0, 0))
        #self.vely = 0
        #self.velx = 0
        self.xinicial = x
        self.escala_tempo = 1
        self.__descanso_pulo_max = 150
        self.__descanso_pulo = self.__descanso_pulo_max
        self.__pulo_lado = True
        self.face = -1

    def mover(self, dimensoesTela, mapa):

        ##### COISA PRO PULO MAIS PRA FRENTE #####
        vely_buff = self.vely

        ##### COLISOES #####
        obsCima, obsBaixo, obsDireita, obsEsquerda = self.checar_colisao(mapa.lista_de_entidades, [Bala, PoderNoMapa])

        if obsEsquerda: obsEsquerda.sofreu_colisao_outros(self, "esquerda")
        if obsDireita: obsDireita.sofreu_colisao_outros(self, "direita")
        if obsCima: obsCima.sofreu_colisao_outros(self, "cima")
        if obsBaixo:
            obsBaixo.sofreu_colisao_outros(self, "baixo")


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

    # def sofreu_colisao_jogador(self, jogador, direcao, mapa):
    #     ##### COLISAO ESQUERDA #####
    #     if not jogador.invisivel:
    #         if direcao == "esquerda":
    #             if jogador.velx <= 0:
    #                 jogador.velx = 0
    #                 jogador.aceleracao = 0
    #                 jogador.x = self.corpo.right + 1
    #             return self.dano_contato
    #         ##### COLISAO DIREITA #####
    #         elif direcao == "direita":
    #             if jogador.velx >= 0:
    #                 jogador.velx = 0
    #                 jogador.aceleracao = 0
    #                 jogador.x = self.corpo.left - jogador.largura
    #             return self.dano_contato
    #         ##### COLISAO BAIXO #####
    #         elif direcao == "baixo":
    #             jogador.vely = 0
    #             jogador.y = self.corpo.top - jogador.altura
    #             self.auto_destruir(mapa)
    #             return 0
    #         ##### COLISAO CIMA #####
    #         elif direcao == "cima":
    #             #if jogador.vely < 0:
    #             #    jogador.vely = 0
    #             #    jogador.y = self.corpo.bottom
    #             return self.dano_contato
    #     else:
    #         return 0

@instanciavel
class Gelatina(Entidade):
    def __init__(self, nome: str, x: int, y: int):
        vida = 1
        danoContato = 1
        largura = 150
        altura = 150
        limiteVel = 1
        super().__init__(nome, x, y, largura, altura, limiteVel, vida, danoContato, "0", (50, 50, 255))
        self.vely = 0
        self.velx = 1
        self.xinicial = x
        self.escala_tempo = 1

    def mover(self, dimensoesTela, mapa):

        ##### COLISOES #####
        obsCima, obsBaixo, obsDireita, obsEsquerda = self.checar_colisao(mapa.lista_de_entidades, [Bala, PoderNoMapa, Entidade])

        if obsEsquerda: obsEsquerda.sofreu_colisao_outros(self, "esquerda")
        if obsDireita: obsDireita.sofreu_colisao_outros(self, "direita")
        if obsCima: obsCima.sofreu_colisao_outros(self, "cima")
        if obsBaixo:
            obsBaixo.sofreu_colisao_outros(self, "baixo")

        ##### GRAVIDADE ######
        else:
            self.vely += gravidade * self.escala_tempo

        self.y += self.vely * self.escala_tempo
        self.x += self.velx * self.escala_tempo

    def sofreu_colisao_jogador(self, jogador, direcao, mapa):
        if not jogador.invisivel:
            jogador.escala_tempo = 0.25
        return 0

    def sofreu_colisao_outros(self, entidade, direcao):
        pass