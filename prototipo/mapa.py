from obstaculos import *
from inimigos import *
from poderes import *
from rei import *
from jogador import Jogador
from hud import *

class Mapa:
    "Classe que segura todas as entidades de um jogo"
    def __init__(self, superficie):
        self.__lista_de_entidades = []
        self.__hud = Hud(superficie.get_size())

        ##### ATRIBUTOS DE RENDERIZACAO #####
        
        self.__superficie = superficie
        tamanho_campo = superficie.get_size()
        self.__campo_visivel = pygame.Rect(0, 0, tamanho_campo[0], tamanho_campo[1])
        self.campo_menor = pygame.Rect(0, 0, tamanho_campo[0], tamanho_campo[1])
        self.__background_colour = (150, 220, 255)  # Cor do fundo

        ##### ATRIBUTOS TEMPORAIS #####
        self.__tempo_restante = ""
        self.__ciclo = 0
        self.escala_tempo = 1
        self.render_escala_tempo = 1

        ##### ATRIBUTOS COMPORTAMENTAIS #####
        self.__vida_jogador = ""
        self.__ganhou = False
        self.__moedas_pegas = ""
        self.__paletas_pegas = ""

    @property
    def lista_de_entidades(self):
        return self.__lista_de_entidades

    @property
    def ganhou(self):
        return self.__ganhou

    @ganhou.setter
    def ganhou(self, ganhou):
        self.__ganhou = ganhou

    @property
    def ciclo(self):
        return self.__ciclo

    @ciclo.setter
    def ciclo(self, ciclo):
        self.__ciclo = ciclo

    @property
    def vida_jogador(self):
        return self.__vida_jogador

    @vida_jogador.setter
    def vida_jogador(self, vida_jogador):
        self.__vida_jogador = vida_jogador

    @property
    def tempo_restante(self):
        return self.__tempo_restante

    @tempo_restante.setter
    def tempo_restante(self, tempo_restante):
        self.__tempo_restante = tempo_restante

    @property
    def campo_visivel(self):
        return self.__campo_visivel

    @property
    def tamanho(self):
        return self.__tamanho

    @property
    def jogador(self):
        return self.__jogador
    
    @property
    def proxima_fase(self):
        return self.__proxima_fase
    
    @property
    def paletas_pegas(self):
        return self.__paletas_pegas
    
    @property
    def moedas_pegas(self):
        return self.__moedas_pegas
    
    @property
    def cor_fundo(self):
        return self.__background_colour
    
    @cor_fundo.setter
    def cor_fundo(self,cor):
        self.__background_colour = cor

    def iniciar(self, fase, dicionaro_mapa, poder_atual, poder_armazenado, paletas):
        """define outras propriedades do mapa fora do __init__()
        
        return o objeto jogador a ser utilizado"""
        ##### LEITURA DAS FASES A PARTIR DO ARQUIVO JSON #####
        lista_todos = dicionaro_mapa[fase]
        objetos_no_mapa = lista_todos[0]
        for item in objetos_no_mapa:
            for classe in classes_instanciaveis:
                if item[0] == classe.__name__:
                    parametros = item[1] #Sim eh so pra ser maneiro
                    objeto = classe(*parametros)
                    self.__lista_de_entidades.append(objeto)
        self.__tamanho = lista_todos[1]
        self.__proxima_fase = lista_todos[2]

        ##### INSTANCIACAO DO JOGADOR #####
        self.__jogador = Jogador("rabisco", 200, self.tamanho[1] - 50, poder_atual, poder_armazenado, paletas)

        ##### CARREGAMENTO DAS IMAGENS DAS ENTIDADES #####
        for entidade in self.__lista_de_entidades:
            if entidade.imagem != "0": entidade.sprite = Sprite(entidade.imagem)
        return self.__jogador

    def atualizar(self, tela, campo_visivel, dimensoes_tela, ciclo):
        "Atualiza, principalmente renderiza cada objeto componente"

        self.__ciclo = ciclo #Frame atual
        self.__campo_visivel = campo_visivel #Aquilo que o jogador ve
        self.__vida_jogador = self.__jogador.vida #Pega a vida do jogador pra passar pro hud
        self.__moedas_pegas = self.__jogador.moedas#Pega as moedas que o jogador tem para passar pro hud
        self.__paletas_pegas = self.__jogador.paleta
        self.render_escala_tempo += max(min(self.escala_tempo - self.render_escala_tempo, 0.05), -0.05)
        self.cor_fundo = [180-min(self.render_escala_tempo,1)*30,
            200+min(self.render_escala_tempo,1)*20,
            210+min(self.render_escala_tempo,1)*45]
        self.__superficie.fill(self.__background_colour)  # Preenche a cor de fundo

        ##### ATUALIZACAO DAS ENTIDADES #####
        for entidade in self.__lista_de_entidades:
            if entidade.atualizar(tela, self, dimensoes_tela):
                self.__lista_de_entidades.remove(entidade)

        ##### ATUALIZACAO DO HUD #####
        self.__hud.atualizar(tela, self, dimensoes_tela, self.__tempo_restante, self.__vida_jogador
                                        , self.__moedas_pegas, self.__paletas_pegas)


