import pygame, time, math, random, json
from jogador import Jogador
from poderes import Verde
from mapa import Mapa, carregar_mapa
from menu import *
from entidades import classes_instanciaveis, renderizar_hitbox
from efeitosrender import *


class Tela_Pause(Sobreposicao):
    def __init__(self,tela):
        continuar = Botao(tela.superficie.get_size()[0]/2, tela.superficie.get_size()[1]/2, 200, 50, (220, 0, 0), "Continuar", 5)
        sair = Botao(tela.superficie.get_size()[0]/2, tela.superficie.get_size()[1]/2+60, 200, 50, (220, 0, 0), "Sair", 5)
        listabotoes = [continuar,sair]
        listatelas = [True,False,"Fechar"]
        super().__init__(listabotoes,((50,50,50),(tela.superficie.get_size()[0]/2-120,tela.superficie.get_size()[1]/2-35,240,130)),tela,listatelas)


class Menu_Principal(Tela_Menu):  # QUASE QUE UMA INSTANCIA DA CLASSE TELA_MENU
    def __init__(self, superficie):
        t = superficie.get_size()
        botaonivel_1 = Botao(t[0]/5, t[1]/12, 100, 50, (220, 0, 0), "Fase 1", 5)
        botaonivel_2 = Botao(t[0]/2, t[1]/12, 100, 50, (220, 110, 0), "Fase 2", 5)
        botaonivel_3 = Botao(t[0]*4/5, t[1]/12, 100, 50, (220, 220, 0), "Fase 3", 5)
        b4 = Botao(t[0]/5, t[1]/4-5, 100, 50, (220, 0, 110), "Fase 4", 5)
        b5 = Botao(t[0]/2, t[1]/4-5, 100, 50, (220, 110, 110), "Fase 5", 5)
        b6 = Botao(t[0]*4/5, t[1]/4-5, 100, 50, (220, 220, 110),  "Fase 6", 5)
        b7 = Botao(t[0]/5, t[1]*5/12-10, 100, 50, (220, 0, 220),  "Fase 7", 5)
        b8 = Botao(t[0]/2, t[1]*5/12-10, 100, 50, (220, 110, 220),  "Fase 8", 5)
        b9 = Botao(t[0]*4/5, t[1]*5/12-10, 100, 50, (220, 220, 220),  "Fase 9", 5)
        botaojogar = Botao(t[0]/2, t[1]*2/3-20, 250, 50, (30, 220, 30),  "Jogar", 5)
        botaoconfig = Botao(t[0]/2, t[1]*3/4, 250, 50, (0, 220, 180), "Configurações", 5)
        botaosair = Botao(t[0]/2, t[1]*5/6+20, 250, 50, (220, 30, 30), "Sair", 5)
        cormenu = misturacor(psicodelico(0), [255, 255, 255], 1, 5)
        listabotoes = [botaosair, botaojogar, botaonivel_1, botaonivel_2,
                          botaonivel_3, botaoconfig,b4,b5,b6,b7,b8,b9]
        listatelas = [True,False,[Carregar_Jogo,[superficie]],[Tela_De_Jogo,[superficie,"fase1",'6']]
                ,[Tela_De_Jogo,[superficie,"fase2",'6']],[Tela_De_Jogo,[superficie,"fase3",'6']],[Configuracoes,[superficie]],True,True,True,True,True,True]
        super().__init__(listabotoes, cormenu, superficie,listatelas)
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

        t = superficie.get_size()
        botoes_encaixe = [Botao(t[0]/3, max(75,t[1]/10)+i*max(60,t[1]/8), max(t[0]*2/3,400), 50, (60, 220, 20), encaixe[i][0], 5) if deletar_encaixe[i] == "Deletar"
                        else Botao(t[0]/3,  max(75,t[1]/10)+i*max(60,t[1]/8), max(t[0]*2/3,400), 50, (160, 160, 160), encaixe[i][0], 5) for i in range(5)]
        sair = Botao(90,t[1]-35, 160, 50, (220, 20, 60), "Sair", 5)
        botoes_deletar = [Botao(t[0]*3/4,  max(75,t[1]/10)+i*max(60,t[1]/8), 100, 40, (220, 20, 60), "Deletar", 5) if deletar_encaixe[i] == "Deletar" 
                        else Botao(-1000, -1000, 50, 50, (0,0,0), "", 5) for i in range(5)]
        texto = Botao(200, 20, 400, 40, (200, 200, 200), "Escolha de Jogo Salvo", 5,True)
        
        listabotoes = botoes_encaixe + botoes_deletar + [sair] + [texto]

        listatelas = [True]
        listatelas += [[Tela_De_Jogo,[superficie,encaixe[i][1],str(i)]] for i in range(5)]
        listatelas += [[Deletar_Save,[superficie,str(i)]] for i in range(5)]
        listatelas += [[Menu_Principal,[superficie]]] + [True]

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
        t = superficie.get_size()
        self.__save = save
        texto = Botao(t[0]/2, t[1]/3, 550, 150, (200, 200, 200), "Quer mesmo deletar esse jogo salvo?", 5,True)
        deletar = Botao(t[0]/2+150, t[1]/3+150, 260, 50, (220, 20, 60), "Deletar", 5)
        cancelar = Botao(t[0]/2-150, t[1]/3+150, 260, 50, (60, 220, 20), "Cancelar", 5)
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
        t = superficie.get_size()
        texto = Botao(t[0]/2, t[1]/3, 550, 150, (200, 200, 200), "Você perdeu...", 5,True)
        continuar = Botao(t[0]/2+150, t[1]/3+150, 260, 50, (160, 220, 60), "Tentar Novamente", 5)
        voltar = Botao(t[0]/2-150, t[1]/3+150, 260, 50, (220, 220, 60), "Menu Principal", 5)
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
        self.__mudanca_tamanho = False
        self.__tamanho = list(superficie.get_size())
        t = self.__tamanho
    
        sair = Botao(120, t[1]-45, 200, 50, (220, 60, 60), "Voltar", 5)

        musica = Botao(360, 120, 140, 50, (200, 200, 200), "Musica: "+ str(int(round(pygame.mixer.music.get_volume(),1)*100)), 5,True)
        musica_mais = Botao(360, 70, 40, 40, (160, 220, 60), "+", 5)
        musica_menos = Botao(360, 170, 40, 40, (220, 160, 60), "-", 5)

        efeitos = Botao(520, 120, 140, 50, (200, 200, 200), "Efeitos:100", 5,True)
        efeitos_mais = Botao(520, 70, 40, 40, (160, 220, 60), "+", 5)
        efeitos_menos = Botao(520, 170, 40, 40, (220, 160, 60), "-", 5)

        tela = Botao(140, 120, 120, 80, (200, 200, 200), "({}x{})".format(*self.__tamanho), 5,True)
        tela_largura_menos = Botao(40, 120, 60, 40, (220, 160, 60), "-100", 5)
        tela_largura_mais = Botao(240, 120, 60, 40, (160, 220, 60), "+100", 5)
        tela_altura_menos = Botao(140, 190, 60, 40, (220, 160, 60), "-100", 5)
        tela_altura_mais = Botao(140, 50, 60, 40, (160, 220, 60), "+100", 5)

        listabotoes = [sair,musica,musica_mais,musica_menos,efeitos,efeitos_mais,efeitos_menos,
                        tela,tela_largura_menos,tela_largura_mais,tela_altura_menos,tela_altura_mais]
        listatelas = [True,[Menu_Principal,[superficie]]] + [True for i in range(11)]
        cormenu = misturacor(psicodelico(0), [255, 255, 255], 1, 5)
        super().__init__(listabotoes,cormenu,superficie,listatelas)
        self.__contador_menu = 0

    def atualizar(self,ciclo):
        global renderizar_hitbox
        self.__contador_menu -= 0.3
        self.fundo = misturacor(psicodelico(self.__contador_menu), [200, 220, 230], 1, 5)
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT: return False
            if evento.type == pygame.MOUSEBUTTONDOWN:
                acao = self.clicar()
                if acao == 1:
                    pygame.display.set_mode(self.__tamanho)
                elif acao == 3:
                    pygame.mixer.music.set_volume(min(round(pygame.mixer.music.get_volume(),1)+0.1,1))
                    self.listabotoes[1].texto = "Musica: "+ str(int(round(pygame.mixer.music.get_volume(),1)*100))
                elif acao == 4:
                    pygame.mixer.music.set_volume(max(round(pygame.mixer.music.get_volume(),1)-0.1,0))
                    self.listabotoes[1].texto = "Musica: "+ str(int(round(pygame.mixer.music.get_volume(),1)*100))
                elif acao == 9:
                    self.__tamanho[0] = max(600,self.__tamanho[0]-100)
                elif acao == 10:
                    self.__tamanho[0] = min(1400,self.__tamanho[0]+100)
                elif acao == 11:
                    self.__tamanho[1] = max(400,self.__tamanho[1]-100)
                elif acao == 12:
                    self.__tamanho[1] = min(900,self.__tamanho[1]+100)
                self.listabotoes[7].texto = "({}x{})".format(*self.__tamanho)
                return self.listatelas[acao]
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    pygame.display.set_mode(self.__tamanho)
                    return self.listatelas[1]
        return super().atualizar()

    def salvar_config(self):
        pass

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
        pygame.mixer.music.play(-1)

        ##### ENTRADAS DO JOGADOR #####
        self.__cima, self.__baixo, self.__direita, self.__esquerda = 0, 0, 0, 0
        self.__atrito = 0.5
        self.__espaco = False
        self.__bola_fogo = False
        self.__troca_poder = False

        ###### INSTANCIAS DE OBJETOS ######
        self.__jogador = Jogador('mario', 200, -1000, 0, 1)

        ##### MAPA #####
        self.__mapa = Mapa(superficie)
        # self.__jogador = Jogador('mario',200, 0, 0, 1)
        self.__jogador = self.__mapa.iniciar(nivel,dicionaro_mapa)
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
        
        @returns: Instancia da proxima tela a ser executada apos o nivel
                  Ou False se o jogo for fechado
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
                    if evento.key == pygame.K_TAB:
                        self.__troca_poder = True
                if evento.type == pygame.KEYUP:
                    if evento.key == pygame.K_w: self.__cima = 0
                    if evento.key == pygame.K_s: self.__baixo = 0
                    if evento.key == pygame.K_d:
                        self.__direita = 0
                    if evento.key == pygame.K_a:
                        self.__esquerda = 0
                    if evento.key == pygame.K_SPACE or evento.key == pygame.K_w: self.__espaco = False
                    if evento.key == pygame.K_TAB:
                        self.__troca_poder = False
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
            self.__troca_poder = False

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
                                                        [self.__direita, self.__esquerda, self.__espaco, self.__troca_poder], self.__atrito)

        # PERDENDO POR MORRER
        if self.__jogador.vida <= 0 and not self.__mapa.ganhou:
            self.__jogador.vida_pra_zero()
            self.__atrasofim += 1
            if self.__atrasofim <= 1:
                if isinstance(self.__jogador.poder, Verde) and self.__mapa.__tempo_restante <= 0:
                    self.__textin = self.__fonte.render("EM NOME DE DEUS LHES CASTIGAREI", False, (0, 0, 0))
                else:
                    self.__textin = self.__fonte.render("PERDEU", False, (0, 0, 0))
                pygame.mixer.music.fadeout(2400)
            else:
                self.__jogador.tipos_transparentes = classes_instanciaveis
            self.superficie.blit(self.__textin, (self.__campo_visivel.w/2 - self.__textin.get_size()[0] / 2, self.__campo_visivel.h/2 - self.__textin.get_size()[1] / 2))
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
            self.__mapa.tempo_restante = int(max(self.__tempo_maximo - tempo_decorrido, 0))

        ### PERDENDO POR TEMPO
        if self.__mapa.tempo_restante == 0:
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
pygame.mixer.music.load('musica_fundo.ogg')
pygame.mixer.music.set_volume(1)
carregar_mapa()
with open("mapas.json","r") as objeto_mapas:
    dicionaro_mapa = json.load(objeto_mapas)
jogo = Jogo()
jogo.menu_inicial()
