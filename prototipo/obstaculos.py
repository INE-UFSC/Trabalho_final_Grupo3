from entidades import *
from sprites import *


# FUNCOES DE ATUALIZAR NECESSITAM DA AREA VISIVEL PARA RENDERIZAR CORRETAMENTE
class Obstaculo(Estatico):
    def __init__(self, nome: str, x: int, y: int, altura: int, largura: int, arquivo: str, cor: tuple):
        super().__init__(nome, x, y, altura, largura, arquivo, cor)

@instanciavel
class PlataformaMovel(Movel):
    def __init__(self, x: int , y: int, largura: int):
        altura = 17
        super().__init__("plataforma_movel", x, y, altura, largura, 5, "0",  (184, 20, 20))
        self.vely = 2

    def mover(self, dimensoesTela, mapa):
        ##### REPOSICIONAMENTO DA PLATAFORMA #####
        self.y += self.vely * mapa.escala_tempo
        if self.y >= mapa.tamanho[1]:
            self.y = 0


@instanciavel
class Bloco(Obstaculo):
    def __init__(self, nome: str, x: int, y: int):
        largura = 30
        altura = 30
        super().__init__(nome, x, y, altura, largura, "0", (255, 102, 0))


@instanciavel
class Lapis(Obstaculo):
    def __init__(self, nome: str, x: int, topo: int, base: int):
        largura = 44
        altura = base - topo
        super().__init__(nome, x, topo, altura, largura, "sprites", (11, 137, 0))


@instanciavel
class Ponta(Obstaculo):
    def __init__(self, nome: str, x: int, topo: int, base: int):
        largura = 44
        altura = base - topo
        super().__init__(nome, x, topo, altura, largura, "sprites", (11, 137, 0))

    def sofreu_colisao_jogador(self, jogador, direcao, mapa):
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
            return 1 * (mapa.escala_tempo >= 1)
        ##### COLISAO CIMA #####
        elif direcao == "cima":
            if jogador.vely < 0:
                jogador.vely = 0
                jogador.y = self.corpo.bottom
        return 0


@instanciavel
class Cano(Obstaculo):
    def __init__(self, nome: str, y: int, esquerda: int, direita: int):
        altura = 50
        largura = direita - esquerda
        super().__init__(nome, esquerda, y, altura, largura, "0", (11, 137, 0))


@instanciavel
class Chao(Obstaculo):
    def __init__(self, nome: str, y: int, esquerda: int, direita: int):
        altura = 17
        super().__init__(nome, esquerda, y, altura, direita - esquerda, "0", (184, 20, 20))


@instanciavel
class Vitoria(Obstaculo):
    def __init__(self, x: int, y: int, largura: int, altura: int):
        super().__init__("vitoria", x, y, altura, largura, "0", (254, 254, 0))