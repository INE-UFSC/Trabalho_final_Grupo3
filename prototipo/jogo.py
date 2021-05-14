import pygame, random
from menu import *
from efeitosrender import *
from DAOjogo import DAOJogo
from telas import *


class Jogo:
    """Classe deus do jogo

    Primeiramente cria a tela de jogo,
    carregando parametros salvos
    depois gerencia a janela aberta

    """
    def __init__(self):
        ###### INFORMACOES TA TELA ######
        configs = DAOJogo.configs
        
        (width, height) = configs["resolucao"]  # Tamanho da tela
        pygame.mixer.music.set_volume(configs["musica"])
        self.__screen = pygame.display.set_mode((width, height),
        pygame.FULLSCREEN if configs["telacheia"] else 0)
    
        caption = ["O Risco do Rabisco: A Jornada das Cores"]
                   #  "As Aventuras do Guri",
                   # "A Aventura Bizarra de Guri",
                   # "Super Guri Bros",
                   # "Arte-lharia",
                   # "Uma Pincelada de Vigor",
                   # "Entre Riscos e Rabiscos"]
        pygame.display.set_caption(random.choices(caption,[1])[0])
        


        self.__ciclo = 0
        self.__janela = Janela(Menu_Principal(self.__screen))
        self.__relogio = pygame.time.Clock()


    def rodar(self):
        """Cria tela do jogo e o roda

        Manda a Tela Atual realizar sua atualizacao
        e retornar qual sera a tela que a sucede
        Entao pega a lista retornada e muda para esta
        caso este seja o caso.
        Ver Tela_Menu e suas classes filhas para
        mais detalhe sobre essa instanciacao

        Realiza isso 60x por segundo ate que alguma
        tela informe que o jogo foi fechado
        """

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
jogo = Jogo()
jogo.rodar()
