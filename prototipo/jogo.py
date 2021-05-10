import pygame, time, math, random, json
from jogador import Jogador
from poderes import Verde
from mapa import Mapa, carregar_mapa
from menu import *
from entidades import classes_instanciaveis
from efeitosrender import *


class Tela_Pause(Sobreposicao):
    def __init__(self,tela):
        continuar = Botao(400, 350, 200, 50, (220, 0, 0), "Continuar", 5)
        sair = Botao(400, 410, 200, 50, (220, 0, 0), "Sair", 5)
        listabotoes = [continuar,sair]
        listatelas = [True,False,"Fechar"]
        super().__init__(listabotoes,((50,50,50),(380,340,240,130)),tela,listatelas)


class Menu_Principal(Tela_Menu):  # QUASE QUE UMA INSTANCIA DA CLASSE TELA_MENU
    def __init__(self, superficie):
        botaonivel_1 = Botao(250, 75, 100, 50, (220, 0, 0), "Fase 1", 5)
        botaonivel_2 = Botao(450, 75, 100, 50, (220, 110, 0), "Fase 2", 5)
        botaonivel_3 = Botao(650, 75, 100, 50, (220, 220, 0), "Fase 3", 5)
        b4 = Botao(250, 150, 100, 50, (220, 0, 110), "Fase 4", 5)
        b5 = Botao(450, 150, 100, 50, (220, 110, 110), "Fase 5", 5)
        b6 = Botao(650, 150, 100, 50, (220, 220, 110),  "Fase 6", 5)
        b7 = Botao(250, 225, 100, 50, (220, 0, 220),  "Fase 7", 5)
        b8 = Botao(450, 225, 100, 50, (220, 110, 220),  "Fase 8", 5)
        b9 = Botao(650, 225, 100, 50, (220, 220, 220),  "Fase 9", 5)
        botaojogar = Botao(375, 350, 250, 50, (30, 220, 30),  "Jogar", 5)
        botaocontinuar = Botao(375, 405, 250, 50, (220, 220, 30),  "-", 5)
        botaoconfig = Botao(375, 460, 250, 50, (0, 220, 180), "Configurações", 5)
        botaosair = Botao(375, 515, 250, 50, (220, 30, 30), "Sair", 5)
        cormenu = misturacor(psicodelico(0), [255, 255, 255], 1, 5)
        listabotoes = [botaosair, botaojogar, botaocontinuar, botaonivel_1, botaonivel_2,
                          botaonivel_3, botaoconfig,botaocontinuar,b4,b5,b6,b7,b8,b9]
        listatelas = [True,False,[Carregar_Jogo,[superficie]],True,[Tela_De_Jogo,[superficie,"fase1",'6']]
                ,[Tela_De_Jogo,[superficie,"fase2",'6']],[Tela_De_Jogo,[superficie,"fase3",'6']],True,True,True,True,True,True,True,True]
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


class Carregar_Jogo(Tela_Menu):
    def __init__(self,superficie):
        try:
            with open("saves.json","r") as saves:
                slots = json.load(saves)
        except:
            with open("saves.json","w") as saves:
                slots = {'0':["Novo Jogo","fase1"],'1':["Novo Jogo","fase1"],'2':["Novo Jogo","fase1"]
                          ,'3':["Novo Jogo","fase1"],'4':["Novo Jogo","fase1"]}
                json.dump(slots,saves)
        
        encaixe = [slots[str(i)] for i in range(5)]
        deletar_encaixe = ["Deletar" if slots[str(i)][0] != "Novo Jogo" else False for i in range(5)]

        botoes_encaixe = [Botao(150, 200+60*i, 500, 50, (60, 220, 20), encaixe[i][0], 5) if deletar_encaixe[i] == "Deletar"
                        else Botao(150, 200+60*i, 500, 50, (160, 160, 160), encaixe[i][0], 5) for i in range(5)]
        sair = Botao(75, 520, 200, 50, (220, 20, 60), "Sair", 5)
        botoes_deletar = [Botao(700, 205+60*i, 100, 40, (220, 20, 60), "Deletar", 5) if deletar_encaixe[i] == "Deletar" 
                        else Botao(-1000, -1000, 50, 50, (0,0,0), "", 5) for i in range(5)]
        texto = Botao(100, 50, 400, 100, (200, 200, 200), "Escolha de Jogo Salvo", 5)
        
        listabotoes = botoes_encaixe + botoes_deletar + [sair] + [texto]

        listatelas = [True] + [[Tela_De_Jogo,
                               [superficie,encaixe[i][1],str(i)]] 
                               for i in range(5)] + [[Deletar_Save,
                                                     [superficie,str(i)]] 
                                                     for i in range(5)] + [[Menu_Principal,[superficie]]] + [True]

        cormenu = misturacor(psicodelico(0), [255, 255, 255], 1, 5)
        super().__init__(listabotoes,cormenu,superficie,listatelas)
        self.__contador_menu = 0

    
    def atualizar(self,ciclo):
        self.__contador_menu -= 0.3
        self.fundo = misturacor(psicodelico(self.__contador_menu), [200, 220, 230], 1, 5)
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT: return False
            if evento.type == pygame.MOUSEBUTTONDOWN:
                acao = self.clicar()
                return self.listatelas[acao]
        return super().atualizar()


class Deletar_Save(Tela_Menu):
    def __init__(self,superficie,save):
        self.__save = save
        texto = Botao(200, 170, 600, 150, (200, 200, 200), "Quer mesmo deletar esse jogo salvo?", 5)
        deletar = Botao(150, 350, 320, 50, (220, 20, 60), "Deletar", 5)
        cancelar = Botao(530, 350, 320, 50, (60, 220, 20), "Cancelar", 5)
        listabotoes = [deletar,cancelar,texto]
        listatelas = [True,[Carregar_Jogo,[superficie]],[Carregar_Jogo,[superficie]],True]
        cormenu = misturacor(psicodelico(0), [255, 255, 255], 1, 5)
        super().__init__(listabotoes,cormenu,superficie,listatelas)
        self.__contador_menu = 0

    def atualizar(self,ciclo):
        self.__contador_menu -= 0.3
        self.fundo = misturacor(psicodelico(self.__contador_menu), [200, 220, 230], 1, 5)
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT: return False
            if evento.type == pygame.MOUSEBUTTONDOWN:
                acao = self.clicar()
                if acao == 1:
                    with open("saves.json","r") as saves:
                        slots = json.load(saves)
                    slots[self.__save] = ["Novo Jogo","fase1"]
                    with open("saves.json","w") as saves:
                        json.dump(slots,saves)
                return self.listatelas[acao]
        return super().atualizar()


class Fim_De_Jogo(Tela_Menu):
    def __init__(self,superficie,nivel,save):
        texto = Botao(200, 170, 600, 150, (200, 200, 200), "Você perdeu...", 5)
        continuar = Botao(530, 350, 320, 50, (160, 220, 60), "Tentar Novamente", 5)
        voltar = Botao(150, 350, 320, 50, (220, 220, 60), "Menu Principal", 5)
        listabotoes = [voltar,continuar,texto]
        listatelas = [True,[Menu_Principal,[superficie]],[Tela_De_Jogo,[superficie,nivel,save]],True]
        cormenu = misturacor(psicodelico(0), [255, 255, 255], 1, 5)
        super().__init__(listabotoes,cormenu,superficie,listatelas)
        self.__contador_menu = 0

    def atualizar(self,ciclo):
        self.__contador_menu -= 0.3
        self.fundo = misturacor(psicodelico(self.__contador_menu), [200, 220, 230], 1, 5)
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT: return False
            if evento.type == pygame.MOUSEBUTTONDOWN:
                acao = self.clicar()
                return self.listatelas[acao]
        return super().atualizar()


class Configuracoes(Tela_Menu):
    def __init__(self,superficie):
        texto = Botao(200, 170, 600, 150, (200, 200, 200), "Você perdeu...", 5)
        continuar = Botao(530, 350, 320, 50, (160, 220, 60), "Tentar Novamente", 5)
        voltar = Botao(150, 350, 320, 50, (220, 220, 60), "Menu Principal", 5)
        listabotoes = [voltar,continuar,texto]
        listatelas = [True,[Menu_Principal,[superficie]],[Tela_De_Jogo,[superficie,nivel,save]],True]
        cormenu = misturacor(psicodelico(0), [255, 255, 255], 1, 5)
        super().__init__(listabotoes,cormenu,superficie,listatelas)
        self.__contador_menu = 0


class Tela_De_Jogo(Tela):
    def __init__(self, superficie, nivel,slot):
        super().__init__(superficie)
        self.__background_colour = (150, 220, 255)  # Cor do fundo
        (width, height) = superficie.get_size()
        self.__campo_visivel = pygame.Rect(0, 0, width, height)
        self.__comeco = 0
        self.__tempo_maximo = 350
        self.__fonte = pygame.font.SysFont('Arial', 20)
        self.__atrasofim = 0
        self.__nivel = nivel
        self.__slot = slot
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
    
    def salvar_jogo(self):
        with open("saves.json","r") as saves:
            slots = json.load(saves)
            slots[self.__slot] = [self.__nivel,self.__nivel]
        with open("saves.json","w") as saves:
            json.dump(slots,saves)

    def atualizar(self, ciclo):
        '''Logica de jogo, envolvendo controles, colisao e renderizacao

        Deve ser chamada pela funcdao gerente 60 vezes por segundo

        @param ciclo: responsavel pelas frames de animacao do Rabisco
        
        @returns: 0 se a janela for fechada
                 1 se o Rabisco morrer ou o tempo acabar
                 2 se o jogo continuar
                 3 se o Guri ganhar
        '''
        if isinstance(self.__sobreposicao,Sobreposicao): pausado = True
        else: pausado = False
        if not pausado:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    self.salvar_jogo()
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
                    self.salvar_jogo()
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

        self.__mapa.atualizar(self.superficie, self.__campo_visivel, self.superficie.get_size(),ciclo)

        # FAZER O JOGADOR RECEBER UM MAPA E SALVAR ONDE ELE TA
        if self.__atrasofim > 0:
            self.__direita = 0
            self.__esquerda = 0
            self.__espaco = not self.__mapa.ganhou
        else:
            # self.__jogador.mover(self.__direita, self.__esquerda, self.__espaco,#self.__superficie.get_size(), self.__mapa, self.__atrito)
            self.__jogador.poderes(self.superficie, self.__mapa, self.__bola_fogo)
        self.__campo_visivel = self.__jogador.atualizar(self.superficie,self.__mapa, self.__campo_visivel, int(ciclo / 6),
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
                self.salvar_jogo()
                return [Fim_De_Jogo,[self.superficie,self.__nivel,self.__slot]]

        ### VENCENDO ###
        if self.__mapa.ganhou:
            self.__atrasofim += 1
            if self.__atrasofim <= 1:
                pygame.mixer.music.fadeout(2400)
            textin = self.__fonte.render("VENCEU", False, (0, 0, 0))
            self.superficie.blit(textin, (500, 300))
            if self.__atrasofim >= 150:
                self.salvar_jogo
                return [Tela_De_Jogo, [self.superficie, self.__mapa.proxima_fase, self.__slot]] if self.__mapa.proxima_fase else [Menu_Principal, [self.superficie]]

        ##### RENDERIZACAO DA TELA #####
        try:
            resultado = self.__sobreposicao.atualizar(ciclo)
            if not resultado:
                self.__sobreposicao = None
            elif resultado == "Fechar":
                self.salvar_jogo()
                return [Fim_De_Jogo,[self.superficie,self.__nivel,self.__slot]]
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
        caption = ["As Aventuras do Guri",
                   "A Aventura Bizarra de Guri",
                   "Super Guri Bros",
                   "Arte-lharia",
                   "Uma Pincelada de Vigor",
                   "Entre Riscos e Riscos"]
        pygame.display.set_caption(random.choices(caption,[6,1,1,4,4,4])[0])
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
                self.__janela.tela = acao[0](*acao[1])
            self.__relogio.tick(60)


pygame.init()
carregar_mapa()
jogo = Jogo()
jogo.menu_inicial()
