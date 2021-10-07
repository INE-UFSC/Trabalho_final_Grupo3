from entidades import *
import pygame

class Hud:
    "Uniao dos elementos do HUD do jogador"
    def __init__(self,tamanho_tela):
        tt = tamanho_tela
        self.__vida = Vida(tt[0]*3/50, tt[1]/20)
        self.__tempo = Tempo(tt[0]*11/50, tt[1]/20)
        self.__borrachona = Borrachona(tt[0] * 8 / 20, tt[1] / 20)
        self.__barra_poder = BarraPoder(tt[0]*7/9, tt[1]/12)
        self.__paleta = Paleta(tt[0]*11/20, tt[1]/20)
        self.__poder_armazenado = ArmazenadoPoder(tt[0]*11/20+92, tt[1]/20+35)
        self.__barra_vida_rei = BarraVidaRei(tt[0]/2, tt[1]/5)

    def atualizar(self, tela, mapa, dimensoes_tela, tempo, vida, moedas_pegas, paletas_pegas):
        "Atualiza cada um dos elementos"
        self.__vida.atualizar_hud(tela, mapa, dimensoes_tela, vida)
        self.__tempo.atualizar_hud(tela, mapa, dimensoes_tela, tempo)
        self.__barra_poder.atualizar_hud(tela, mapa, dimensoes_tela)
        self.__borrachona.atualizar_hud(tela, mapa, dimensoes_tela, moedas_pegas)
        self.__paleta.atualizar_hud(tela, mapa, dimensoes_tela, paletas_pegas)
        self.__poder_armazenado.atualizar_hud(tela, mapa, dimensoes_tela)
        self.__barra_vida_rei.atualizar_hud(tela, mapa, dimensoes_tela)
    
    @property
    def barra_rei(self):
        return self.__barra_vida_rei


@visivel
class Vida(Estatico):
    "Indica a vida do jogador"
    nome_imagem = "sprites"
    def __init__(self, x: int, y: int):
        altura = 30
        largura = 100
        self.__fonte = pygame.font.SysFont('Arial', 20)
        self.__vida = ""
        super().__init__("vida", x, y, altura, largura, "sprites", (10, 237, 0))

    def renderizar(self, tela, mapa):
        nome = self.nome+"_"+str(self.__vida)
        self.sprite.imprimir(tela, nome, self.x, self.y, 0, 0, 0, 0, 0, 0)

    def atualizar_hud(self, tela, mapa, dimensoes_tela, vida):
        self.__vida = vida
        self.renderizar(tela, mapa)
        return False


@visivel
class Tempo(Estatico):
    "Mostra o tempo restante ate que o jogador perca"
    nome_imagem = "sprites"
    def __init__(self, x: int, y: int):
        altura = 30
        largura = 70
        self.tempomax = 320
        self.__fonte = pygame.font.SysFont('Arial', 40)
        self.__tempo = 0
        self.__contador = self.__fonte.render('time :' + " " + str(self.__tempo), False, (0, 0, 0))
        super().__init__("tempo", x, y, altura, largura, "sprites", (160, 160, 160))

    def renderizar(self, tela, mapa):
        "Mostra o timer e altera o sprite da ampulheta quando necessario"
        #print(self.__tempo, self.tempomax)
        if type(self.__tempo) == int  :
            nome = "tempo_"+str(int(self.__tempo/max((self.tempomax/5),1)))
        else:
            nome = "tempo_"
        self.__contador = self.__fonte.render(str(self.__tempo), False, (0, 0, 0))
        tela.blit(self.__contador, (self.x+70, self.y+35))
        self.sprite.imprimir(tela, nome, self.x, self.y, 0, 0, 0, 0, 0, 0)

    def atualizar_hud(self, tela, mapa, dimensoes_tela, tempo):
        "Atualiza o contador interno dele com o do mapa"
        self.__tempo = tempo
        self.renderizar(tela, mapa)
        return False


@visivel
class Borrachona(Estatico):
    "Contador de Borrachas coletadas"
    nome_imagem = "sprites"
    def __init__(self, x: int, y: int):
        altura = 30
        largura = 60
        super().__init__("borrachona", x, y, altura, largura, "sprites", (254, 254, 0))
        self.__numero_biscoitos = 0
        self.__fonte = pygame.font.SysFont('Arial', 40)
        self.__escreve_na_tela = ""

    def renderizar(self, tela, mapa):
        "Mostra a quantidade de borrachas coletadas"
        self.__escreve_na_tela = self.__fonte.render("x" + str(self.__numero_biscoitos), False, (0, 0, 0))
        self.sprite.imprimir(tela, "borrachona", self.x, self.y, 0, 0, 0, 0, 0, 0)
        tela.blit(self.__escreve_na_tela, (self.x+90, self.y+35))
        
    def atualizar_hud(self, tela, mapa, dimensoes_tela, moedas_pegas):
        "Atualiza o contador interno dele com o do Jogador"
        self.__numero_biscoitos = moedas_pegas
        self.renderizar(tela, mapa)
        return False


@visivel
class BarraPoder(Estatico):
    "Indica a recarga e duracao do poder"
    nome_imagem = "sprites"
    def __init__(self, x: int, y: int):
        altura = 40
        largura = 188
        self.__largura_atual = largura
        self.__cor_poder = (0, 0, 0)
        self.__corpo_poder = []
        super().__init__("poder_barra", x, y, altura, largura, "sprites", (205, 133, 63))
        #self.sprite = SpriteSheetBarras()

    def atualizar_hud(self, tela, mapa, dimensoes_tela):
        "Checa se o jogador trocou de poder e tenta renderizar"
        self.__cor_poder = mapa.jogador.poder.cor
        self.__largura_atual = (abs(mapa.jogador.poder.descanso - mapa.jogador.poder.recarga))/mapa.jogador.poder.recarga * self.largura
        self.__corpo_poder = pygame.Rect(self.x, self.y, self.__largura_atual, self.altura)
        self.renderizar(tela, mapa)
        return False

    def renderizar(self, tela, mapa):
        "Mostra quanto falta para recarregar ou acabar o poder, e qual ele eh"
        pygame.draw.rect(tela, self.cor, self.corpo)
        pygame.draw.rect(tela, self.__cor_poder, self.__corpo_poder)
        nome = self.nome+"_"+mapa.jogador.poder.nome
        self.sprite.imprimir(tela, nome, self.x-70, self.y-18, 0, 0, 0, 0, 0, 0)


@visivel
class Paleta(Estatico):
    "Mostra o progresso de colecao de paletas no mapa"
    nome_imagem = "sprites"
    def __init__(self, x: int, y: int):
        altura = 40
        largura = 40
        self.__largura_atual = largura
        super().__init__("paleta", x, y, altura, largura, "sprites", (205, 133, 63))
        self.__paletas_coletadas = 0
        self.__fonte = pygame.font.SysFont('Arial', 40)
        self.__escreve_na_tela= ""

    def renderizar(self, tela, mapa):
        "Renderiza a soma das partes coletadas"
        nome = self.nome + "_" + str(self.__paletas_coletadas)
        self.sprite.imprimir(tela, nome, self.x, self.y, 0, 0, 0, 0, 0, 0)

    def atualizar_hud(self, tela, mapa, dimensoes_tela, paletas_pegas):
        self.__paletas_coletadas = paletas_pegas
        self.renderizar(tela, mapa)
        return False


@visivel
class ArmazenadoPoder(Estatico):
    "Mostra qual poder o jogador guardou para trocar quando necessario"
    nome_imagem = "sprites"
    def __init__(self, x: int, y: int):
        altura = 40
        largura = 40
        self.__cor_poder = (0, 0, 0)
        self.__corpo_poder = []
        super().__init__("poder_armazenado", x, y, altura, largura, "sprites", (205, 133, 63))
        #self.sprite = SpriteSheetBarras()

    def atualizar_hud(self, tela, mapa, dimensoes_tela):
        self.renderizar(tela, mapa)
        return False

    def renderizar(self, tela, mapa):
        "Poe na tela o icone do poder guardado"
        nome = "poder_"+mapa.jogador.poder_armazenado.nome
        self.sprite.imprimir(tela, nome, self.x-70, self.y-18, 0, 0, 0, 0)

@visivel
class BarraVidaRei(Estatico):
    "Barra de vida do Rei das Cores"
    nome_imagem = "sprites"
    def __init__(self,x:int,y:int):
        altura = 1
        largura = 657 + 72
        super().__init__("barra_rei",x,y,altura,largura,"sprites",(205, 133, 63))
        self.vida = 90
        self.vida_aparente = 900
        self.__cor = (5, 200, 40)
        self.__anti_cor = (0,0,0)
    
    @property
    def cor(self):
        return self.__cor

    @cor.setter
    def cor(self,cor):
        self.__cor = cor
        self.__anti_cor = (0,0,0) if cor[0] + cor[1] + cor[2] > 200 else (255,255,255)

    def atualizar_hud(self,tela,mapa,dimensoes_tela):
        if mapa.fase == "fase6":
            if self.vida_aparente > self.vida*10:
                self.vida_aparente -= 5
            elif self.vida_aparente < self.vida*10:
                self.vida_aparente += 5
            self.renderizar(tela, mapa)
    
    def renderizar(self, tela, mapa):
        pygame.draw.rect(tela, (160,120,88), [self.x-330,self.y-6,660,12])
        pygame.draw.rect(tela, self.cor, [self.x-330,self.y-6,self.vida_aparente/900*660,12])
        pygame.draw.rect(tela, self.__anti_cor, [self.x+110,self.y-6,3,12])
        pygame.draw.rect(tela, self.__anti_cor, [self.x-110,self.y-6,3,12])
        self.sprite.imprimir(tela,"barra_rei",self.x-365,self.y-20)