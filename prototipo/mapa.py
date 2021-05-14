from obstaculos import *
from inimigos import *
from poderes import *
from rei import *
from jogador import Jogador
from hud import *


class Mapa:
    "Classe que segura todas as entidades de um jogo"
    def __init__(self, superficie):
        self.__lista_de_entidades = []
        self.__hud = Hud(superficie.get_size())


        ##### ATRIBUTOS DE RENDERIZACAO #####
        
        self.__superficie = superficie
        tamanho_campo = superficie.get_size()
        self.__campo_visivel = pygame.Rect(0, 0, tamanho_campo[0], tamanho_campo[1])
        self.campo_menor = pygame.Rect(0, 0, tamanho_campo[0], tamanho_campo[1])
        self.__background_colour = (150, 220, 255)  # Cor do fundo

        ##### ATRIBUTOS TEMPORAIS #####
        self.__tempo_restante = ""
        self.__ciclo = 0
        self.escala_tempo = 1
        self.render_escala_tempo = 1

        ##### ATRIBUTOS COMPORTAMENTAIS #####
        self.__vida_jogador = ""
        self.__ganhou = False
        self.__moedas_pegas = ""
        self.__paletas_pegas = ""

    @property
    def lista_de_entidades(self):
        return self.__lista_de_entidades

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
    
    @property
    def cor_fundo(self):
        return self.__background_colour
    
    @cor_fundo.setter
    def cor_fundo(self,cor):
        self.__background_colour = cor

    def iniciar(self, fase, dicionaro_mapa, poder_atual, poder_armazenado, paletas):
        """define outras propriedades do mapa fora do __init__()
        
        return o objeto jogador a ser utilizado"""
        ##### LEITURA DAS FASES A PARTIR DO ARQUIVO JSON #####
        lista_todos = dicionaro_mapa[fase]
        objetos_no_mapa = lista_todos[0]
        for item in objetos_no_mapa:
            for classe in classes_instanciaveis:
                if item[0] == classe.__name__:
                    parametros = item[1] #Sim eh so pra ser maneiro
                    objeto = classe(*parametros)
                    self.__lista_de_entidades.append(objeto)
        self.__tamanho = lista_todos[1]
        self.__proxima_fase = lista_todos[2]

        ##### INSTANCIACAO DO JOGADOR #####
        self.__jogador = Jogador("rabisco", 200, self.tamanho[1] - 50, poder_atual, poder_armazenado, paletas)

        ##### CARREGAMENTO DAS IMAGENS DAS ENTIDADES #####
        for entidade in self.__lista_de_entidades:
            if entidade.imagem != "0": entidade.sprite = Sprite(entidade.imagem)
        return self.__jogador

    def atualizar(self, tela, campo_visivel, dimensoes_tela, ciclo):
        "Atualiza, principalmente renderiza cada objeto componente"

        self.__ciclo = ciclo #Frame atual
        self.__campo_visivel = campo_visivel #Aquilo que o jogador ve
        self.__vida_jogador = self.__jogador.vida #Pega a vida do jogador pra passar pro hud
        self.__moedas_pegas = self.__jogador.moedas#Pega as moedas que o jogador tem para passar pro hud
        self.__paletas_pegas = self.__jogador.paleta
        self.render_escala_tempo += max(min(self.escala_tempo - self.render_escala_tempo, 0.05), -0.05)
        self.cor_fundo = [180-min(self.render_escala_tempo,1)*30,
            200+min(self.render_escala_tempo,1)*20,
            210+min(self.render_escala_tempo,1)*45]
        self.__superficie.fill(self.__background_colour)  # Preenche a cor de fundo

        ##### ATUALIZACAO DAS ENTIDADES #####
        for entidade in self.__lista_de_entidades:
            if entidade.atualizar(tela, self, dimensoes_tela):
                self.__lista_de_entidades.remove(entidade)

        ##### ATUALIZACAO DO HUD #####
        self.__hud.atualizar(tela, self, dimensoes_tela, self.__tempo_restante, self.__vida_jogador
                                        , self.__moedas_pegas, self.__paletas_pegas)


def montar_mapas():
    """Funcao que gera os mapas para serem utilizados no jogo

    Facilita adicionar conteudo ao modificar esta funcao
    em vez de diretamente modificar o arquivo json
    """
    width = 6600
    height = 600
    fase1 = [[
        ["ReiDasCores", (200, 100)],
        ["PunhoVermelho", (0, 0, "esquerdo")],
        ["PunhoVermelho", (0, 0, "direito")],
        ["CabecaLaranja", (0, 0)],
        ["CoracaoRoxo", (0, 0)],
        ["Chao", ('chao', height - 10, 0, 6200)],#1200)],
        # ["Lapis", (600, height - 125, height)],
        # ["Bolota", (700, height - 50)],
        # ["Lapis", (900, height - 125, height)],
        #
        #
        # ["Chao", ('chao', height - 10, 1375, 1700)],
        # ["Saltante", (1400, height - 100)],
        #
        # #["Chao", ('chao', 250, 1475, 1600)],
        #
        # ["Chao", ('chao', height - 10, 1875, 2775)],
        # ["Saltante", (1900, height - 100)],
        # ["Lapis", (2150, height - 125, height)],
        # ["Bolota", (2200, height - 50)],
        # ["Lapis", (2450, height - 125, height)],
        #
        # ["Chao", ('chao', height - 10, 3050, 4000)],
        # ["Chao", ('chao', height - 450, 3050, 4000)],
        # ["TintaVermelha", (3325, height - 260)],
        # ["Saltante", (3350, height - 100)],
        # ["Chao", ('chao', height - 160, 3975, 4100)],
        # ["Lapis", (3950, height - 125, height)],
        # ["Lapis", (3950, height - 235, height)],
        # ["Lapis", (3950, height - 320, height)],
        # ["Chao", ('chao', height - 320, 3450, 3650)],
        # ["Chao", ('chao', height - 160, 3250, 3450)],
        # ["Paleta", (3520, 90)],
        #
        # ["Chao", ('chao', height - 10, 4000, 7000)],
        #
        # ["Ponta", (4500, height - 125, height)],
        # ["Ponta", (4545, height - 125, height)],
        # ["Ponta", (4590, height - 125, height)],
        # ["Ponta", (4635, height - 125, height)],
        # ["Ponta", (4680, height - 125, height)],
        # ["Ponta", (4725, height - 125, height)],
        # ["Ponta", (4770, height - 125, height)],
        # ["Ponta", (4815, height - 125, height)],
        # ["Ponta", (4860, height - 125, height)],
        # ["Ponta", (4905, height - 125, height)],
        # ["Ponta", (4950, height - 125, height)],
        # ["Ponta", (4995, height - 125, height)],
        #
        # ["Saltante", (5675, height - 100)],
        # ["Saltante", (5775, height - 100)],
        #
        # ["Chao", ('chao', 275, 5500, 5900)],
        # ["Saltante", (5825, 175)],

        ##### BORDA E VITORIA #####
        ["Vitoria", (6400, height - 285)]

    ],

        (width, height),
        
        "fase2"]

    width = 6800
    height = 900
    fase2 = [[
        ["Chao", ('chao', height - 10, 0, 995)],
        ["Chao", ('chao', height - 200, 200, 400)],
        ["Bolota", (275, height- 250)],
        ["Borracha", (240, height - 300)],
        ["Borracha", (290, height - 300)],
        ["Borracha", (340, height - 300)],
        ["Lapis", (950, height - 125, height)],
        ["Atirador", (750, height - 100)],
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
        ["TintaLaranja", (3675, height - 200)],
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
        ["Espinhento", (4800, height - 50)],
        ["Espinhento", (4900, height - 50)],
        ["Espinhento", (5000, height - 50)],
        ["Espinhento", (5100, height - 50)],
        ["Espinhento", (5200, height - 50)],
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
        ["Vitoria", (6600, height - 285)]

    ],

        (width, height),

        "fase3"]

    width = 6800
    height = 900
    fase3 = [[
        ["Chao", ('chao', height-10, 0, 2250)],
        ["Lapis", (950, height - 125, height)],
        ["Gelatina", (700, height - 160)],

        ["Saltante", (1550, height - 100)],

        ["Chao", ('chao', height - 400, 1600, 1750)],
        ["Atirador", (1630, height - 450, False)],
        ["Chao", ('chao', height - 150, 2400, 2550)],

        ["Chao", ('chao', height - 10, 2700, 3300)],
        ["Lapis", (2750, height - 450, height-300)],
        ["Gelatina", (2800, height - 600)],
        ["Lapis", (3200, height - 450, height-300)],
        ["Chao", ('chao', height - 300, 2700, 3300)],

        ["Chao", ('chao', height - 600, 2550, 2700)],
        ["Atirador", (2580, height - 650, False)],

        ["Chao", ('chao', height - 600, 3300, 3450)],
        ["Atirador", (3330, height - 650, False)],


        ["PlataformaMovel", (100, 3600, 100, -2)],
        ["PlataformaMovel", (400, 3600, 100, -2)],
        ["PlataformaMovel", (700, 3600, 100, -2)],

        ["Chao", ('chao', height - 10, 3900, 5000)],
        ["Ponta", (4000, height - 125, height)],
        ["Gelatina", (4100, height - 200)],
        ["TintaAzul", (4175, height - 75)],
        ["Ponta", (4300, height - 125, height)],

        ["Atirador", (4600, height - 100, False)],
        ["Atirador", (4600, height - 150, False)],
        ["Saltante", (4750, height - 100)],

        ["Chao", ('chao', height - 400, 4850, 5000)],
        ["Atirador", (4880, height - 450, False)],

        ["PlataformaMovel", (100, 5150, 100, -2)],
        ["PlataformaMovel", (400, 5150, 100, -2)],
        ["PlataformaMovel", (700, 5150, 100, -2)],

        ["Chao", ('chao', height - 10, 5400, 6800)],
        ["Ponta", (5450, height - 125, height)],
        ["Gelatina", (5500, height - 160)],
        ["Gelatina", (5700, height - 160)],
        ["Gelatina", (5900, height - 160)],
        ["Gelatina", (6100, height - 160)],
        ["Gelatina", (6300, height - 160)],

        ["Chao", ('chao', height - 400, 5400, 5550)],
        ["Atirador", (5430, height - 450, False)],

        ["Chao", ('chao', height - 400, 5600, 5750)],
        ["Atirador", (5630, height - 450, False)],

        ["Chao", ('chao', height - 400, 5800, 5950)],
        ["Atirador", (5830, height - 450, False)],

        ["Chao", ('chao', height - 400, 6000, 6150)],
        ["Atirador", (6030, height - 450, False)],

        ["Chao", ('chao', height - 400, 6200, 6350)],
        ["Atirador", (6230, height - 450, False)],

        ##### BORDA E VITORIA #####
        ["Vitoria", (6600, height - 285)]

    ],

        (width, height),
        
        "fase4"]

    width = 6800
    height = 900
    fase4 = [[
        ["Temporal", (300, height - 200)],
        ["Chao", ('chao', height - 10, 0, 1400)],
        ["Atirador", (600, height - 100, False)],
        ["Atirador", (600, height - 150, False)],
        ["Saltante", (750, height - 100)],
        ["Lapis", (850, height - 125, height)],
        ["Bolota", (900, height - 50)],
        ["Lapis", (1250, height - 125, height)],

        ["Temporal", (1600, height - 200)],
        ["Temporal", (1900, height - 200)],
        ["Temporal", (2200, height - 200)],

        ["Chao", ('chao', height - 10, 2400, 3700)],
        ["Ponta", (2500, height - 125, height)],

        ["Chao", ('chao', height - 400, 2700, 2850)],
        ["Atirador", (2730, height - 450, False)],
        ["Atirador", (2730, height - 500, False)],

        ["Gelatina", (2800, height - 200)],
        ["TintaRoxa", (2975, height - 200)],
        ["Saltante", (3100, height - 100)],

        ["Chao", ('chao', height - 400, 3250, 3400)],
        ["Atirador", (3280, height - 450, False)],
        ["Atirador", (3280, height - 500, False)],

        ["Ponta", (3500, height - 125, height)],

        ["PlataformaMovel", (100, 3900, 1000, 3)],
        ["PlataformaMovel", (400, 3900, 1000, 3)],
        ["PlataformaMovel", (700, 3900, 1000, 3)],

        ["Chao", ('chao', height - 10, 5200, 6800)],
        ["Lapis", (5250, height - 125, height)],

        ["Atirador", (5600, height - 100, False)],
        ["Atirador", (5600, height - 150, False)],
        ["Saltante", (5750, height - 100)],

        ["Atirador", (6200, height - 100, False)],
        ["Atirador", (6200, height - 150, False)],
        ["Saltante", (6350, height - 100)],

        ["Chao", ('chao', height - 350, 6250, 6500)],
        ["Temporal", (6375, height - 450)],

        ##### BORDA E VITORIA #####
        ["Vitoria", (6600, height - 285)]

    ],

        (width, height),

        False]

    width = 5040
    height = 700
    fase5 = [[
        ["Chao", ('chao1', height - 10, -200, 300)],

        ["Bloco", ('bloco1', 300, height - 200)],
        ["Bloco", ('bloco2', 450, height - 350)],
        ["Bloco", ('bloco3', 600, height - 500)],


        ["Chao", ('chao2', height - 500, 750, 1100)],
        ["Chao", ('chao3', 450, 870, 1010)],
        ["Atirador", (870, 406, False)],
        ["Chao", ('chao4', 350, 1200, 1250)],
        ["Chao", ('chao4', height - 500, 1514, 1734)],
        ["Lapis", (1470, height - 544, height - 483)],
        ["Gelatina", (1600, 100)],
        ["Lapis", (1734, height - 544, height - 483)],
        ["Chao", ('chao4', -100, 1900, 2500)],
        ["Saltante", (2400, -154)],
        ["Chao", ('chao4', -300, 1970, 2060)],
        ["Atirador", (1970, -344, False)],
        ["Chao", ('chao4', 144, 2400, 2490)],
        ["Atirador", (2400, 100, False)],
        ["Temporal", (1970, -390)],
        ["TintaLaranja", (2470, -160)],
        ["Bloco", ('bloco4', 2860, -100)],
        ["Bloco", ('bloco6', 3170, -100)],
        ["Chao", ('chao4', 144, 3200, 3290)],
        ["Atirador", (3200, 100, False)],
        ["Atirador", (3200, 54, False)],
        ["Bloco", ('bloco7', 3480, -100)],
        ["Lapis", (3880, 40, 140)],
        ["Chao", ('chao4', 123, 3924, 4500)],
        ["Lapis", (4501, 40, 140)],

        ##### BORDA E VITORIA #####
        ["Chao", ('chao4', 335, 4770, 5031)],
        ["Vitoria", (4870, 60)],

        ["Gelatina", (1000, height - 450)],
        ["Paleta", (995, 405)],
        ["Paleta", (1200, 300)],
        ["Paleta", (1400, 300)],
        ["Paleta", (1600, 300)],

        ##### PODERES #####
        ["TintaVermelha", (1200, height - 100)],
        ["TintaLaranja", (250, height - 500)],
        ["TintaAzul", (1525, height - 300)],
        ["VerdeBebe", (1600, height - 50)],
        ["TintaRoxa", (1400, height - 100)],
        ["Borracha", (550, 550)],
        # ["Chakra",('chakra', 1600, height-50)],
        ##### INIMIGOS #####
        # ["Bolota", (610, height - 50)],
        # ["Bolota",(900, height - 50)],
        ["Saltante", (700, height - 250)],
        ["Voador", ('voador1', 100, height - 500, 200)],
        ["Temporal", (2000, height - 200)],
        # ["Espinhento", ('porco1', 900, height - 50)]
        # ["Atirador",(1150, height - 50)],
        ["Atirador", (1000, height - 205, False)]

    ],

        (width, height),

        False]

    return {"fase1": fase1, "fase2": fase2, "fase3": fase3, "fase4": fase4, "fase5": fase5}
