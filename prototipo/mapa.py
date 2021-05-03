from obstaculos import *
from inimigos import *
from poderes import *

class Mapa:
    def __init__(self, tamanho):
        self.__tamanho = tamanho
        self.__lista_de_entidades = []
        self.__lista_de_display = []
        self.__campo_visivel = pygame.Rect(0,0,tamanho[0],tamanho[1])
        self.__conta = ""
        self.__vitoria = pygame.Rect(tamanho[0]-30, 550-30, 30, 100)
        self.__ganhou = False
        self.__vida_jogador = ""

    @property
    def lista_de_entidades(self):
        return self.__lista_de_entidades
    
    @property
    def lista_de_display(self):
        return self.__lista_de_display

    @lista_de_entidades.setter
    def lista_de_entidades(self, lista_de_entidades):
        self.__lista_de_entidades = lista_de_entidades
    
    @property
    def ganhou(self):
        return self.__ganhou

    @ganhou.setter
    def ganhou(self, ganhou):
        self.__ganhou = ganhou
    
    @property
    def vida_jogador(self):
        return self.__vida_jogador

    @vida_jogador.setter
    def vida_jogador(self, vida_jogador):
        self.__vida_jogador = vida_jogador
    
    @property
    def conta(self):
        return self.__conta

    @conta.setter
    def conta(self, conta):
        self.__conta = conta
    
    
    @property
    def campo_visivel(self):
        return self.__campo_visivel

    def iniciar(self,entidades):
        lista_todos = entidades.copy()
        #for item in lista_todos[0]: print(item.nome)
        self.__lista_de_entidades = lista_todos[0]
        for entidade in self.__lista_de_entidades:
            if entidade.imagem != "0": entidade.imagem = SpriteSheet(entidade.imagem)
        self.__lista_de_display = lista_todos[1]

    def atualizar(self, tela,campo_visivel,dimensoes_tela):
        # O CAMPO_VISIVEL FAZ COM QUE APENAS OBJETOS NA TELA SEJAM RENDERIZADOS
        # PODE AJUDAR CASO OS MAPAS FIQUEM MUITO GRANDES
        self.__campo_visivel = campo_visivel
        for entidade in self.__lista_de_entidades:
            if entidade.atualizar(tela, self, dimensoes_tela):
                self.__lista_de_entidades.remove(entidade)
        for elemento_hud in self.__lista_de_display:
            if isinstance(elemento_hud, Tempo):
                elemento_hud.tempo = self.conta
            if isinstance(elemento_hud, Vida):
                elemento_hud.vida = self.__vida_jogador

            elemento_hud.atualizar(tela,self,dimensoes_tela)

##### INSTANCIAS DE MAPAS #####

width = 1000
height = 600

fase1 = [[
    Muro('cano1', 550, 475, height),
    Muro('cano2', 800, 475, height),
    Muro('cano3', 1500, 475, height),

    Bloco('bloco1', 200, 400),
    Bloco('bloco2', 250, 400),
    Bloco('bloco3', 300, 400),
    Bloco('bloco4', 350, 400),

    Chao('chao1', height-10, -200, 350),
    Chao('chao2', height-10, 450, 2000),
    Chao('chao3', height-10, 2500, 3000),

    ##### BORDA E VITORIA #####
    Borda('borda1', 0),
    Borda('borda2', 3000),
    Vitoria(1900),

    ##### PODERES #####
    ShurikenDoNinja('shuriken1', 1200, 500),
    OrbeDoMago('orbe1', 275, 300),

    ##### INIMIGOS #####
    Rato('goomba1', 610, height - 50)

],

[   Vida('vida', 140, 50),
    Tempo('tempo', 470, 50),
    Moeda('moeda', 800, 50),]]

fase2 = [[
    Muro('cano1', -9000, 475, height),
    Muro('cano2', 1600, 475, height),

    Chao('chao1', height - 10, -1000, 2000),

    ##### INIMIGOS #####
    Rato('goomba1', 100, height - 50),
    Rato('goomba2', 600, height - 50),
    Rato('goomba3', 1000, height - 50),
    Rato('goomba4', 1200, height - 50),
    Rato('goomba5', 1400, height - 50),
    Rato('goomba6', 1600, height - 50),

    ##### BORDA E VITORIA #####
    Borda('borda1', 0),
    Borda('borda2', 2000),
    Vitoria(1900)

],[Vida('vida', 140, 50),
    Tempo('tempo', 470, 50),
    Moeda('moeda', 800, 50),]]