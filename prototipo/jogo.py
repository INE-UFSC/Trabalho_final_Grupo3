import pygame, time, math, random
from jogador import Jogador
<<<<<<< HEAD
from obstaculo_generico import ObstaculoGenerico
from mapa import Mapa
=======
>>>>>>> 3a13016f1075575af93d6a40075967f29cba2f46

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
        pass

    def rodar(self):
        pygame.init()
<<<<<<< HEAD
        retangulo = pygame.Rect(180, 25, 200, 40)
        retangulo.bottomright
        
        
        #goomba = Goomba("goomba")
        retangulo = pygame.Rect(50, 60, 200, 80)
=======
        retangulo = pygame.Rect(300, 420, 200, 40)
        retangulo.bottomright
        
>>>>>>> 3a13016f1075575af93d6a40075967f29cba2f46
        cima, baixo, direita, esquerda = 0,0,0,0
        espaco = False
        R,G,B = 0,0,0
        gR, gG, gB = 0, 120, 240
        background_colour = (255, 255, 255) #Cor do fundo
        (width, height) = (800, 500) #Tamanho da tela
        size = 100
        incrementador = 1

        screen = pygame.display.set_mode((width, height)) #Cria o objeto da tela
        #relogio = pygame.time.Clock(60)
        pygame.display.set_caption('Tutorial 1')
        screen.fill(background_colour)
        circulo = Particle((150, 50), 15)
<<<<<<< HEAD
        mapa1 = Mapa(15).inicializacao()
        jogador = Jogador('mario',150, 50, 0, 1)
        #retangulo2 = ObstaculoGenerico(550, 350).bloco()
=======
        jogador = Jogador('mario',150, 50, 0, 5)
>>>>>>> 3a13016f1075575af93d6a40075967f29cba2f46

        rodando = True
        while rodando:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT: rodando = False
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_w: cima = 5
                    if evento.key == pygame.K_s: baixo = 5
                    if evento.key == pygame.K_d: direita = 5
                    if evento.key == pygame.K_a: esquerda = 5
                    if evento.key == pygame.K_SPACE: espaco = True
                if evento.type == pygame.KEYUP:
                    if evento.key == pygame.K_w: cima = 0
                    if evento.key == pygame.K_s: baixo = 0
                    if evento.key == pygame.K_d: direita = 0
                    if evento.key == pygame.K_a: esquerda = 0
                    if evento.key == pygame.K_SPACE: espaco = False


            #TUDO QUE VAI SER RENDERIZADO EM ORDEM
            screen.fill(background_colour)
             # Preenche com o a cor de fundo
<<<<<<< HEAD
            screen.fill(background_colour)  # Preenche com o a cor de fundo
=======
>>>>>>> 3a13016f1075575af93d6a40075967f29cba2f46
            # print(direita,esquerda, espaco)
            #circulo.atualizar((R,G,B),size)
            #circulo.move(direita, esquerda ,espaco)
            jogador.colisao(retangulo)
            jogador.mover(direita, esquerda ,espaco, (width, height))
            jogador.atualizar(screen)
<<<<<<< HEAD
            #print(retangulo.bottomleft)
=======
>>>>>>> 3a13016f1075575af93d6a40075967f29cba2f46
            #circulo.display(screen)
            pygame.draw.rect(screen, (0,0,255), retangulo)
            pygame.draw.rect(screen, (125,100,255), mapa1[0])


            #jogador.colisao(retangulo)
            jogador.colisao(mapa1)
            # pygame.draw.circle(screen, (R, G, B), (400, 250), size, 10)

            #RENDERIZACAO DA TELA
            pygame.display.flip()

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

            time.sleep(0.01)

jogo = Jogo()
jogo.rodar()