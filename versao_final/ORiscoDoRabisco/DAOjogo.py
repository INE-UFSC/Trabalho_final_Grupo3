import json, pygame, os
from mapa import montar_mapas
from entidades import *

class DAO:
    """Classe responsavel por dados de mapa, jogos salvos, e configs
    
    Configuracoes incluem tamanho de tela, tela cheia,
    volume de musica e efeitos

    Jogos salvos incluem nome da fase, a fase em si, poderes guardados

    Dados de mapa incluem inimigos, obstaculos e coletaveis,
    definidos pela funcao montar_mapas
    """
    def __init__(self):
        from sys import platform
        if platform == "win32":
            self.__pasta_data = __file__.rsplit("\\",1)[0]+"\\data\\"
            self.__pasta_assets = __file__.rsplit("\\",1)[0]+"\\assets\\"
        else:
            self.__pasta_data = __file__.rsplit("/",1)[0]+"/data/"
            self.__pasta_assets = __file__.rsplit("/",1)[0]+"/assets/"
        self.carregar_configs()
        self.carregar_saves()
        self.carregar_mapas()
        self.__sprites = {}
    
    def carregar_configs(self):
        default = {"resolucao":[1000,600],
                "musica":1,
                "efeitos":1,
                "telacheia":False,
                "mostrarfps":False,
                "renderizarhitbox":False,
                "renderizarsprite":True}
        try:
            with open(self.__pasta_data+"configs.json","r") as arquivo:
                configs = json.load(arquivo)
        except (FileNotFoundError,json.JSONDecodeError):
            configs = {}
        finally:
            for key in default.keys():
                if key not in configs.keys():
                    configs[key] = default[key]
            with open(self.__pasta_data+"configs.json","w") as arquivo:
                json.dump(configs,arquivo)
            self.__configs = configs
          
    def carregar_saves(self):
        try:
            self.__saves = json.load(open(self.__pasta_data+"saves.json","r"))
        except (FileNotFoundError,IndexError,KeyError):
            slots = {'0':["Novo Jogo","fase1","Cinza","Cinza",0],'1':["Novo Jogo","fase1","Cinza","Cinza",0],
                        '2':["Novo Jogo","fase1","Cinza","Cinza",0],'3':["Novo Jogo","fase1","Cinza","Cinza",0],
                        '4':["Novo Jogo","fase1","Cinza","Cinza",0],'6':["Novo Jogo","fase1","Cinza","Cinza",0]}
            with open(self.__pasta_data+"saves.json","w") as saves:
                json.dump(slots,saves)
            self.__saves = slots
    
    def carregar_mapas(self):
        try:
            if modo_dev:
                raise FileNotFoundError
            self.__mapas = json.load(open(self.__pasta_data+"mapas.json","r"))
        except FileNotFoundError:
            with open(self.__pasta_data+"mapas.json","w") as mapa_arquivo:
                mapas = montar_mapas()
                json.dump(mapas, mapa_arquivo)
                self.__mapas = mapas
    
    def carregar_sprite(self, nome):
        try:
            return self.__sprites[nome]
        except KeyError:
            arquivo = self.__pasta_assets+nome
            sprite_sheet = pygame.image.load(arquivo+".png").convert_alpha()
            with open(arquivo+".json") as f:
                dados = json.load(f)
            self.__sprites[nome] = {"sprite_sheet":sprite_sheet,"dados":dados}
            return self.__sprites[nome]
            

    @property
    def configs(self):
        return self.__configs
    
    @configs.setter
    def configs(self,configs):
        self.__configs = configs
        with open(self.__pasta_data+"configs.json","w") as f:
            json.dump(configs,f)

    @property
    def mapas(self):
        return self.__mapas
    
    @mapas.setter
    def mapas(self,mapas):
        self.__mapas = mapas
        with open(self.__pasta_data+"mapas.json","w") as f:
            json.dump(mapas,f)
    
    @property
    def saves(self):
        return self.__saves
    
    @saves.setter
    def saves(self,saves):
        self.__saves = saves
        with open(self.__pasta_data+"saves.json","w") as f:
            json.dump(saves,f)
    
    @property
    def pasta_data(self):
        return self.__pasta_data

    @property
    def pasta_assets(self):
        return self.__pasta_assets

DAOJogo = DAO()