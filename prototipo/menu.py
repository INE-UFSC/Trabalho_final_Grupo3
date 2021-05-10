import pygame

class Janela:
    def __init__(self, tela):
        self.__tela = tela
    
    @property
    def tela(self):
        return self.__tela
    
    @tela.setter
    def tela(self, telanova):
        self.__tela = telanova

    def atualizar(self):
        self.tela.atualizar()


class Tela:
    def __init__(self,superficie):
        self.__superficie = superficie
    
    @property
    def superficie(self):
        return self.__superficie #superficie a se desenhar, no caso desse jogo, window
    
    def atualizar(self):
        pass


class Tela_Menu(Tela):
    def __init__(self,listabotoes:list,fundo:list,superficie,listatelas):
        super().__init__(superficie)
        self.__listatelas = listatelas
        self.__listabotoes = listabotoes        #lista de objetos Botao
        self.__fundo = fundo                    #[red,green,blue] do fundo   
    
    @property
    def fundo(self):
        return self.__fundo
    
    @fundo.setter
    def fundo(self,fundo):
        self.__fundo = fundo
    
    def atualizar(self):
        result = self.logica_menu()
        self.superficie.fill(self.__fundo)           #preenche o fundo
        for i in self.__listabotoes:            #renderiza cada botao
            i.renderizar(self.superficie)
        pygame.display.flip()
        return result
    
    def clicar(self):
        for i in self.__listabotoes:
            if i.clicar():  return self.__listabotoes.index(i)+1
        else: return 0
    
    def logica_menu(self):
        pass

    @property
    def listatelas(self):
        return self.__listatelas
    
    @property
    def listabotoes(self):
        return self.__listabotoes
    
class Botao:
    def __init__(self,x,y,w,h,cor,texto,borda,estatico=False):
        ### tamanho,posicao,cor e texto do botao
        self.__x = x-w/2
        self.__y = y-h/2
        self.__w = w
        self.__h = h
        self.__centro = [x,y,w,h]
        self.__cor = cor
        self.__corhover = [cor[0]*3/4,cor[1]*3/4,cor[2]*3/4] if not estatico else cor
        self.__textsf = pygame.font.SysFont(None,28).render(texto,True,(0,0,0))
        self.__texttamanho = self.__textsf.get_size()
        self.__borda = borda
        self.__estatico = estatico

    @property
    def cor(self):
        return self.__cor
    
    @cor.setter
    def cor(self,cor):
        self.__cor = cor
        self.__corhover = [cor[0]*3/4,cor[1]*3/4,cor[2]*3/4] if not self.__estatico else cor
    
    @property
    def texto(self):
        return self.__textsf
    
    @texto.setter
    def texto(self,texto):
        self.__textsf = pygame.font.SysFont(None,28).render(texto,True,(0,0,0))
        self.__texttamanho = self.__textsf.get_size()

    def renderizar(self,superficie):
        pos = pygame.mouse.get_pos()
        pygame.draw.rect(superficie,(0,0,0),[self.__x,self.__y,self.__w,self.__h])
        ### cor do botao depende de se o mouse esta em cima dele
        cor = self.__corhover if self.__x <= pos[0] <= self.__x + self.__w and self.__y <= pos[1] <= self.__y + self.__h else self.cor
        pygame.draw.rect(superficie,cor,[self.__x+self.__borda,self.__y+self.__borda,self.__w-2*self.__borda,self.__h-2*self.__borda])
        superficie.blit(self.__textsf,[self.__centro[0]-self.__texttamanho[0]/2,self.__centro[1]-self.__texttamanho[1]/2])
        

    def clicar(self):
        pos = pygame.mouse.get_pos()
        if self.__x <= pos[0] <= self.__x + self.__w and self.__y <= pos[1] <= self.__y + self.__h:
            return True
        else:
            return False


class Sobreposicao(Tela_Menu):
    def __init__(self,listabotoes:list,fundo:list,tela,listatelas):
        super().__init__(listabotoes,fundo,tela.superficie,listatelas)
        self.__tela_superior = tela
    
    def atualizar(self,ciclo):
        pygame.draw.rect(self.superficie,*self.fundo)
        for i in self.listabotoes:
            i.renderizar(self.superficie)
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT: return False
        if pygame.mouse.get_pressed()[0]:
            acao = self.clicar()
            return self.listatelas[acao]
        return True

