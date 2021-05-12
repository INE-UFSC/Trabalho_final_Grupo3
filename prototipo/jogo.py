import pygame, random, json
from mapa import carregar_mapa
from menu import *
from efeitosrender import *
from telas import *


class Jogo:
    def __init__(self):
        ###### INFORMACOES TA TELA ######
        try:
            configs = json.load(open("configs.json","r"))
        except FileNotFoundError:
            configs = {"resolucao":[1000,600],
                "musica":1,
                "efeitos":1,
                "telacheia":False}
            json.dump(configs,open("configs.json","w"))
        
        (width, height) = configs["resolucao"]  # Tamanho da tela
        pygame.mixer.music.set_volume(configs["musica"])
        self.__screen = pygame.display.set_mode((width, height),pygame.FULLSCREEN if configs["telacheia"] else 0)  # Cria o objeto da tela
        caption = ["As Aventuras do Guri",
                   "A Aventura Bizarra de Guri",
                   "Super Guri Bros",
                   "Arte-lharia",
                   "Uma Pincelada de Vigor",
                   "Entre Riscos e Riscos"]
        pygame.display.set_caption(random.choices(caption,[6,1,1,4,4,4])[0])
        self.__ciclo = 0
        self.__janela = Janela(Menu_Principal(self.__screen))
        self.__relogio = pygame.time.Clock()

    def menu_inicial(self):  # Menu inicial do jogo
        self.__janela.tela = Menu_Principal(self.__screen)
        while True:
            self.__ciclo += 1
            acao = self.__janela.tela.atualizar(self.__ciclo)

            ### se acao == 0, nao fazer nada
            ### caso contrario, fazer a acao correspondente ao botao descrito

            if acao[0] == False:
                break
            elif isinstance(acao,list):
                try:
                    self.__janela.tela = acao[0](*acao[1])
                except IndexError:
                    "nada muda"
                except TypeError:
                    "onaji desu"
            self.__relogio.tick(60)


pygame.init()
pygame.mixer.music.load('musica_fundo.ogg')
carregar_mapa()
jogo = Jogo()
jogo.menu_inicial()
