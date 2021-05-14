import json, pygame, os

modo_dev = True

class DAO:
    def __init__(self):
        self.carregar_configs()
        self.carregar_saves()
        self.carregar_mapas()
    
    def carregar_configs(self):
        try:
            self.__configs = json.load(open("configs.json","r"))
        except FileNotFoundError:
            configs = {"resolucao":[1000,600],
                "musica":1,
                "efeitos":1,
                "telacheia":False}
            json.dump(configs,open("configs.json","w"))
            self.__configs = configs
    
    def carregar_saves(self):
        try:
            self.__saves = json.load(open("saves.json","r"))
        except FileNotFoundError:
            slots = {'0':["Novo Jogo","fase1","Cinza","Cinza",0],'1':["Novo Jogo","fase1","Cinza","Cinza",0],
                        '2':["Novo Jogo","fase1","Cinza","Cinza",0],'3':["Novo Jogo","fase1","Cinza","Cinza",0],
                        '4':["Novo Jogo","fase1","Cinza","Cinza",0],'6':["Novo Jogo","fase1","Cinza","Cinza",0]}
            json.dump(slots,open("saves.json","w"))
            self.__saves = slots
    
    def carregar_mapas(self):
        try:
            if modo_dev:
                raise FileNotFoundError
            self.__mapas = json.load(open("mapas.json","r"))
        except FileNotFoundError:
            with open("mapas.json","w") as mapa_arquivo:
                mapas = montar_mapas()
                json.dump(mapas, mapa_arquivo)
                self.__mapas = mapas
    
    def carregar_sprites(self):
        from entidades import imagens_instanciaveis
        print(imagens_instanciaveis)
        self.__sprites = {}
        for key in imagens_instanciaveis.keys():
            try:
                self.__sprites[key] = {"imagem": pygame.image.load("sprites/"+key+".png").convert_alpha(),
                    "dados": json.load(open("sprites/"+key+".json","r"))}
            except FileNotFoundError:
                self.__sprites[key] = {"imagem":"sus",
                    "dados": "jesus"}

    @property
    def configs(self):
        return self.__configs
    
    @configs.setter
    def configs(self,configs):
        self.__configs = configs
        json.dump(configs,open("configs.json","w"))

    @property
    def mapas(self):
        return self.__mapas
    
    @mapas.setter
    def mapas(self,mapas):
        self.__mapas = mapas
        json.dump(mapas,open("mapas.json","w"))
    
    @property
    def saves(self):
        return self.__saves
    
    @saves.setter
    def saves(self,saves):
        self.__saves = saves
        json.dump(saves,open("saves.json","w"))
    
    @property
    def sprites(self):
        return self.__sprites

def montar_mapas():
    """Funcao que gera os mapas para serem utilizados no jogo

    Facilita adicionar conteudo ao modificar esta funcao
    em vez de diretamente modificar o arquivo json
    """
    width = 6600
    height = 600
    fase1 = [[
        ["ReiDasCores", (200, 100)],
        ["PunhoVermelho", (0, 0, "esquerdo", 280)],
        ["PunhoVermelho", (0, 0, "direito", 340)],
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


DAOJogo = DAO()