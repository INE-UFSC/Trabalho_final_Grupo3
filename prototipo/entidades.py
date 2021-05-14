# Arquivos com as classes abstratas do jogo
import pygame
from sprites import *

colisao_analisada = "0"
renderizar_hitbox = False
renderizar_sprite = True
modo_dev = True
gravidade = 0.2
classes_instanciaveis = []
imagens_instanciaveis = {}
poderes_no_jogador = []

#Decorator que indica o que a classe pode ser instanciada no mapa
def instanciavel(classe):
    classes_instanciaveis.append(classe)
    return classe

def visivel(classe):
    imagens_instanciaveis[classe.__name__] = classe.nome_imagem
    return classe

def poder_no_jogador(classe):
    poderes_no_jogador.append(classe)
    return classe


class Estatico():
    """Base para qualquer objeto fisico no mapa

    Possui posicao e tamanho
    """
    def __init__(self, nome: str, x: int, y: int, altura: int, largura: int, imagem: str, cor=(0, 0, 0)):
        self.__nome = nome
        self.__x = x
        self.__y = y
        self.__largura = largura
        self.__altura = altura
        self.__corpo = pygame.Rect(x, y, largura, altura)
        self.__imagem = imagem
        self.__cor = cor
        try:
            self.__sprite = Sprite(imagem)
        except FileNotFoundError:
            self.__sprite = []  # nao possui sprite

    @property
    def nome(self):
        return self.__nome

    @nome.setter
    def nome(self, nome):
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

    @cor.setter
    def cor(self, cor):
        self.__cor = cor

    def auto_destruir(self, mapa):
        "Remove-te a ti mesmo"
        if self in mapa.lista_de_entidades:  # RESOLVE PROVISORIAMENTE
            mapa.lista_de_entidades.remove(self)

    def renderizar(self, tela, mapa):
        "Coloca a imagem correspondente na tela"
        if renderizar_hitbox:
            pygame.draw.rect(tela, self.__cor, [self.corpo.x - mapa.campo_visivel.x,
                                                self.corpo.y - mapa.campo_visivel.y,
                                                self.corpo.w,
                                                self.corpo.h])
        if renderizar_sprite:
            try:
                self.sprite.imprimir(tela, self.__nome, self.x - mapa.campo_visivel.x, self.y - mapa.campo_visivel.y, 0,
                                     0, 0, 0, self.__largura, self.__altura)
            except AttributeError:
                #print(self.nome,"sprite nao encontrado")
                pass

    def atualizar(self, tela, mapa, dimensoes_tela):
        "Basicamente, renderiza se estiver na tela, senao, nao"
        if mapa.campo_visivel.colliderect(self.corpo):
            self.renderizar(tela, mapa)
        return False

    def sofreu_colisao_jogador(self, jogador, direcao, mapa):
        "Detecta colisao com o jogador"
        ##### COLISAO ESQUERDA #####
        if direcao == "esquerda":
            if jogador.velx <= 0:
                jogador.velx = 0
                jogador.x = self.corpo.right + 1
        ##### COLISAO DIREITA #####
        elif direcao == "direita":
            if jogador.velx >= 0:
                jogador.velx = 0
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

    def sofreu_colisao_outros(self, entidade, direcao, mapa):
        "Idem Ibdem so que com outros objetos nao jogador"
        ##### COLISAO ESQUERDA #####
        if direcao == "esquerda":
            if entidade.velx <= 0:
                entidade.velx = - entidade.velx
                entidade.x = self.corpo.right + 1
                entidade.face = -(entidade.face)
        ##### COLISAO DIREITA #####
        elif direcao == "direita":
            if entidade.velx >= 0:
                entidade.x = self.corpo.left - entidade.largura
                entidade.velx = - entidade.velx
                entidade.face = -(entidade.face)
        elif direcao in ["baixo"]:
            entidade.vely = 0
            entidade.y = self.corpo.top - entidade.altura


class Movel(Estatico):
    """Expande no estatico e adiciona a acapacidade de mexer
    
    possui tambem velocidade e direcao horizontal
    """
    def __init__(self, nome: str, x: int, y: int, altura: int, largura: int, limite_vel: int, imagem: str,
                 cor=(0, 0, 0)):
        super().__init__(nome, x, y, altura, largura, imagem, cor)
        self.escala_tempo = 1.0
        self.__velx = 0
        self.__vely = 0
        self.__limite_vel = limite_vel
        self.__face = 1
    
    @property
    def face(self):
        return self.__face
    
    @face.setter
    def face(self, face):
        self.__face = face

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
        "Detecta colisao com outros objetos no mapa"
        ##### COLISOES #####
        obsBaixo, obsCima, obsEsquerda, obsDireita = 0, 0, 0, 0

        ##### COLISOES COM OBSTACULOS #####
        for entidade in lista_de_entidades:
            transparente = False
            for tipo in tipos_transparentes:
                transparente = transparente or isinstance(entidade, tipo)
            if entidade != self and not transparente:

                ##### DEFINICAO DO CORPO VELOZ #####
                if self.__velx < 0:  # movimento para a esquerda
                    cveloz_left = self.corpo.left - 1 + self.__velx * self.escala_tempo
                    cveloz_largura = self.corpo.right - cveloz_left + 1
                else:  # movimento para a direita
                    cveloz_left = self.corpo.left - 1
                    cveloz_largura = self.corpo.right - cveloz_left + 1 + self.__velx * self.escala_tempo
                if self.__vely < 0:  # movimento para cima
                    cveloz_top = self.corpo.top - 1 + self.__vely * self.escala_tempo
                    cveloz_altura = self.corpo.bottom - cveloz_top + 1
                else:  # movimento para baixo
                    cveloz_top = self.corpo.top
                    cveloz_altura = self.corpo.bottom - cveloz_top + 1 + self.__vely * self.escala_tempo
                self.__corpoveloz = pygame.Rect(cveloz_left, cveloz_top, cveloz_largura, cveloz_altura)
                colisaoVeloz = self.__corpoveloz.colliderect(entidade.corpo)

                if colisaoVeloz:
                    # Determina o quanto da dentro em cada direcao
                    distCima = abs(self.__corpoveloz.top - entidade.corpo.bottom)
                    distBaixo = abs(self.__corpoveloz.bottom - entidade.corpo.top)
                    distEsquerda = abs(self.__corpoveloz.left - entidade.corpo.right)
                    distDireita = abs(self.__corpoveloz.right - entidade.corpo.left)

                    if distDireita <= distCima and distDireita <= distEsquerda and distDireita <= distBaixo:
                        obsDireita = entidade
                    elif distEsquerda <= distCima and distEsquerda <= distBaixo:
                        obsEsquerda = entidade
                    elif distCima <= distBaixo:
                        obsCima = entidade
                    else:
                        obsBaixo = entidade

        return [obsCima, obsBaixo, obsDireita, obsEsquerda]

    def atualizar(self, tela, mapa, dimensoes_tela):
        "Governa movimento, assim como seu movimento em tempo distorcido"
        if self.escala_tempo != mapa.escala_tempo:
            self.escala_tempo += max(min(mapa.escala_tempo - self.escala_tempo, 0.05), -0.05)
        self.mover(dimensoes_tela, mapa)
        self.corpo = pygame.Rect(self.x, self.y, self.largura, self.altura)
        if mapa.campo_visivel.colliderect(self.corpo):
            self.renderizar(tela, mapa)
        return False
    
    def sofreu_colisao_jogador(self, jogador, direcao, mapa):
        "Detecta colisao com o jogador"
        ##### COLISAO ESQUERDA #####
        if direcao == "esquerda":
            if jogador.velx <= 0:
                jogador.velx = 0
                jogador.x = self.corpo.right + 1
        ##### COLISAO DIREITA #####
        elif direcao == "direita":
            if jogador.velx >= 0:
                jogador.velx = 0
                jogador.x = self.corpo.left - jogador.largura
        ##### COLISAO BAIXO #####
        elif direcao == "baixo":
            jogador.vely = self.vely
            jogador.y = self.corpo.top - jogador.altura
        ##### COLISAO CIMA #####
        elif direcao == "cima":
            if jogador.vely < 0:
                jogador.vely = 0
                jogador.y = self.corpo.bottom
        return 0

    def sofreu_colisao_outros(self, entidade, direcao, mapa):
        "Determina resultado da colisao"
        if self.escala_tempo > 0:
            if direcao == "esquerda":
                if entidade.velx <= 0:
                    entidade.velx = - entidade.velx
                    entidade.face = -(entidade.face)
                    entidade.x = self.corpo.right + 1
                    self.velx = - self.velx
                    self.face = - self.face
            ##### COLISAO DIREITA #####
            elif direcao == "direita":
                if entidade.velx >= 0:
                    entidade.x = self.corpo.left - entidade.largura
                    entidade.velx = - entidade.velx
                    entidade.face = -(entidade.face)
                    self.velx = - self.velx
                    self.face = - self.face
            elif direcao in ["baixo"]:
                entidade.vely = 0
                entidade.y = self.corpo.top - entidade.altura


class Entidade(Movel):
    "Expande no movel, adicionando dano de contato e animacoes"
    def __init__(self, nome: str, x: int, y: int, altura: int, largura: int, limiteVel: int, vida: int,
                 dano_contato: int, imagem: str, cor, frames: int, fogo = False):
        super().__init__(nome, x, y, altura, largura, limiteVel, imagem, cor)
        self.__vida = vida
        self.__dano_contato = dano_contato
        self.__a_prova_de_fogo = fogo
        self.__frames = frames

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
    def contato(self, contato):
        self.__contato = contato

    @property
    def a_prova_de_fogo(self):
        return self.__a_prova_de_fogo

    @property
    def frames(self):
        return self.__frames

    def sofreu_colisao_jogador(self, jogador, direcao, mapa):
        ##### COLISAO ESQUERDA #####
        if not jogador.invisivel:
            if direcao == "esquerda":
                if jogador.velx <= 0:
                    jogador.velx = 0
                    #jogador.aceleracao = 0
                    jogador.x = self.corpo.right + 1
                return self.__dano_contato * (mapa.escala_tempo >= 1)
            ##### COLISAO DIREITA #####
            elif direcao == "direita":
                if jogador.velx >= 0:
                    jogador.velx = 0
                    #jogador.aceleracao = 0
                    jogador.x = self.corpo.left - jogador.largura
                return self.__dano_contato * (mapa.escala_tempo >= 1)
            ##### COLISAO BAIXO #####
            elif direcao == "baixo":
                jogador.vely = -1
                jogador.y = self.corpo.top - jogador.altura
                self.auto_destruir(mapa)
                return 0
            ##### COLISAO CIMA #####
            elif direcao == "cima":
                if jogador.vely < 0:
                    jogador.vely = 0
                    jogador.y = self.corpo.bottom
                return self.__dano_contato * (mapa.escala_tempo >= 1)
        else:
            return 0

    def renderizar(self, tela, mapa):

        if renderizar_hitbox:
            pygame.draw.rect(tela, self.cor, [self.corpo.x - mapa.campo_visivel.x, self.corpo.y - mapa.campo_visivel.y,
                                              self.corpo.w, self.corpo.h])
        if renderizar_sprite and type(self.sprite) != list:
            self.sprite.imprimir(tela, self.nome, self.x - mapa.campo_visivel.x, self.y - mapa.campo_visivel.y,
                        self.face, self.velx, self.vely, int((self.escala_tempo != 0)*mapa.ciclo/6) % self.__frames, 0,0)