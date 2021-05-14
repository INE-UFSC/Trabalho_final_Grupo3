from entidades import *
from poderes import *

##### ITENS DOS PODERES NO MAPA #####
class Coletavel(Movel):
    "Itens que mudam alguma propriedade do jogador"

    def __init__(self, nome, x, y, imagem, cor=(0, 0, 0), largura=32, altura=32):
        limite_vel = 4
        super().__init__(nome, x, y, altura, largura, limite_vel, imagem, cor)

    def coleta(self, jogador, mapa):
        jogador.coletar_poder(self)
        mapa.escala_tempo = 1
        self.auto_destruir(mapa)

    def sofreu_colisao_outros(self, entidade, direcao, mapa):
        return 0

    def sofreu_colisao_jogador(self, jogador, direcao, mapa):
        self.coleta(jogador, mapa)
        return 0


@instanciavel
class Borracha(Coletavel):
    "Adiciona borracha ao contador"

    def __init__(self, x, y, cor=(245, 245, 220)):
        super().__init__("borracha", x, y, "sprites", cor, 41, 29)
        self.__raio = 10

    def coleta(self, jogador, mapa):
        jogador.coletar_moeda()
        mapa.escala_tempo = 1
        self.auto_destruir(mapa)


@instanciavel
class Paleta(Coletavel):
    """Adiciona uma parte da paleta ao jogador

    Quando completa, permite que o jogador guarde um poder
    """

    def __init__(self, x, y, cor=(0, 0, 0)):
        super().__init__("paleta_mapa", x, y, "sprites", cor, 50, 35)

    def coleta(self, jogador, mapa):
        jogador.coletar_paleta()
        mapa.escala_tempo = 1
        self.auto_destruir(mapa)


@instanciavel
class PoderNoMapa(Coletavel):
    "Base para itens que dao poder ao jogador"

    def __init__(self, nome, x, y, poder_atribuido, imagem, cor=(0, 0, 0)):
        self.poder_atribuido = poder_atribuido
        super().__init__(nome, x, y, imagem, cor)


@instanciavel
class TintaVermelha(PoderNoMapa):
    "Da ao jogador o poder vermelho"

    def __init__(self, x, y):
        super().__init__("poder_Vermelho", x, y, Vermelho(), "sprites", (50, 50, 50))


@instanciavel
class TintaLaranja(PoderNoMapa):
    "Da ao jogador o poder laranja"

    def __init__(self, x, y):
        super().__init__("poder_Laranja", x, y, Laranja(), "sprites", (255, 50, 50))


@instanciavel
class TintaAzul(PoderNoMapa):
    "Da ao jogador o poder azul"

    def __init__(self, x, y):
        super().__init__("poder_Azul", x, y, Azul(), "sprites", (50, 50, 255))


@instanciavel
class TintaRoxa(PoderNoMapa):
    def __init__(self, x, y):
        super().__init__("poder_Roxo", x, y, Roxo(), "sprites", (80, 10, 120))


@instanciavel
class TintaVerde(PoderNoMapa):
    def __init__(self, x, y):
        super().__init__("poder_Verde", x, y, Verde(), "sprites", (5, 200, 40))


@instanciavel
class TintaMarrom(PoderNoMapa):
    def __init__(self, x, y):
        super().__init__("poder_Marrom", x, y, Marrom(), "sprites", (255, 255, 0))
