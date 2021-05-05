import pygame, time, math, random
from jogador import Jogador
from poderes import FeitoNoCeu
from mapa import Mapa, fase1
from menu import *
from efeitosrender import *

class Menu_Principal(Tela_Menu):   #QUASE QUE UMA INSTANCIA DA CLASSE TELA_MENU
    def __init__(self,superficie):
        botaonivel_1 = Botao(250, 75, 100, 100, (220, 0, 200), (160, 0, 140), "Fase 1", 5)
        botaonivel_2 = Botao(450, 75, 100, 100, (220, 200, 0), (160, 140, 0), "Fase 2", 5)
        botaonivel_3 = Botao(650, 75, 100, 100, (0, 200, 220), (0, 120, 140), "Fase 3", 5)
        botaojogar = Botao(375, 350, 250, 50, (30, 220, 30), (30, 160, 30), "Começar", 5)
        botaoplacar = Botao(375, 425, 250, 50, (30, 220, 30), (30, 160, 30), "Placar", 5)
        botaosair = Botao(375, 500, 250, 50, (30, 220, 30), (30, 160, 30), "Sair", 5)
        (width,height) = superficie.get_size()
        botaoconfig = Botao(width-100, height-100, 50, 50, (0, 220, 180), (0, 160, 110), "C", 5)
        cormenu = misturacor(psicodelico(0),[255,255,255],1,5)
        super().__init__([botaosair,botaojogar,botaoplacar,botaonivel_1, botaonivel_2,
                botaonivel_3, botaoconfig],cormenu,superficie)
        self.__contador_menu = 0

    def logica_menu(self)->int:
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
        self.__tempo_maximo = 350
        self.__fonte = pygame.font.SysFont('Arial',20)
        self.__atrasofim = 0

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
    
    def atualizar(self, ciclo)->int:
        '''Logica de jogo, envolvendo controles, colisao e renderizacao

        Deve ser chamada pela funcao gerente 60 vezes por segundo

        @param ciclo: responsavel pelas frames de animacao do Guri
        
        @returns: 0 se a janela for fechada
                 1 se o Guri morrer ou o tempo acabar
                 2 se o jogo continuar
                 3 se o Guri ganhar
        '''
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

        ##### FILA DE RENDERIZACAO E ATUALIZACAO #####
        self.__superficie.fill(self.__background_colour) # Preenche a cor de fundo

        self.__mapa.atualizar(self.__superficie, self.__campo_visivel, self.__superficie.get_size())

        # FAZER O JOGADOR RECEBER UM MAPA E SALVAR ONDE ELE TA
        if self.__atrasofim > 0:
            self.__direita = 0
            self.__esquerda = 0
            self.__espaco = 0
        else:
            #self.__jogador.mover(self.__direita, self.__esquerda, self.__espaco,#self.__superficie.get_size(), self.__mapa, self.__atrito)
            self.__jogador.poderes(self.__superficie, self.__mapa, self.__bola_fogo)
        self.__campo_visivel = self.__jogador.atualizar(self.__superficie, self.__mapa, self.__campo_visivel, int(ciclo/6),
                                                        [self.__direita, self.__esquerda, self.__espaco],self.__atrito)

        # PERDENDO POR MORRER
        if self.__jogador.vida <= 0 and not self.__mapa.ganhou:
            self.__jogador.vida_pra_zero()
            self.__atrasofim += 1 
            if isinstance(self.__jogador.poder,FeitoNoCeu) and self.__mapa.conta <= 0:
                textin = self.__fonte.render("EM NOME DE DEUS LHES CASTIGAREI", 0, (0,0,0))
            else:
                textin = self.__fonte.render("PERDEU", 0, (0,0,0))
            self.__superficie.blit(textin, (500-textin.get_size()[0]/2, 300-textin.get_size()[1]/2))
            if self.__atrasofim >= 150:
                return 1
        
        ### VENCENDO ###
        if self.__mapa.ganhou:
            self.__atrasofim += 1
            textin = self.__fonte.render("VENCEU", 0, (0,0,0))
            self.__superficie.blit(textin, (500, 300))
            if self.__atrasofim >= 150:
                return 3

        ##### RENDERIZACAO DA TELA #####
        pygame.display.flip()
        self.__tempo_maximo += 1/60 - self.__mapa.escala_tempo/60
        tempo_decorrido = pygame.time.get_ticks()/1000 - self.__comeco
        if not self.__mapa.ganhou:
            self.__mapa.conta =  int(max(self.__tempo_maximo - tempo_decorrido,0))
        
        ##### PASSANDO A VIDA PRO DISPLAY #####d
        self.__mapa.vida_jogador = self.__jogador.vida

        ### PERDENDO POR TEMPO
        if self.__mapa.conta == 0:
            self.__jogador.vida_pra_zero()
        return 2

        

class Jogo:
    def __init__(self):
        ###### INFORMACOES TA TELA ######
        (width, height) = (1000, 600)  # Tamanho da tela
        self.__screen = pygame.display.set_mode((width, height)) #Cria o objeto da tela
        pygame.display.set_caption('Luigi Vermelho')
        self.__contadormenu = 0
        self.__ciclo = 0
        self.__janela = Janela(Menu_Principal(self.__screen))

    def logica_menu(self)->int:
        '''logica do sistema do menu principal
        cria uma tela de menu, e gerencia botoes
        '''
        relogiomenu = pygame.time.Clock()
        self.__janela.trocar_tela(Menu_Principal(self.__screen))
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
            elif acao in [2,4,5,6]:  # botao jogar, fase 1, fase 2
                if acao == 5:
                    aconteceu = self.rodar("fase2")
                elif acao == 6:
                    aconteceu = self.rodar("fase3")
                else:
                    aconteceu = self.rodar("fase1")
                if aconteceu == 0:  # se o jogador fechar o jogo durante a fase
                    break
                elif aconteceu == 3:
                    pass

    def rodar(self,nivel)->int:
        ''' Funcao responsavel por colocar o jogo propriamente dito na tela
        Loop define a taxa de quadros do jogo
        
        @param nivel: nome do nivel a ser inicializado

        @returns: valor retornado pela funcao atualizar do nivel,
                  a nao ser que o valor seja 2, ou seja, o jogo continua
                  rodando normalmente, sem ter chegado a condicao de fim alguma
        '''
        ###### PYGAME GERAL #####
        relogio = pygame.time.Clock()
        try:
            self.__janela.trocar_tela(Tela_De_Jogo(self.__screen, nivel))
        except:
            return 3
        nivel = self.__janela.tela
        while True:
            self.__ciclo += 1
            jogar = nivel.atualizar(self.__ciclo)
            if jogar != 2:
                return jogar
            ##### FPS MELHORADO #####
            relogio.tick(60)


pygame.init()
jogo = Jogo()
jogo.menu_inicial()