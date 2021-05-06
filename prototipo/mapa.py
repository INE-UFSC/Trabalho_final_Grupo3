from obstaculos import *
from inimigos import *
from poderes import *
from jogador import Jogador
import json

class Mapa:
    def __init__(self, tamanho_campo):
        self.__lista_de_entidades = []
        self.__lista_de_display = []
        self.__campo_visivel = pygame.Rect(0,0,tamanho_campo[0],tamanho_campo[1])
        self.__conta = ""
        self.__vitoria = pygame.Rect(tamanho_campo[0]-30, 550-30, 30, 100)
        self.__ganhou = False
        self.__vida_jogador = ""
        self.escala_tempo = 1

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
    
    @property
    def tamanho(self):
        return self.__tamanho
    
    @property
    def jogador(self):
        return self.__jogador

    def iniciar(self,entidades):
        listatipos = {"Muro":Muro,"Bloco":Bloco,"Chao":Chao,"Borda":Borda,"Vitoria":Vitoria,
            "BandanaDoNinja":BandanaDoNinja,"CartolaDoMago":CartolaDoMago,
            "OculosDoNerd":OculosDoNerd,"VerdeBebe":VerdeBebe,
            "BoneMarinheiro":BoneMarinheiro,"Rato":Rato,"Voador":Voador, "Atirador":Atirador,
            "Vida":Vida,"Tempo":Tempo,"Biscoitos":Biscoitos} 
        with open("mapas.json") as m:
            lista_mapas = json.load(m)
        lista_todos = lista_mapas[entidades]
        for item in lista_todos[0]:
            try:
                item = listatipos[item[0]](*item[1])
            except:
                item = listatipos[item[0]](item[1])
            self.__lista_de_entidades.append(item)
        for item in lista_todos[1]:
            try:
                item = listatipos[item[0]](*item[1])
            except:
                item = listatipos[item[0]](item[1])
            self.__lista_de_display.append(item)
        self.__tamanho = lista_todos[2]
        self.__jogador = Jogador("mario", 200, self.tamanho[1]-50, 0, 100)
        for entidade in self.__lista_de_entidades:
            if entidade.imagem != "0": entidade.sprite = SpriteSheet(entidade.imagem)
        return self.__jogador

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

### !!! RODAR ESTE ARQUIVO QUANDO FOR ADICIONAR MAPA !!! ###

# faseX = [
#       [["tipo",(parametros)],["tipo",(parametros)]],
#       [["tipo",(parametros)],["tipo",(parametros)]]
# ]

width = 3200
height = 700
fase1 = [[
    ["Muro",('cano1', 550, height-125, height)],
    ["Muro",('cano2', 800, height-125, height)],
    ["Muro",('cano3', 1500, height-125, height)],

    ["Bloco",('bloco1', 200, height-350)],
    ["Bloco",('bloco2', 250, height-300)],
    ["Bloco",('bloco3', 300, height-250)],
    ["Bloco",('bloco4', 350, height-200)],
    ["Bloco",('bloco4', 1000, height-200)],
    ["Bloco",('bloco4', 1020, height-200)],

    ["Chao",('chao1', height-10, -200, 350)],
    ["Chao",('chao2', height-10, 450, 2205)],
    ["Chao",('chao3', height-10, 2500, 3205)],

    ##### BORDA E VITORIA #####
    ["Vitoria",(1900,height-200,100,190)],

    ##### PODERES #####
    ["BandanaDoNinja",('shuriken1', 1200, height-100)],
    ["CartolaDoMago",('orbe1', 250, height-500)],
    ["OculosDoNerd",('oculos1', 1525, height-300)],
    ["VerdeBebe",('orbe',1600,height-50)],
    ["BoneMarinheiro",('cabelo', 1400, height-100)],
    ##### INIMIGOS #####
    ["Rato",('rato1', 610, height - 50)],
    ["Rato",('rato3', 900, height - 50)],
    ["Voador",('rato2', 100, height - 500,200)],
    ["Atirador",('atiro', 1150, height - 50)],
    ["Atirador",('atiro2', 1000, height - 205)]

],

[   ["Vida",('vida', 140, 50)],
    ["Tempo",('tempo', 470, 50)],
    ["Biscoitos",('moeda', 800, 50)]],

    (width,height)]

width = 2100
height = 600
fase2 = [[
    ["Muro",('cano1', -9000, height-125, height)],
    ["Muro",('cano2', 1600, height-125, height)],

    ["Chao",('chao1', height - 10, -1000, 2105)],

    ##### INIMIGOS #####
    ["Rato",('rato1', 100, height - 50)],
    ["Rato",('rato2', 600, height - 50)],
    ["Rato",('rato3', 1000, height - 50)],
    ["Rato",('rato4', 1200, height - 50)],
    ["Rato",('rato5', 1400, height - 50)],
    ["Voador",('voador1', 100, height - 250,200)],
    ["Voador",('voador2', 600, height - 250,200)],

    ##### BORDA E VITORIA #####
    ["Vitoria",(1900,height-200,100,190)]

],[["Vida",('vida', 140, 50)],
    ["Tempo",('tempo', 470, 50)],
    ["Biscoitos",('moeda', 800, 50)]],

    (width,height)]

width = 1000
height = 2000
fase3 = [[
    ["Muro",('cano1', -9000, height-125, height)],
    ["Muro",('cano2', 825, height-150, height)],
    ["Muro",('cano2', 500, height-75, height)],
    ["Muro",('cano3', 225, height-400, height-250)],

    ["Chao",('chao1', height - 10, 0, 1000)],
    ["Chao",('chao2', height - 250, 0, 700)],
    ["Chao",('chao3', height - 500, 400, 700)],

    ##### INIMIGOS #####
    ["Rato",('rato1', 600, height - 50)],
    

    ##### BORDA E VITORIA #####
    ["Vitoria",(500,height-690,100,190)]

],[["Vida",('vida', 140, 50)],
    ["Tempo",('tempo', 470, 50)],
    ["Biscoitos",('moeda', 800, 50)]],

    (width,height)]

with open("mapas.json",'w') as m:
    json.dump({"fase1":fase1,"fase2":fase2,"fase3":fase3},m)