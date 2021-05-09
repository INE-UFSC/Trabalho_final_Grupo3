import pygame
from obstaculos import Bloco, Vitoria
from entidades import gravidade, colisao_analisada, renderizar_hitbox, renderizar_sprite
from inimigos import Rato
from poderes import *
from sprites import Sprite


class Jogador(Movel):
    def __init__(self, nome: str, x: int, y: int, velx: int, vida: int):
        ##### ATRIBUTOS GERAIS #####
        self.__vida = 5
        self.__nome = nome
        self.__sprite = {"cinza": Sprite("rabisco_cinza"),
                         "laranja": Sprite("rabisco_laranja"),
                         "vermelho": Sprite("rabisco_vermelho"),
                         "roxo": Sprite("rabisco_roxo"),
                         "azul": Sprite("rabisco_azul"),
                         "verde": Sprite("rabisco_verde"),
                         "marrom": Sprite("rabisco_marrom")}
        self.__posicao_comeco = (x, y)
        self.__tipos_transparentes = [BolaFogo, Vitoria]

        ##### ATRIBUTOS POSICIONAIS #####
        altura = 46
        largura = 46
        limite_vel = 5
        self.__tamanho_jogador = (altura, largura)
        self.__aceleracao = 0

        ##### ATRIBUTOS COMPORTAMENTAIS #####
        self.__poder = Cinza()
        self.__recuperacao = 0
        self.__recarga = 0
        self.__invisivel = 0
        self.__moedas = 0
        self.__escala_tempo = 1

        super().__init__(nome, x, y, largura, altura, limite_vel, "0")

    @property
    def invisivel(self):
        return self.__invisivel

    @property
    def tamanho_jogador(self):
        return self.__tamanho_jogador

    @tamanho_jogador.setter
    def tamanho_jogador(self, tamanho_jogador):
        self.__tamanho_jogador = tamanho_jogador

    @property
    def poder(self):
        return self.__poder

    @poder.setter
    def poder(self, poder):
        self.__poder = poder

    @property
    def moedas(self):
        return self.__moedas

    @moedas.setter
    def moedas(self, moedas):
        self.__moedas = moedas

    @property
    def aceleracao(self):
        return self.__aceleracao

    @aceleracao.setter
    def aceleracao(self, aceleracao):
        self.__aceleracao = aceleracao

    @property
    def posicao_comeco(self):
        return self.__posicao_comeco

    @posicao_comeco.setter
    def posicao_comeco(self, posicao_comeco):
        self.__posicao_comeco = posicao_comeco

    @property
    def vida(self):
        return self.__vida

    @property
    def tipos_transparentes(self):
        return self.__tipos_transparentes
    
    @tipos_transparentes.setter
    def tipos_transparentes(self,tipos):
        self.__tipos_transparentes = tipos
    
    @property
    def recuperacao(self):
        return self.__recuperacao

    @property
    def escala_tempo(self):
        return self.__escala_tempo

    @escala_tempo.setter
    def escala_tempo(self, escala_tempo):
        self.__escala_tempo = escala_tempo

    def vida_pra_zero(self):
        self.__vida = 0

    def coletar_poder(self, item):
        self.poder = item.poder_atribuido

    def coletar_moeda(self):
        self.__moedas += 1


    def renderizar(self, tela, campo_visivel, ciclo):
    
        if renderizar_hitbox:
            pygame.draw.rect(tela, (50, 50, 255),[self.corpo.x - campo_visivel.x, self.corpo.y - campo_visivel.y,
                                                self.corpo.w, self.corpo.h])
        if renderizar_sprite:
            if self.recuperacao % 15 < 10:
                self.__sprite[type(self.poder).__name__.lower()].imprimir(tela, "rabisco", self.x - campo_visivel.x, self.y - campo_visivel.y,
                                self.face, self.velx, self.vely, ciclo % 12)

    def atualizar(self, screen, mapa, campo_visivel, ciclo, entradas, atrito):  ### REQUER AREA VISIVEL PARA RENDERIZAR
        self.mover(entradas[0], entradas[1], entradas[2], screen.get_size(), mapa, atrito)

        self.renderizar(screen, campo_visivel, ciclo)

        ##### ATUALIZACAO DOS PODERES #####
        if self.__recarga > 0: self.__recarga -= 1
        self.__invisivel = self.__poder.atualizar(screen, mapa)

        ##### SIDESCROLL #####
        x_min = min(0, campo_visivel.x)
        x_max = max(mapa.tamanho[0] - campo_visivel.w, campo_visivel.x)
        y_min = min(0, campo_visivel.y)
        y_max = max(mapa.tamanho[1] - campo_visivel.h, campo_visivel.y)
        if self.x > campo_visivel.x + 600:
            campo_x = max(0, min((mapa.tamanho[0] - campo_visivel.w, self.x - 600)))
            # if campo_visivel.x < mapa.tamanho[0] - campo_visivel.w:
            #    return pygame.Rect(self.x-600,0,campo_visivel.w,campo_visivel.h)
            # else:
            #    return pygame.Rect(mapa.tamanho[0]-campo_visivel.w,0,campo_visivel.w,campo_visivel.h)
        elif self.x < campo_visivel.x + 400:
            campo_x = max(0, min((mapa.tamanho[0] - campo_visivel.w, self.x - 400)))
            # if campo_visivel.x > 0:
            #    return pygame.Rect(self.x-400,0,campo_visivel.w,campo_visivel.h)
            # else:
            #    return pygame.Rect(0,0,campo_visivel.w,campo_visivel.h)
        else:
            campo_x = campo_visivel.x
        if self.y > campo_visivel.y + 300:
            campo_y = max(0, min((mapa.tamanho[1] - campo_visivel.h, self.y - 300)))
        elif self.y < campo_visivel.y + 200:
            campo_y = max(0, min((mapa.tamanho[1] - campo_visivel.h, self.y - 200)))
        else:
            campo_y = campo_visivel.y
        return pygame.Rect(campo_x, campo_y, campo_visivel.w, campo_visivel.h)

    def respawn(self):
        ##### EMPURRA O JOGADOR #####
        self.x = self.posicao_comeco[0]
        self.y = self.posicao_comeco[1]

    def mover(self, direita, esquerda, espaco, screen, mapa, atrito):

        ##### ATUALIZACAO DA LENTIDAO #####
        self.__escala_tempo = 1

        ##### MOVIMENTO HORIZONTAL #####
        self.__aceleracao = (direita - esquerda)
        self.velx += self.__aceleracao

        ##### COLISOES #####
        # 0-Cima, 1-Baixo, 2-Direita, 3-Esquerda
        obsCima, obsBaixo, obsDireita, obsEsquerda = self.checar_colisao(mapa.lista_de_entidades, self.__tipos_transparentes)
        obstaculos = [obsCima, obsBaixo, obsDireita, obsEsquerda]
        dano_total = 0

        if obsCima:
            dano_sofrido = obsCima.sofreu_colisao_jogador(self, "cima", mapa)
            dano_total += dano_sofrido
        if obsBaixo:
            dano_sofrido = obsBaixo.sofreu_colisao_jogador(self, "baixo", mapa)
            dano_total += dano_sofrido
        if obsDireita:
            dano_sofrido = obsDireita.sofreu_colisao_jogador(self, "direita", mapa)
            dano_total += dano_sofrido
        if obsEsquerda:
            dano_sofrido = obsEsquerda.sofreu_colisao_jogador(self, "esquerda", mapa)
            dano_total += dano_sofrido

        if not self.invisivel:
            if dano_total and not self.__recuperacao and mapa.escala_tempo > 0:
                self.__vida -= dano_total
                self.__recuperacao = 90
            elif self.__recuperacao > 0:
                self.__recuperacao -= 1


        ##### PERMITE
        if self.__invisivel:
            for i in range(len(obstaculos)):
                if isinstance(obstaculos[i], Entidade):
                    obstaculos[i] = 0

        ##### COLETA ITENS #####
        for i in range(len(obstaculos)):
            if isinstance(obstaculos[i], Coletavel):
                obstaculos[i].coleta(self, mapa)
                obstaculos[i] = 0

        ##### REPOSICIONAMENTO POS COLISAO #####
        if obsDireita and obsEsquerda:  # ESMAGAMENTO
            self.__vida = 0

        ##### IMPEDE QUE O JOGADOR PASSE DA BORDA ESQUERDA #####
        if self.x <= 0:
            if self.velx <= 0:
                self.velx = 0
                aceleracao = 0
                self.x = 0

        ##### IMPEDE QUE O JOGADOR PASSE DA BORDA DIREITA #####
        if self.x >= mapa.tamanho[0] - self.largura:
            if self.velx >= 0:
                self.velx = 0
                aceleracao = 0
                self.x = mapa.tamanho[0] - self.largura

        ### CHECANDO VITÓRIA ###
        entidade_vitoria = 0
        for ganhar in mapa.lista_de_entidades:
            if isinstance(ganhar, Vitoria):
                entidade_vitoria = ganhar

        if self.corpo.colliderect(entidade_vitoria.corpo):
            mapa.ganhou = True

        ##### GRAVIDADE ######
        if not obsBaixo: self.vely += gravidade

        ##### ATRITO ######
        if self.__aceleracao == 0:
            if self.velx < 0:
                self.velx += atrito
            elif self.velx > 0:
                self.velx -= atrito

        #### PULO ####
        if obsBaixo and espaco:
            self.vely = -self.poder.pulo

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
        self.y += self.vely * self.__escala_tempo
        self.x += self.velx * self.__escala_tempo

        ##### MATA O JOGADOR SE CAIR NO BURACO #####
        if self.y > mapa.tamanho[1]: self.__vida = 0

        ##### INDICA A DIRECAO DO JOGADOR PARA DIRECIONAR PODERES #####
        if self.velx > 0:
            self.face = 1
        elif self.velx < 0:
            self.face = -1

        ##### ATUALIZACAO DO CORPO DO JOGADOR #####
        self.corpo = pygame.Rect(self.x, self.y, self.largura, self.altura)

    def poderes(self, screen, mapa, acao=False, outros_poderes=False):
        ##### ATIRA BOLA DE FOGO SE ESTIVER DISPONIVEL
        if acao and not self.poder.descanso:
            self.__poder.acao(self, screen, mapa)
