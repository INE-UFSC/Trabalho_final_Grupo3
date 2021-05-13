from entidades import *
from inimigos import *
from poderes import *

class ParteDoRei(Entidade):
    def __init__(self, nome: str, x: int, y: int, altura: int, largura: int, limiteVel: int, vida: int, dano_contato: int, imagem: str, cor, frames: int):
        super().__init__(nome, x, y, altura, largura, limiteVel, vida, dano_contato, imagem, cor, frames)

@instanciavel
class PunhoVermelho(ParteDoRei):
    def __init__(self, x, y, lado):
        self.__centro_x = x
        self.__centro_y = y
        self.__rei = []
        self.__lado = lado
        self.__montado = False
        altura = 50
        largura = 50
        dano_contato = 1
        cor = (255,0,0)
        limiteVel = 10
        super().__init__("punho", x, y, altura, largura, limiteVel, 0, dano_contato, "0", cor, 0)

    def montar(self, mapa):
        for entidade in mapa.lista_de_entidades:
            if type(entidade) == ReiDasCores:
                self.__montado = True
                self.__rei = entidade
                if self.__lado == "esquerdo":
                    entidade.punho_esquerdo = self
                else:
                    entidade.punho_direito = self

    def atualizar(self, tela, mapa, dimensoes_tela):
        if not self.__montado: self.montar(mapa)
        self.renderizar(tela, mapa)
        ##### ATUALIZACAO DO CORACAO #####
        if self.__lado == "direito":
            self.x = self.__rei.x + 200
            self.y = self.__rei.y + 100
        else:
            self.x = self.__rei.x - 100
            self.y = self.__rei.y + 100
        self.corpo = pygame.Rect(self.x, self.y, self.largura, self.altura)

    def lancar(self, mapa, jogador):
        pass

    def sofreu_colisao_jogador(self, jogador, direcao, mapa):
        "Detecta colisao com jogador, return dano caso valido"
        ##### COLISAO ESQUERDA #####
        if not jogador.invisivel:
            if direcao == "esquerda":
                if jogador.velx <= 0:
                    jogador.velx = 0
                    jogador.aceleracao = 0
                    jogador.x = self.corpo.right + 1
                return self.dano_contato
            ##### COLISAO DIREITA #####
            elif direcao == "direita":
                if jogador.velx >= 0:
                    jogador.velx = 0
                    jogador.aceleracao = 0
                    jogador.x = self.corpo.left - jogador.largura
                return self.dano_contato
            ##### COLISAO BAIXO #####
            elif direcao == "baixo":
                jogador.vely = 0
                jogador.y = self.corpo.top - jogador.altura
                return self.dano_contato
            ##### COLISAO CIMA #####
            elif direcao == "cima":
                if jogador.vely < 0:
                    jogador.vely = 0
                    jogador.y = self.corpo.bottom
                return self.dano_contato
        else:
            return 0

@instanciavel
class CabecaLaranja(ParteDoRei):
    def __init__(self, x, y):
        self.__rei = 0
        self.__vel_projetil = 3
        self.__descanso_poder_max = 125
        self.__descanso_poder = randrange(0, 25)
        self.__numero_de_projeteis = 1
        self.__poder = Projetil()
        self.__montado = False
        altura = 50
        largura = 50
        dano_contato = 1
        cor = (255,128,0)
        limiteVel = 10
        super().__init__("cabeca", x, y, altura, largura, limiteVel, 0, dano_contato, "0", cor, 0)

    @property
    def descanso_poder_max(self):
        return self.__descanso_poder_max

    @descanso_poder_max.setter
    def descanso_poder_max(self, descanso_poder_max):
        self.__descanso_poder_max = descanso_poder_max

    @property
    def numero_de_projeteis(self):
        return self.__numero_de_projeteis

    @numero_de_projeteis.setter
    def numero_de_projeteis(self, numero_de_projeteis):
        self.__numero_de_projeteis = numero_de_projeteis

    def montar(self, mapa):
        for entidade in mapa.lista_de_entidades:
            if type(entidade) == ReiDasCores:
                print()
                self.__montado = True
                self.__rei = entidade
                entidade.cabeca = self

    def atualizar(self, tela, mapa, dimensoes_tela):
        if not self.__montado: self.montar(mapa)
        self.renderizar(tela, mapa)
        ##### ATUALIZACAO DO CORACAO #####
        self.x = self.__rei.x + 50
        self.y = self.__rei.y -50
        self.corpo = pygame.Rect(self.x, self.y, self.largura, self.altura)

        if mapa.jogador.x <= self.x:
            dstancia = (((mapa.jogador.y + mapa.jogador.altura) - (self.y + self.altura)) ** 2 + (
                    mapa.jogador.x - self.x - 15 * self.face) ** 2) ** (1 / 2)
            divisor = max(dstancia / self.__vel_projetil, 0.001)
            velx = (mapa.jogador.x - self.x - 15 * self.face) / divisor
        else:
            dstancia = (((mapa.jogador.y + mapa.jogador.altura) - (self.y + self.altura)) ** 2 + (
                    mapa.jogador.x - self.corpo.bottomright[0] - 15 * self.face) ** 2) ** (1 / 2)
            divisor = max(dstancia / self.__vel_projetil, 0.001)
            velx = (mapa.jogador.x - self.corpo.bottomright[0] - 15 * self.face) / divisor
        vely = ((mapa.jogador.y) - (self.y)) / divisor

        if self.__descanso_poder <= 0:
            for i in range(self.__numero_de_projeteis):
                self.__poder.acao(self, tela, mapa, velx, vely, 0+10*i)
            self.__descanso_poder = self.__descanso_poder_max# + randrange(0, 50)
        else:
            self.__descanso_poder -= 1 * self.escala_tempo

    def sofreu_colisao_jogador(self, jogador, direcao, mapa):
        "Detecta colisao com jogador, return dano caso valido"
        ##### COLISAO ESQUERDA #####
        if not jogador.invisivel:
            if direcao == "esquerda":
                if jogador.velx <= 0:
                    jogador.velx = 0
                    jogador.aceleracao = 0
                    jogador.x = self.corpo.right + 1
            ##### COLISAO DIREITA #####
            elif direcao == "direita":
                if jogador.velx >= 0:
                    jogador.velx = 0
                    jogador.aceleracao = 0
                    jogador.x = self.corpo.left - jogador.largura
            ##### COLISAO BAIXO #####
            elif direcao == "baixo":
                jogador.vely = 0
                jogador.y = self.corpo.top - jogador.altura
            ##### COLISAO CIMA #####
            elif direcao == "cima":
                if jogador.vely < 0:
                    jogador.vely = 0
                    jogador.y = self.corpo.bottom
            return 0
        else:
            return 0

@instanciavel
class CoracaoRoxo(ParteDoRei):
    def __init__(self, x, y):
        self.__rei = 0
        altura = 25
        largura = 25
        dano_contato = 0
        cor = (255,0,255)
        limiteVel = 4
        self.__montado = False
        super().__init__("coracao", x, y, altura, largura, limiteVel, 0, dano_contato, "0", cor, 0)

    def montar(self, mapa):
        self.__montado = True
        for entidade in mapa.lista_de_entidades:
            if type(entidade) == ReiDasCores:
                self.__rei = entidade
                entidade.coracao = self

    def atualizar(self, tela, mapa, dimensoes_tela):
        if not self.__montado: self.montar(mapa)
        self.renderizar(tela, mapa)
        ##### ATUALIZACAO DO CORACAO #####
        self.x = self.__rei.x + 63
        self.y = self.__rei.y + 100
        self.corpo = pygame.Rect(self.x, self.y, self.largura,self.altura)

    def sofreu_colisao_jogador(self, jogador, direcao, mapa):
        "Determina que o jogador fique mais lento ao passar"
        if not jogador.invisivel:
            jogador.escala_tempo = 0.25
        return 0

    def sofreu_colisao_outros(self, entidade, direcao, mapa):
        pass


@instanciavel
class ReiDasCores(Entidade):
    def __init__(self, x, y):
        self.__cabeca = 0 #CabecaLaranja(x+50,y-50, self)
        self.__punho_esquerdo = 0 #PunhoVermelho(x-100,y+100, self, "esquerdo")
        self.__punho_direito = 0 #PunhoVermelho(x+200,y+100, self, "direito")
        self.__coracao = 0 #CoracaoRoxo(x+63,y+100, self)
        super().__init__("corpo", x, y, 300, 150, 0, 0, 0, "0", (0,0,255), 0, True)
        self.velx = 1
        self.__descanso_ate_prox_fase = 500

    @property
    def punho_esquerdo(self):
        return self.__punho_esquerdo

    @punho_esquerdo.setter
    def punho_esquerdo(self, punho_esquerdo):
        self.__punho_esquerdo = punho_esquerdo

    @property
    def punho_direito(self):
        return self.__punho_direito

    @punho_direito.setter
    def punho_direito(self, punho_direito):
        self.__punho_direito = punho_direito

    @property
    def cabeca(self):
        return self.__cabeca

    @cabeca.setter
    def cabeca(self, cabeca):
        self.__cabeca = cabeca

    @property
    def coracao(self):
        return self.__coracao

    @coracao.setter
    def coracao(self, coracao):
        self.__coracao = coracao


    def fase_0(self):
        self.__cabeca.descanso_poder_max = 100
        self.__cabeca.numero_de_projeteis = 5

    def atualizar(self, tela, mapa, dimensoes_tela):
        if self.__descanso_ate_prox_fase: self.__descanso_ate_prox_fase -= 1
        else:
            self.fase_0()
        self.mover(dimensoes_tela, mapa)
        self.renderizar(tela, mapa)

    def renderizar(self, tela, mapa):
        pygame.draw.rect(tela, self.cor,
                [self.corpo.x - mapa.campo_visivel.x, self.corpo.y - mapa.campo_visivel.y, self.corpo.w, self.corpo.h])

    def mover(self, dimensoesTela, mapa):
        ##### COLISOES #####
        obsCima, obsBaixo, obsDireita, obsEsquerda = self.checar_colisao(mapa.lista_de_entidades, [Bala, Coletavel, ParteDoRei])

        if obsEsquerda: obsEsquerda.sofreu_colisao_outros(self, "esquerda", mapa)
        if obsDireita: obsDireita.sofreu_colisao_outros(self, "direita", mapa)
        if obsCima: obsCima.sofreu_colisao_outros(self, "cima", mapa)
        if obsBaixo:
            obsBaixo.sofreu_colisao_outros(self, "baixo", mapa)

        ##### GRAVIDADE ######
        else:
            self.vely += gravidade * self.escala_tempo

        ##### ATUALIZACAO DAS POSICOES #####
        self.y += self.vely * self.escala_tempo
        self.x += self.velx * self.escala_tempo

        self.corpo = pygame.Rect(self.x, self.y, self.largura, self.altura)

    def sofreu_colisao_jogador(self, jogador, direcao, mapa):
        "Determina que o jogador fique mais lento ao passar"
        if not jogador.invisivel:
            jogador.escala_tempo = 0.25
        return 0

    def sofreu_colisao_outros(self, entidade, direcao, mapa):
        pass