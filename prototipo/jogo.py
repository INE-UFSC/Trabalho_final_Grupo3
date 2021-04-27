import pygame, time, math, random
from jogador import Jogador
from mapa import Mapa
from inimigos import *
from menu import Menu,Tela,Botao
from efeitosrender import *

class Jogo:
    def __init__(self):
        ###### INFORMACOES TA TELA ######
        self.__background_colour = (150, 220, 255)  # Cor do fundo
        (width, height) = (1000, 600)  # Tamanho da tela
        self.__screen = pygame.display.set_mode((width, height)) #Cria o objeto da tela
        pygame.display.set_caption('Tutorial 1')
        self.__screen.fill(self.__background_colour)
        self.__contadormenu = 0

        ### MENU PRINCIPAL
        contadormenu = 0      #usado para criar o efeito rgb do menu
        corsaturada = psicodelico(contadormenu)
        cormenu = misturacor(corsaturada,[255,255,255],1,5)


        botaonivel_1 = Botao(250, 75, 100, 100, (220, 0, 200), (160, 0, 140), "Fase 1", 5)
        botaonivel_2 = Botao(450, 75, 100, 100, (220, 200, 0), (160, 140, 0), "Fase 2", 5)
        botaonivel_3 = Botao(650, 75, 100, 100, (0, 200, 220), (0, 160, 140), "Fase 3", 5)
        botaojogar = Botao(375, 350, 250, 50, (30, 220, 30), (30, 160, 30), "Começar", 5)
        botaoplacar = Botao(375, 425, 250, 50, (30, 220, 30), (30, 160, 30), "Placar", 5)
        botaosair = Botao(375, 500, 250, 50, (30, 220, 30), (30, 160, 30), "Sair", 5)
        botaoconfig = Botao(width-100, height-100, 50, 50, (0, 220, 180), (0, 160, 110), "C", 5)
        telaprincipal = Tela([botaosair,botaojogar,botaoplacar,botaonivel_1, botaonivel_2, botaonivel_3, botaoconfig],cormenu,self.__screen)
        self.__menu = Menu(telaprincipal)

    def logicamenu(self):   # logica do sistema de menu
        relogiomenu = pygame.time.Clock()
        while True:
            self.__menu.tela.renderizar(self.__screen)
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT: return 1
                if evento.type == pygame.MOUSEBUTTONDOWN:
                    acao = self.__menu.tela.clicar()
                    return acao
            self.__contadormenu += 1
            self.__menu.tela.setfundo(misturacor(psicodelico(self.__contadormenu),[240,240,240],1,7))
            relogiomenu.tick(60)

    def rodar(self):
        ###### PYGAME GERAL #####
        rodando = True
        aberto = True
        relogio = pygame.time.Clock()
        screen = self.__screen
        ##### ENTRADAS DO JOGADOR #####
        cima, baixo, direita, esquerda = 0, 0, 0, 0
        atrito = 0.5
        espaco = False
        bola_fogo = False

        ###### INSTANCIAS DE OBJETOS ######
        (width,height) = self.__screen.get_size()
        jogador = Jogador('mario',200, 550, 0, 1)
        mapa = Mapa((width,height))
        mapa.iniciar()

        while rodando:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT: 
                    rodando = False
                    aberto = False
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_w: cima = 5
                    if evento.key == pygame.K_s: baixo = 5
                    if evento.key == pygame.K_d:
                        direita = 0.5
                    if evento.key == pygame.K_a:
                        esquerda = 0.5
                    if evento.key == pygame.K_SPACE or evento.key == pygame.K_w: espaco = True
                    if evento.key == pygame.K_t: bola_fogo = True
                if evento.type == pygame.KEYUP:
                    if evento.key == pygame.K_w: cima = 0
                    if evento.key == pygame.K_s: baixo = 0
                    if evento.key == pygame.K_d:
                        direita = 0
                    if evento.key == pygame.K_a:
                        esquerda = 0
                    if evento.key == pygame.K_SPACE or evento.key == pygame.K_w: espaco = False
                    if evento.key == pygame.K_t: bola_fogo = False



            ##### FILA DE RENDERIZACAO #####
            screen.fill(self.__background_colour) # Preenche com o a cor de fundo
            #circulo.atualizar((R,G,B),size)
            #circulo.move(direita, esquerda ,espaco)

            mapa.atualizar(screen)

            #jogador.colisao(retangulo)
            jogador.mover(direita, esquerda ,espaco, (width, height), mapa, atrito)
            jogador.poderes(screen, mapa, bola_fogo)
            jogador.atualizar(screen)
            if jogador.vida == "morto":
                rodando = False

            #jogador.colisao(retangulo)
            # jogador.colisao(mapa1)
            # pygame.draw.circle(screen, (R, G, B), (400, 250), size, 10)

            ##### RENDERIZACAO DA TELA #####
            pygame.display.flip()

            ##### FPS MELHORADO #####
            relogio.tick(60)
        return aberto


pygame.init()
jogo = Jogo()
while True:
    acao = jogo.logicamenu()

    ### se acao == 0, nao fazer nada
    ### caso contrario, fazer a acao correspondente ao botao descrito

    if acao == 1:   # botao sair
        break
    elif acao == 2: # botao jogar
        if not jogo.rodar():    # se o jogador fechar o jogo durante a fase
            break
