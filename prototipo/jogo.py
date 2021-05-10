import pygame, time, math, random
from jogador import Jogador
from poderes import Verde
from mapa import Mapa, carregar_mapa
from menu import *
from entidades import classes_instanciaveis
from efeitosrender import *


class Menu_Principal(Tela_Menu):  # QUASE QUE UMA INSTANCIA DA CLASSE TELA_MENU
    def __init__(self, superficie):
        botaonivel_1 = Botao(250, 75, 100, 50, (220, 0, 0), (160, 0, 0), "Fase 1", 5)
        botaonivel_2 = Botao(450, 75, 100, 50, (220, 110, 0), (160, 80, 0), "Fase 2", 5)
        botaonivel_3 = Botao(650, 75, 100, 50, (220, 220, 0), (160, 160, 0), "Fase 3", 5)
        b4 = Botao(250, 150, 100, 50, (220, 0, 110), (160, 0, 80), "Fase 4", 5)
        b5 = Botao(450, 150, 100, 50, (220, 110, 110), (160, 80, 80), "Fase 5", 5)
        b6 = Botao(650, 150, 100, 50, (220, 220, 110), (160, 160, 80), "Fase 6", 5)
        b7 = Botao(250, 225, 100, 50, (220, 0, 220), (160, 0, 160), "Fase 7", 5)
        b8 = Botao(450, 225, 100, 50, (220, 110, 220), (160, 80, 160), "Fase 8", 5)
        b9 = Botao(650, 225, 100, 50, (220, 220, 220), (160, 160, 160), "Fase 9", 5)
        botaojogar = Botao(375, 350, 250, 50, (30, 220, 30), (30, 160, 30), "Novo Jogo", 5)
        botaocontinuar = Botao(375, 405, 250, 50, (220, 220, 30), (160, 160, 30), "Carregar Jogo", 5)
        botaoconfig = Botao(375, 460, 250, 50, (0, 220, 180), (0, 160, 110), "Configurações", 5)
        botaosair = Botao(375, 515, 250, 50, (220, 30, 30), (160, 30, 30), "Sair", 5)
        cormenu = misturacor(psicodelico(0), [255, 255, 255], 1, 5)
        listabotoes = [botaosair, botaojogar, botaocontinuar, botaonivel_1, botaonivel_2,
                          botaonivel_3, botaoconfig,botaocontinuar,b4,b5,b6,b7,b8,b9]
        listatelas = [True,False,[Tela_De_Jogo,[superficie,"fase1"]],True,[Tela_De_Jogo,[superficie,"fase1"]]
                        ,[Tela_De_Jogo,[superficie,"fase2"]],[Tela_De_Jogo,[superficie,"fase3"]],True,True,True,True,True,True,True,True]
        super().__init__(listabotoes, cormenu, superficie,listatelas)
        self.__contador_menu = 0
        pygame.mixer.music.stop()


    def atualizar(self,ciclo):
        self.__contador_menu -= 0.3
        self.fundo = misturacor(psicodelico(self.__contador_menu), [200, 220, 230], 1, 5)
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT: return False
            if evento.type == pygame.MOUSEBUTTONDOWN:
                acao = self.clicar()
                return self.listatelas[acao]
        return super().atualizar()

    def menu_inicial(self):
        pass


class Tela_De_Jogo(Tela):
    def __init__(self, superficie, nivel):
        super().__init__(superficie)
        self.__background_colour = (150, 220, 255)  # Cor do fundo
        (width, height) = superficie.get_size()
        self.__campo_visivel = pygame.Rect(0, 0, width, height)
        self.__comeco = 0
        self.__tempo_maximo = 350
        self.__fonte = pygame.font.SysFont('Arial', 20)
        self.__atrasofim = 0
        self.__sobreposicao = None
        self.__musica_fundo = pygame.mixer.music.load('musica_fundo.ogg')
        pygame.mixer.music.play(-1)

        ##### ENTRADAS DO JOGADOR #####
        self.__cima, self.__baixo, self.__direita, self.__esquerda = 0, 0, 0, 0
        self.__atrito = 0.5
        self.__espaco = False
        self.__bola_fogo = False

        ###### INSTANCIAS DE OBJETOS ######
        self.__jogador = Jogador('mario', 200, -1000, 0, 1)

        ##### MAPA #####
        self.__mapa = Mapa(superficie)
        # self.__jogador = Jogador('mario',200, 0, 0, 1)
        self.__jogador = self.__mapa.iniciar(nivel)
        self.__comeco = pygame.time.get_ticks() / 1000

    def atualizar(self, ciclo):
        '''Logica de jogo, envolvendo controles, colisao e renderizacao

        Deve ser chamada pela funcdao gerente 60 vezes por segundo

        @param ciclo: responsavel pelas frames de animacao do Guri
        
        @returns: 0 se a janela for fechada
                 1 se o Guri morrer ou o tempo acabar
                 2 se o jogo continuar
                 3 se o Guri ganhar
        '''
        if isinstance(self.__sobreposicao,Sobreposicao): pausado = True
        else: pausado = False
        if not pausado:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    return False
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_w: self.__cima = 5
                    if evento.key == pygame.K_s: self.__baixo = 5
                    if evento.key == pygame.K_d:
                        self.__direita = 0.5
                    if evento.key == pygame.K_a:
                        self.__esquerda = 0.5
                    if evento.key == pygame.K_SPACE or evento.key == pygame.K_w: self.__espaco = True
                    if evento.key == pygame.K_ESCAPE:
                        self.__sobreposicao = Tela_Pause(self)
                if evento.type == pygame.KEYUP:
                    if evento.key == pygame.K_w: self.__cima = 0
                    if evento.key == pygame.K_s: self.__baixo = 0
                    if evento.key == pygame.K_d:
                        self.__direita = 0
                    if evento.key == pygame.K_a:
                        self.__esquerda = 0
                    if evento.key == pygame.K_SPACE or evento.key == pygame.K_w: self.__espaco = False
                if evento.type == pygame.MOUSEBUTTONDOWN:
                    self.__bola_fogo = True
                elif evento.type == pygame.MOUSEBUTTONUP:
                    self.__bola_fogo = False
        else:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    return False
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_ESCAPE:
                        self.__sobreposicao = None
            self.__direita = 0
            self.__esquerda = 0
            self.__cima = 0
            self.__baixo = 0
            self.__espaco = False
            self.__bola_fogo = False

        ##### FILA DE RENDERIZACAO E ATUALIZACAO #####
        self.superficie.fill(self.__background_colour)  # Preenche a cor de fundo

        self.__mapa.atualizar(self.superficie, self.__campo_visivel, self.superficie.get_size())

        # FAZER O JOGADOR RECEBER UM MAPA E SALVAR ONDE ELE TA
        if self.__atrasofim > 0:
            self.__direita = 0
            self.__esquerda = 0
            self.__espaco = not self.__mapa.ganhou
        else:
            # self.__jogador.mover(self.__direita, self.__esquerda, self.__espaco,#self.__superficie.get_size(), self.__mapa, self.__atrito)
            self.__jogador.poderes(self.superficie, self.__mapa, self.__bola_fogo)
        self.__campo_visivel = self.__jogador.atualizar(self.superficie, self.__mapa, self.__campo_visivel,
                                                        int(ciclo / 6),
                                                        [self.__direita, self.__esquerda, self.__espaco], self.__atrito)

        # PERDENDO POR MORRER
        if self.__jogador.vida <= 0 and not self.__mapa.ganhou:
            self.__jogador.vida_pra_zero()
            self.__atrasofim += 1
            if self.__atrasofim <= 1:
                if isinstance(self.__jogador.poder, Verde) and self.__mapa.conta <= 0:
                    self.__textin = self.__fonte.render("EM NOME DE DEUS LHES CASTIGAREI", False, (0, 0, 0))
                else:
                    self.__textin = self.__fonte.render("PERDEU", False, (0, 0, 0))
                pygame.mixer.music.fadeout(2400)
            else:
                self.__jogador.tipos_transparentes = classes_instanciaveis
            self.superficie.blit(self.__textin, (500 - self.__textin.get_size()[0] / 2, 300 - self.__textin.get_size()[1] / 2))
            if self.__atrasofim >= 150:
                if self.__mapa.proximo: 
                    return [Menu_Principal,[self.superficie]]

        ### VENCENDO ###
        if self.__mapa.ganhou:
            self.__atrasofim += 1
            if self.__atrasofim <= 1:
                pygame.mixer.music.fadeout(2400)
            textin = self.__fonte.render("VENCEU", False, (0, 0, 0))
            self.superficie.blit(textin, (500, 300))
            if self.__atrasofim >= 150:
                return [Tela_De_Jogo,[self.superficie, self.__mapa.proximo]] if self.__mapa.proximo else [Menu_Principal,[self.superficie]]

        ##### RENDERIZACAO DA TELA #####
        try:
            resultado = self.__sobreposicao.atualizar(ciclo)
            if not resultado:
                self.__sobreposicao = None
            elif resultado == "Fechar":
                return [Menu_Principal,[self.superficie]]
        except AttributeError:
            pass
        pygame.display.flip()
        self.__tempo_maximo += 1 / 60 - self.__mapa.escala_tempo / 60
        tempo_decorrido = pygame.time.get_ticks() / 1000 - self.__comeco
        if not self.__mapa.ganhou:
            self.__mapa.conta = int(max(self.__tempo_maximo - tempo_decorrido, 0))

        ##### PASSANDO A VIDA PRO DISPLAY #####d
        self.__mapa.vida_jogador = self.__jogador.vida

        ### PERDENDO POR TEMPO
        if self.__mapa.conta == 0:
            self.__jogador.vida_pra_zero()
        return True


class Jogo:
    def __init__(self):
        ###### INFORMACOES TA TELA ######
        (width, height) = (1000, 600)  # Tamanho da tela
        self.__screen = pygame.display.set_mode((width, height))  # Cria o objeto da tela
        pygame.display.set_caption('As Aventuras do Guri')
        self.__ciclo = 0
        self.__janela = Janela(Menu_Principal(self.__screen))
        self.__relogio = pygame.time.Clock()

    def menu_inicial(self):  # Menu inicial do jogo
        self.__janela.tela = Menu_Principal(self.__screen)
        while True:
            self.__ciclo += 1
            acao = self.__janela.tela.atualizar(self.__ciclo)

            ### se acao == 0, nao fazer nada
            ### caso contrario, fazer a acao correspondente ao botao descrito

            if acao == False:
                break
            elif isinstance(acao,list):
                self.__ciclo = 0
                self.__janela.tela = acao[0](*acao[1])
            self.__relogio.tick(60)


pygame.init()
carregar_mapa()
jogo = Jogo()
jogo.menu_inicial()
