import mapa
import pygame
class Poder_Generico:
    def __init__(self,tem_tempo: bool, duracao: int):
        self.__tem_tempo = tem_tempo
        self.__duracao = duracao 
        'self.__nome_funcionalidade = nome_funcionalidade'

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
    '''@property
    def nome_funcionalidade (self):
        return self.__nome_funcionalidade
    
    @nome_funcionalidade.setter
    def nome_funcionalidade (self, nome_funcionalidade):
        self.__nome_funcionalidade = nome_funcionalidade'''
    
    def atirar(self):   ### ERA PRA SER ABSTRATO MAS FDS
        pass

class VermelhoDoMago(Poder_Generico):
    def __init__(self):
        super().__init__(False,0)
        self.__bolas = []
    def atirar(self,jogador,screen,mapa):
        self.__bolas.append(BolaFogo([jogador.x,jogador.y], screen, mapa, jogador.face))
    def atualizar(self,tela,campo_visivel):
        for fogo in self.__bolas:
            if fogo.atualizar(tela,campo_visivel):
                self.__bolas.remove(fogo)

class BolaFogo:
    def __init__(self, pos_inicial , screen, mapa, vel):
        self.vida = 1
        self.largura = 15
        self.altura = 15
        self.duracao = 100
        self.mapa = mapa
        self.vely = 0
        self.velx = 3 * vel
        self.x = pos_inicial[0] + 25 * vel
        self.y = pos_inicial[1]
        self.__corpo = pygame.Rect(self.x, self.y, self.largura, self.altura)

    @property
    def corpo(self):
        return self.__corpo
    
    @corpo.setter
    def corpo(self, corpo):
        self.__corpo = corpo
    
    ###TESTE###
    def checar_colisao(self, corpo):
        colisaoBaixo, colisaoCima, colisaoEsquerda, colisaoDireita = False, False, False, False
        corpoLargo = pygame.Rect(self.x-1, self.y-1, self.largura+2,self.altura+2)
        colisaoAjustada = corpoLargo.colliderect(corpo)
        if colisaoAjustada:
            ##### VERTICAIS #####
            '''if self.corpo.left in range(corpo.left+1, corpo.right-1) or self.corpo.right in range(corpo.left+1, corpo.right-1):
                if corpoLargo.bottom in range(corpo.top+1, corpo.bottom-1 + int(self.vely)):
                    colisaoBaixo = True
                elif corpoLargo.top in range(corpo.top+1+ int(self.vely), corpo.bottom-1):
                    colisaoCima = True'''
            ##### HORIZONTAIS #####
            '''print(f'SEILA {self.corpo.top} =? {corpo.top+1, corpo.bottom-1}')
            print(f'SEILA2 {self.corpo.bottom} =? {corpo.top+1, corpo.bottom-1}')
            print(f'SEILA3 {self.corpo.top} =? {corpo.top+1, corpo.bottom-1}')
            print(f'SEILA4{colisaoCima, colisaoBaixo}')'''

            if (self.corpo.top in range(corpo.top+1, corpo.bottom-1) or self.corpo.bottom in range(corpo.top+1, corpo.bottom-1)):
                ###TIREI DO IF da LINHA 77  and (not colisaoCima and not colisaoBaixo)                
                if corpoLargo.right in range(corpo.left+1, corpo.right-1 + int(self.velx)):
                    colisaoDireita = True
                ###POR ENQUANTO É INÚTIL PQ SÓ JOGA PODER PELA DIREITA
                if corpoLargo.left in range(corpo.left+1 + int(self.velx), corpo.right-1):
                    colisaoEsquerda = True
        return [colisaoCima, colisaoBaixo, colisaoDireita, colisaoEsquerda]

    def mover(self):

        ##### COLISOES #####
        colisaoCima, colisaoBaixo, colisaoEsquerda, colisaoDireita = False, False, False, False
        cCima, cBaixo, cEsquerda, cDireita = False, False, False, False
        obsBaixo, obsCima, obsEsquerda, obsDireita = 0,0,0,0

        ##### COLISOES COM OBSTACULOS #####
        
        for obstaculo in self.mapa.lista_de_entidades:

            cCima, cBaixo, cDireita, cEsquerda = self.checar_colisao(obstaculo.corpo)
            #print(f'{cDireita}')

            # Essa checagem em dois passos tem que ocorrer por que se nao ele so salva a colisao com o utlimo obstaculo
            ## Inutil enquanto a bola so vai reto e so 
            '''if cCima:
                colisaoCima = True
                obsCima = obstaculo
            if cBaixo:
                colisaoBaixo = True
                obsBaixo = obstaculo'''
            if cEsquerda:
                colisaoEsquerda = True
                obsEsquerda = obstaculo
            if cDireita:
                colisaoDireita = True
                obsDireta = obstaculo
                print('ENTROU NA 109')
            

        ##### HORIZONTAIS #####
        if colisaoEsquerda or colisaoDireita:
            self.duracao = 0
            #self.velx = 0

        ##### VERTICAIS #####
        '''if colisaoBaixo:
            self.vely = 0
            #self.y = obsBaixo.corpo.top - self.altura'''

        self.y += self.vely
        self.x += self.velx

    def atualizar(self, tela, campo_visivel):
        if (self.duracao >  0):
            self.mover()
            self.corpo.x = self.x
            self.corpo.y = self.y
            pygame.draw.rect(tela, [245,87+self.duracao,65], [self.corpo.x-campo_visivel.x-50,self.corpo.y,self.corpo.w,self.corpo.h])
            self.duracao -= 1
            return False
        return True