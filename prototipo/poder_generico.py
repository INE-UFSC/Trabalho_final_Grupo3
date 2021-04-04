import mapa
import pygame
class Poder_Generico():
    def __init__(tem_tempo: bool, duracao: int, nome_funcionalidade: str):
        self.__tem_tempo = tem_tempo
        self.__duracao = durcao 
        self.__nome_funcionalidade = nome_funcionalidade

    @property
    def tem_tempo (self):
        return self.__tem_tempo
    
    @tem_tempo.setter
    def tem_tempo (self, tem_tempo):
        self.__tem_tempo = tem_tempo
    
    @property
    def duracao (self):
        return self.__duracao
    
    @duracao.setter
    def duracao (self, duracao):
        self.__duracao = duracao
    @property
    def nome_funcionalidade (self):
        return self.__nome_funcionalidade
    
    @nome_funcionalidade.setter
    def nome_funcionalidade (self, nome_funcionalidade):
        self.__nome_funcionalidade = nome_funcionalidade

class BolaFogo(Poder_Generico):
    def __init__(self, pos_inicial , screen, mapa):
        danoContato = 1
        largura = 15
        altura = 15
        limVel = 4
        self.mapa = mapa
        self.vely = 0
        self.velx = 1
        self.x = pos_inicial[0]
        self.y = pos_inicial[1]
        self.__corpo = pygame.Rect(self.x, self.y, largura, altura)

    @property
    def corpo(self):
        return self.__corpo
    
    @corpo.setter
    def corpo(self, corpo):
        self.__corpo = corpo

    def mover(self):
        self.x += 3.5

    def atualizar(self, tela):
        self.mover()
        self.corpo.x = self.x
        self.corpo.y = self.y
        pygame.draw.rect(tela, (205,157,205), self.corpo)


        