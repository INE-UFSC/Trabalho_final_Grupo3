import pygame, time, math, random
from jogador import Jogador
from mapa import Mapa, fase1, fase2
from inimigos import *
from menu import *
from efeitosrender import *

class Menu_Principal(Tela_Menu):   #QUASE QUE UMA INSTANCIA DA CLASSE TELA_MENU
    def __init__(self,superficie):
        botaonivel_1 = Botao(250, 75, 100, 100, (220, 0, 200), (160, 0, 140), "Fase 1", 5)
        botaonivel_2 = Botao(450, 75, 100, 100, (220, 200, 0), (160, 140, 0), "Fase 2", 5)
        botaonivel_3 = Botao(650, 75, 100, 100, (0, 200, 220), (0, 160, 140), "Fase 3", 5)
        botaojogar = Botao(375, 350, 250, 50, (30, 220, 30), (30, 160, 30), "Começar", 5)
        botaoplacar = Botao(375, 425, 250, 50, (30, 220, 30), (30, 160, 30), "Placar", 5)
        botaosair = Botao(375, 500, 250, 50, (30, 220, 30), (30, 160, 30), "Sair", 5)
        (width,height) = superficie.get_size()
        botaoconfig = Botao(width-100, height-100, 50, 50, (0, 220, 180), (0, 160, 110), "C", 5)
        cormenu = misturacor(psicodelico(0),[255,255,255],1,5)
        super().__init__([botaosair,botaojogar,botaoplacar,botaonivel_1, botaonivel_2,
                botaonivel_3, botaoconfig],cormenu,superficie)
        self.__contador_menu = 0

    def logica_menu(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT: return 1
            if evento.type == pygame.MOUSEBUTTONDOWN:
                acao = self.clicar()
                return acao
        self.__contador_menu += 1
        self.setfundo(misturacor(psicodelico(self.__contador_menu),[240,240,240],1,7))
    
    def menu_inicial(self):
        pass

class Tela_De_Jogo(Tela):
    def __init__(self,superficie,nivel):
        self.__superficie = superficie
        self.__background_colour = (150, 220, 255)  # Cor do fundo
        (width,height) = superficie.get_size()
        self.__campo_visivel = pygame.Rect(0,0,width,height)
        self.__comeco = 0

        ##### ENTRADAS DO JOGADOR #####
        self.__cima, self.__baixo, self.__direita, self.__esquerda = 0, 0, 0, 0
        self.__atrito = 0.5
        self.__espaco = False
        self.__bola_fogo = False

        ###### INSTANCIAS DE OBJETOS ######
        self.__jogador = Jogador('mario',200, 550, 0, 1)

        ##### MAPA #####
        self.__mapa = Mapa((width, height))
        self.__mapa.iniciar(nivel)
        self.__comeco = pygame.time.get_ticks()/1000
    
    def atualizar(self, ciclo):

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT: 
                return 0
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_w: self.__cima = 5
                if evento.key == pygame.K_s: self.__baixo = 5
                if evento.key == pygame.K_d:
                    self.__direita = 0.5
                if evento.key == pygame.K_a:
                    self.__esquerda = 0.5
                if evento.key == pygame.K_SPACE or evento.key == pygame.K_w: self.__espaco = True
            if evento.type == pygame.KEYUP:
                if evento.key == pygame.K_w: self.__cima = 0
                if evento.key == pygame.K_s: self.__baixo = 0
                if evento.key == pygame.K_d:
                    self.__direita = 0
                if evento.key == pygame.K_a:
                    self.__esquerda = 0
                if evento.key == pygame.K_SPACE or evento.key == pygame.K_w: self.__espaco = False
            if evento.type == pygame.MOUSEBUTTONDOWN: self.__bola_fogo = True
            elif evento.type == pygame.MOUSEBUTTONUP: self.__bola_fogo = False

        ##### FILA DE RENDERIZACAO #####
        self.__superficie.fill(self.__background_colour) # Preenaa a com o a cor de fundo

        self.__mapa.atualizar(self.__superficie, self.__campo_visivel, self.__superficie.get_size())

        # FAZER O JOGADOR RECEBER UM MAPA E SALVAR ONDE ELE TA
        self.__jogador.mover(self.__direita, self.__esquerda, self.__espaco, 
            self.__superficie.get_size(), self.__mapa, self.__atrito)
        self.__jogador.poderes(self.__superficie, self.__mapa, self.__bola_fogo)
        self.__campo_visivel = self.__jogador.atualizar(self.__superficie, self.__campo_visivel, int(ciclo/15))
        if self.__jogador.vida <= 0:
            return 1

        ##### RENDERIZACAO DA TELA #####
        pygame.display.flip()
        self.__mapa.conta = int((pygame.time.get_ticks()/1000) - self.__comeco)
        return 2

class Jogo:
    def __init__(self):
        ###### INFORMACOES TA TELA ######
        (width, height) = (1000, 600)  # Tamanho da tela
        self.__screen = pygame.display.set_mode((width, height)) #Cria o objeto da tela
        pygame.display.set_caption('Luigi Vermelho')
        self.__contadormenu = 0
        self.__ciclo = 0

        telaprincipal = Menu_Principal(self.__screen)
        self.__janela = Janela(telaprincipal)

    def logica_menu(self):   # logica do sistema de menu
        relogiomenu = pygame.time.Clock()
        while True:
            return self.__janela.tela.atualizar()
            relogiomenu.tick(60)

    def menu_inicial(self): # Menu inicial do jogo
        while True:
            acao = self.logica_menu()

            ### se acao == 0, nao fazer nada
            ### caso contrario, fazer a acao correspondente ao botao descrito

            if acao == 1:  # botao sair
                break
            elif acao == 2:  # botao jogar
                if not self.rodar():  # se o jogador fechar o jogo durante a fase
                    break

    def rodar(self):
        ###### PYGAME GERAL #####
        relogio = pygame.time.Clock()

        nivel = Tela_De_Jogo(self.__screen, fase1)
        while True:
            self.__ciclo += 1
            jogar = nivel.atualizar(self.__ciclo)
            if jogar == 0:
                return False
            if jogar == 1:
                return True
            ##### FPS MELHORADO #####
            relogio.tick(60)


pygame.init()
jogo = Jogo()
jogo.menu_inicial()