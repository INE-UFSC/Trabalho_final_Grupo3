import pygame, time, math, random
from jogador import Jogador
from mapa import Mapa
from inimigos import *
from menu import Menu,Tela,Botao
from efeitosrender import *

class Particle:
    def __init__(self, pos, size):
        self.velx = 0
        self.vely = 0
        self.x = pos[0]
        self.y = pos[1]
        self.size = size
        self.colour = (0, 0, 0)
        self.thickness = 10

    def display(self, screen):
      pygame.draw.circle(screen, self.colour, (self.x, self.y), self.size, self.thickness)

    def atualizar (self, cor, size):
        self.colour = cor
        self.size = size

    def move(self, direita, esquerda, espaco):
        self.velx = direita - esquerda

        if espaco and self.y == 500:
            self.vely = -20

        if self.y + self.vely >= 500:
            self.y = 500
            self.vely = 0
        else:
            self.vely += 1

        self.y += self.vely
        self.x += self.velx

        self.x = self.x % 800

def definir_cor(graus):
    graus = int(graus)
    if graus in range(300,360) or graus in range(0,60):
        valor = 255
    elif graus in range(120, 240):
        valor = 0
    elif graus in range(60, 120):
        valor = int(255 - ((graus - 60))*4.25)
    else: #graus in range(240, 300)
        valor = int((graus - 240)*4.25)
    return valor

class Jogo:
    def __init__(self):
        ###### INFORMACOES TA TELA ######
        self.__background_colour = (255, 255, 255)  # Cor do fundo
        (width, height) = (1000, 600)  # Tamanho da tela
        self.__screen = pygame.display.set_mode((width, height)) #Cria o objeto da tela
        pygame.display.set_caption('Tutorial 1')
        self.__screen.fill(self.__background_colour)

        ### MENU PRINCIPAL
        contadormenu = 0      #usado para criar o efeito rgb do menu
        corsaturada = psicodelico(contadormenu)
        cormenu = misturacor(corsaturada,[255,255,255],1,5)


        botaonivel_1 = Botao(250, 75, 100, 100, (0, 220, 180), (0, 160, 110), "Fase 1", 5)
        botaonivel_2 = Botao(450, 75, 100, 100, (0, 220, 180), (0, 160, 110), "Fase 2", 5)
        botaonivel_3 = Botao(650, 75, 100, 100, (0, 220, 180), (0, 160, 110), "Fase 3", 5)
        botaojogar = Botao(375, 250, 250, 50, (0, 220, 180), (0, 160, 110), "Começar", 5)
        botaoplacar = Botao(375, 350, 250, 50, (0, 220, 180), (0, 160, 110), "Placar", 5)
        botaosair = Botao(375, 450, 250, 50, (0, 220, 180), (0, 160, 110), "Sair", 5)
        botaoconfig = Botao(width-100, height-100, 50, 50, (0, 220, 180), (0, 160, 110), "C", 5)
        telaprincipal = Tela([botaojogar,botaosair,botaoplacar,botaonivel_1, botaonivel_2, botaonivel_3, botaoconfig],cormenu,self.__screen)
        self.__menu = Menu(telaprincipal)

    def logicamenu(self):   # logica do sistema de menu
        relogiomenu = pygame.time.Clock()
        self.__contadormenu = 0
        while True:
            self.__menu.tela.renderizar(self.__screen)
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT: return 0
                if evento.type == pygame.MOUSEBUTTONDOWN:
                    acao = self.__menu.tela.clicar()
                    if acao != 0:
                        return acao
            self.__contadormenu += 1
            corsaturada = psicodelico(self.__contadormenu)
            self.__menu.tela.setfundo(misturacor(corsaturada,[240,240,240],1,7))
            relogiomenu.tick(60)

    def rodar(self):
        ###### PYGAME GERAL #####
        rodando = True
        aberto = True
        relogio = pygame.time.Clock()
        screen = self.__screen
        ##### ENTRADAS DO JOGADOR #####
        cima, baixo, direita, esquerda = 0, 0, 0, 0
        espaco = False
        bola_fogo = False

        ###### INSTANCIAS DE OBJETOS ######
        (width,height) = self.__screen.get_size()
        jogador = Jogador('mario',100, 500, 0, 1)
        mapa = Mapa((width,height))
        mapa.iniciar()

        ###### FORMAS GEOMETRICAS DE TESTE ######
        R, G, B = 0, 0, 0
        gR, gG, gB = 0, 120, 240
        size = 100
        incrementador = 1

        #circulo = Particle((150, 50), 15)
        #retangulo2 = ObstaculoGenerico(550, 350).bloco()
        #retangulo = pygame.Rect(300, 420, 200, 40)

        while rodando:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT: 
                    rodando = False
                    aberto = False
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_w: cima = 5
                    if evento.key == pygame.K_s: baixo = 5
                    if evento.key == pygame.K_d: direita = 5
                    if evento.key == pygame.K_a: esquerda = 5
                    if evento.key == pygame.K_SPACE or evento.key == pygame.K_w: espaco = True
                    if evento.key == pygame.K_t: bola_fogo = True
                if evento.type == pygame.KEYUP:
                    if evento.key == pygame.K_w: cima = 0
                    if evento.key == pygame.K_s: baixo = 0
                    if evento.key == pygame.K_d: direita = 0
                    if evento.key == pygame.K_a: esquerda = 0
                    if evento.key == pygame.K_SPACE or evento.key == pygame.K_w: espaco = False
                    if evento.key == pygame.K_t: bola_fogo = False



            ##### FILA DE RENDERIZACAO #####
            screen.fill(self.__background_colour) # Preenche com o a cor de fundo
            #circulo.atualizar((R,G,B),size)
            #circulo.move(direita, esquerda ,espaco)

            mapa.atualizar(screen)

            #jogador.colisao(retangulo)
            jogador.mover(direita, esquerda ,espaco, (width, height), mapa)
            jogador.poderes((width, height), mapa, bola_fogo)
            jogador.atualizar(screen)
            if jogador.vida == "morto":
                rodando = False
            #print(retangulo.bottomleft)
            #circulo.display(screen)

            #pygame.draw.rect(screen, (0,0,255), retangulo)
            #pygame.draw.rect(screen, (125,100,255), mapa1[0])


            #jogador.colisao(retangulo)
            # jogador.colisao(mapa1)
            # pygame.draw.circle(screen, (R, G, B), (400, 250), size, 10)

            ##### RENDERIZACAO DA TELA #####
            pygame.display.flip()

            ##### MANIPULACAO DE PARAMETROS DE TESTE #####
            size += incrementador
            if size > 200:
                incrementador = -1
            elif size < 10:
                incrementador = 1

            gR = (gR + 0.5) % 360
            gG = (gG + 0.5) % 360
            gB = (gB + 0.5) % 360

            R = definir_cor(gR)
            G = definir_cor(gG)
            B = definir_cor(gB)

            ##### FPS MELHORADO #####
            relogio.tick(60)
        return aberto


pygame.init()
jogo = Jogo()
while True:
    acao = jogo.logicamenu()
    if acao == 1 and jogo.rodar():
        pass
    else:
        break
