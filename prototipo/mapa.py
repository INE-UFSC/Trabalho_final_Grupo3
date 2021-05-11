from obstaculos import *
from inimigos import *
from poderes import *
from jogador import Jogador
from hud import *
import json


class Mapa:
    def __init__(self, superficie):
        self.__lista_de_entidades = []
        self.__hud = Hud(superficie.get_size())

        ##### ATRIBUTOS DE RENDERIZACAO #####
        self.__superficie = superficie
        tamanho_campo = superficie.get_size()
        self.__campo_visivel = pygame.Rect(0, 0, tamanho_campo[0], tamanho_campo[1])
        self.campo_menor = pygame.Rect(0, 0, tamanho_campo[0], tamanho_campo[1])

        ##### ATRIBUTOS TEMPORAIS #####
        self.__tempo_restante = ""
        self.__ciclo = 0
        self.escala_tempo = 1

        ##### ATRIBUTOS COMPORTAMENTAIS #####
        self.__vida_jogador = ""
        self.__ganhou = False
        self.__moedas_pegas = ""
        self.__paletas_pegas = ""

    @property
    def lista_de_entidades(self):
        return self.__lista_de_entidades

    # @lista_de_entidades.setter
    # def lista_de_entidades(self, lista_de_entidades):
    #     self.__lista_de_entidades = lista_de_entidades

    @property
    def ganhou(self):
        return self.__ganhou

    @ganhou.setter
    def ganhou(self, ganhou):
        self.__ganhou = ganhou

    @property
    def ciclo(self):
        return self.__ciclo

    @ciclo.setter
    def ciclo(self, ciclo):
        self.__ciclo = ciclo

    @property
    def vida_jogador(self):
        return self.__vida_jogador

    @vida_jogador.setter
    def vida_jogador(self, vida_jogador):
        self.__vida_jogador = vida_jogador

    @property
    def tempo_restante(self):
        return self.__tempo_restante

    @tempo_restante.setter
    def tempo_restante(self, tempo_restante):
        self.__tempo_restante = tempo_restante

    @property
    def campo_visivel(self):
        return self.__campo_visivel

    @property
    def tamanho(self):
        return self.__tamanho

    @property
    def jogador(self):
        return self.__jogador
    
    @property
    def proxima_fase(self):
        return self.__proxima_fase
    
    @property
    def paletas_pegas(self):
        return self.__paletas_pegas
    
    @property
    def moedas_pegas(self):
        return self.__moedas_pegas

    def iniciar(self, fase,dicionaro_mapa):
        ##### LEITURA DAS FASES A PARTIR DO ARQUIVO JSON #####
        lista_todos = dicionaro_mapa[fase]
        objetos_no_mapa = lista_todos[0]
        for item in objetos_no_mapa:
            for classe in classes_instanciaveis:
                if item[0] == classe.__name__:
                    objeto = classe(*item[1])
                    self.__lista_de_entidades.append(objeto)
        self.__tamanho = lista_todos[1]
        self.__proxima_fase = lista_todos[2]

        ##### INSTANCIACAO DO JOGADOR #####
        self.__jogador = Jogador("rabisco", 200, self.tamanho[1] - 50, 0, 100)

        ##### CARREGAMENTO DAS IMAGENS DAS ENTIDADES #####
        for entidade in self.__lista_de_entidades:
            if entidade.imagem != "0": entidade.sprite = Sprite(entidade.imagem)
        return self.__jogador

    def atualizar(self, tela, campo_visivel, dimensoes_tela, ciclo):

        self.__ciclo = ciclo #Frame atual
        self.__campo_visivel = campo_visivel #Aquilo que o jogador ve
        self.__vida_jogador = self.__jogador.vida #Pega a vida do jogador pra passar pro hud
        self.__moedas_pegas = self.__jogador.moedas#Pega as moedas que o jogador tem para passar pro hud
        self.__paletas_pegas = self.__jogador.paleta

        ##### ATUALIZACAO DAS ENTIDADES #####
        for entidade in self.__lista_de_entidades:
            if entidade.atualizar(tela, self, dimensoes_tela):
                self.__lista_de_entidades.remove(entidade)

        ##### ATUALIZACAO DO HUD #####
        self.__hud.atualizar(tela, self, dimensoes_tela, self.__tempo_restante, self.__vida_jogador
                                        , self.__moedas_pegas, self.__paletas_pegas)


def carregar_mapa():
    width = 4200
    height = 700
    fase1 = [[
        ["Lapis", (550, height - 125, height)],
        ["Lapis", (800, height - 125, height)],
        ["Lapis", (1500, height - 125, height)],

        ["Bloco", ('bloco1', 200, height - 350)],
        ["Bloco", ('bloco2', 250, height - 300)],
        ["Bloco", ('bloco3', 300, height - 250)],
        ["Bloco", ('bloco4', 350, height - 200)],
        ["Bloco", ('bloco5', 1000, height - 200)],
        ["Bloco", ('bloco6', 1020, height - 200)],

        ["Chao", ('chao1', height - 10, -200, 350)],
        ["Chao", ('chao2', height - 10, 450, 2205)],
        ["Chao", ('chao3', height - 10, 2500, 4205)],

        ##### BORDA E VITORIA #####
        ["Vitoria", (4000, height - 200, 100, 190)],

        ["Gelatina", (1000, height - 450)],

        ##### PODERES #####
        ["BandanaDoNinja", ('shuriken1', 1200, height - 100)],
        ["CartolaDoMago", ('orbe1', 250, height - 500)],
        ["OculosDoNerd", ('oculos1', 1525, height - 300)],
        #["VerdeBebe", ('orbe', 1600, height - 50)],
        ["BoneMarinheiro", ('cabelo', 1400, height - 100)],
        ["BiscoitoNoMapa", ('bisc', 550, 550)],
        #["Chakra",('chakra', 1600, height-50)],
        ##### INIMIGOS #####
        #["Rato", ('rato1', 610, height - 50)],
        # ["Rato",('rato3', 900, height - 50)],
        ["Saltante", (700, height - 250)],
        ["Voador", ('voador1', 100, height - 500, 200)],
        ["Temporal", ('temporal', 2000, height - 200)],
        # ["PorcoEspinho", ('porco1', 900, height - 50)]
        #["Atirador",(1150, height - 50)],
        ["Atirador",(1000, height - 205, False)]

    ],

        (width, height),
        
        "fase2"]

    width = 6500
    height = 600
    fase2 = [[
        ["Voador", ('voador2', 300, height - 450, 400)],
        ["Chao", ('chao', height - 10, 0, 1200)],
        ["Lapis", (600, height - 125, height)],
        ["Rato", ('rato',700, height - 50)],
        ["Lapis", (900, height - 125, height)],


        ["Chao", ('chao', height - 10, 1375, 1700)],
        ["Saltante", (1400, height - 100)],

        #["Chao", ('chao', 250, 1475, 1600)],

        ["Chao", ('chao', height - 10, 1875, 2775)],
        ["Saltante", (1900, height - 100)],
        ["Lapis", (2150, height - 125, height)],
        ["Rato", ('rato', 2200, height - 50)],
        ["Lapis", (2450, height - 125, height)],

        ["Chao", ('chao', height - 10, 3050, 3425)],
        ["BandanaDoNinja", ('vermelho', 3225, height - 200)],
        ["Saltante", (3350, height - 100)],

        ["Chao", ('chao', height - 10, 4000, 7000)],

        ["Ponta", (4400, height - 125, height)],
        ["Ponta", (4445, height - 125, height)],
        ["Ponta", (4490, height - 125, height)],
        ["Ponta", (4535, height - 125, height)],
        ["Ponta", (4580, height - 125, height)],
        ["Ponta", (4625, height - 125, height)],
        ["Ponta", (4670, height - 125, height)],
        ["Ponta", (4715, height - 125, height)],
        ["Ponta", (4760, height - 125, height)],
        ["Ponta", (4805, height - 125, height)],
        ["Ponta", (4850, height - 125, height)],
        ["Ponta", (4895, height - 125, height)],

        ["Saltante", (5575, height - 100)],
        ["Saltante", (5875, height - 100)],

        ["Chao", ('chao', 275, 5400, 5800)],
        ["Saltante", (5725, 175)],

        ##### BORDA E VITORIA #####
        ["Vitoria", (6300, height - 200, 100, 190)]

    ],

        (width, height),
        
        "fase3"]

    width = 6800
    height = 900
    fase3 = [[
        ["Chao", ('chao', height-10, 0, 995)],
        ["Lapis", (950, height - 125, height)],
        ["Atirador", (750, height - 50)],

        ["Chao", ('chao', height - 10, 1400, 3000)],
        ["Ponta", (1900, height - 125, height)],
        ["Saltante", (1750, height - 100)],

        ["Chao", ('chao', height - 400, 2100, 2250)],
        ["Chao", ('chao', height - 400, 2400, 2550)],
        ["Atirador", (2130, height - 450, False)],
        ["Atirador", (2430, height - 450, False)],
        ["Chao", ('chao', height - 300, 2300, 2350)],
        ["Chao", ('chao', height - 150, 2450, 2550)],

        ["Chao", ('chao', height - 10, 3350, 4000)],
        ["CartolaDoMago", ('orbe1', 3675, height - 200)],
        ["Saltante", (3800, height - 100)],
        ["Chao", ('chao', height - 400, 3700, 3850)],
        ["Atirador", (3730, height - 450, False)],
        ["Chao", ('chao', height - 400, 3900, 4050)],
        ["Atirador", (3930, height - 450, False)],

        ["PlataformaMovel", (150, 4300, 100, -2)],
        ["PlataformaMovel", (450, 4300, 100, -2)],
        ["PlataformaMovel", (750, 4300, 100, -2)],
        ["PlataformaMovel", (300, 4400, 100, -2)],
        ["PlataformaMovel", (600, 4400, 100, -2)],
        ["PlataformaMovel", (900, 4400, 100, -2)],

        ["Chao", ('chao', height - 10, 4600, 5500)],

        ["Lapis", (4900, height - 500, height - 150)],
        ["Chao", ('chao', height - 150, 4900, 5200)],
        ["Lapis", (5156, height - 500, height - 150)],
        ["Chao", ('chao', height - 500, 4900, 5200)],

        ["Lapis", (4700, height - 125, height)],
        ["PorcoEspinho", ('porco', 4800, height - 50)],
        ["PorcoEspinho", ('porco', 4900, height - 50)],
        ["PorcoEspinho", ('porco', 5000, height - 50)],
        ["PorcoEspinho", ('porco', 5100, height - 50)],
        ["PorcoEspinho", ('porco', 5200, height - 50)],
        ["Lapis", (5300, height - 125, height)],

        ["Chao", ('chao', height - 10, 5800, 6800)],
        ["Saltante", (6300, height - 100)],

        ["Chao", ('chao', height - 200, 6300, 6500)],
        ["Atirador", (6350, height - 250, False)],
        ["Atirador", (6350, height - 300, False)],
        ["Atirador", (6350, height - 350, False)],
        ["Atirador", (6350, height - 400, False)],
        ["Atirador", (6350, height - 450, False)],
        ["Atirador", (6350, height - 500, False)],
        ["Atirador", (6350, height - 550, False)],


        ##### BORDA E VITORIA #####
        ["Vitoria", (6600, height - 200, 100, 190)]

    ],

        (width, height),
        
        False]

    with open("mapas.json", 'w') as imagem:
        json.dump({"fase1": fase1, "fase2": fase2, "fase3": fase3}, imagem)
