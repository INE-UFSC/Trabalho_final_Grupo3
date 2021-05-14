from entidades import *
from inimigos import *
from poderes import *
from obstaculos import *

@instanciavel
class Gota(Coletavel):
    def __init__(self, x, y, rei):
        largura = 20
        altura = 20
        num = 1
        self.__rei = rei
        super().__init__("gota"+str(num), x, y, "0", (0, 0, 0), largura, altura)
    
    def coleta(self, jogador, mapa):
        jogador.ganha_vida()
        self.__rei.jogador_pega_gota()
        mapa.escala_tempo = 1
        self.auto_destruir(mapa)

class ParteDoRei(Entidade):
    def __init__(self, nome: str, x: int, y: int, altura: int, largura: int, limiteVel: int, vida: int, dano_contato: int, imagem: str, cor, frames: int):
        super().__init__(nome, x, y, altura, largura, limiteVel, vida, dano_contato, imagem, cor, frames, True)
        self.__montado = False
        self.__fase = 0
        self.__rei = 0

    @property
    def montado(self):
        return self.__montado

    @property
    def fase(self):
        return self.__fase

    @property
    def rei(self):
        return self.__rei

    @rei.setter
    def rei(self, rei):
        self.__rei = rei

    @montado.setter
    def montado(self, montado):
        self.__montado = montado

    def passar_fase(self):
        self.__fase += 1

    def montar(self, mapa):
        for entidade in mapa.lista_de_entidades:
            if type(entidade) == ReiDasCores:
                self.__montado = True
                self.__rei = entidade
                if type(self) == CabecaLaranja:
                    entidade.cabeca = self
                elif type(self) == CoracaoRoxo:
                    entidade.coracao = self


@instanciavel
class PunhoVermelho(ParteDoRei):
    def __init__(self, x, y, lado, primeiro_tiro):
        self.__centro_x = x
        self.__centro_y = y
        self.__lado = lado
        altura = 60
        largura = 60
        dano_contato = 1
        cor = (255,0,0)
        limiteVel = 10
        self.__espera = 0
        self.__recarga = 300
        self.__descanso_tiro = primeiro_tiro
        self.__atirando = False
        self.__atirou = False
        self.__vel_projetil = 10
        self.__quebrado = False
        super().__init__("punho", x, y, altura, largura, limiteVel, 0, dano_contato, "punho", cor, 0)
    
    @property
    def recarga(self):
        return self.__recarga
    
    @recarga.setter
    def recarga(self, recarga):
        self.__recarga = recarga

    @property
    def quebrado(self):
        return self.__quebrado

    def renderizar(self, tela, mapa):
        "renderiza na tela na posicao correta"

        if renderizar_hitbox:
            pygame.draw.rect(tela, (255, 0, 0), [self.corpo.x - mapa.campo_visivel.x, self.corpo.y - mapa.campo_visivel.y,
                                                   self.corpo.w, self.corpo.h])
        if renderizar_sprite:
            if self.velx > 0: face = 1
            elif self.velx < 0: face = -1
            else:
                if self.__lado == "esquerdo": face = -1
                else: face = 1
            self.sprite.imprimir(tela, "punho", self.x - mapa.campo_visivel.x, self.y - mapa.campo_visivel.y, face, 0, 0,
                                        1 * (self.__quebrado))

    def montar(self, mapa):
        for entidade in mapa.lista_de_entidades:
            if type(entidade) == ReiDasCores:
                self.montado = True
                self.rei = entidade
                if self.__lado == "esquerdo":
                    entidade.punho_esquerdo = self
                else:
                    entidade.punho_direito = self


    def atualizar(self, tela, mapa, dimensoes_tela):
        atira = 0 #define se o boss vai laçar a mão
        if not self.__atirando: #se não esta lançando a posição é colada ao boss e conta para poder atirar
            self.__descanso_tiro -= 1
            if self.__descanso_tiro == 0:
                self.__atirou = False
                atira = 1
                self.__descanso_tiro = self.__recarga
            self.x = self.__centro_x
            self.y = self.__centro_y
            self.vely = 0
            self.velx = 0
        
        self.lancar(mapa.jogador, mapa, atira) # lançar é o mover da mão
        if not self.montado: self.montar(mapa)
        ##### ATUALIZACAO DO CORACAO #####
        if self.__lado == "direito":
            self.__centro_x = self.rei.x + 200
            self.__centro_y = self.rei.y + 100
        else:
            self.__centro_x = self.rei.x - 100
            self.__centro_y = self.rei.y + 100
        self.corpo = pygame.Rect(self.x, self.y, self.largura, self.altura)

        self.renderizar(tela, mapa)

    def lancar(self, jogador, mapa, atira):
        velx_buff = self.velx
        obsCima, obsBaixo, obsDireita, obsEsquerda = self.checar_colisao(mapa.lista_de_entidades, [BolaFogo ,Bala, Coletavel, ParteDoRei])
        if obsEsquerda: obsEsquerda.sofreu_colisao_outros(self, "esquerda", mapa)
        if obsDireita: obsDireita.sofreu_colisao_outros(self, "direita", mapa)
        if obsCima: obsCima.sofreu_colisao_outros(self, "cima", mapa)
        if obsBaixo:
            obsBaixo.sofreu_colisao_outros(self, "baixo", mapa)
            self.velx = 0
        ##### VOLTANDO AO CORPO #####
        if velx_buff and not self.velx and self.__atirando: # se acabou de de tocar no chão começa o tempo de espera paravoltar ao corpo
            self.vely = 0
            self.__espera = 120
            self.__atirou = True # variavel para deixar a função de voltar ao corpo rodar só depois de ter atirado
        if self.__espera == 0 and self.__atirou:# função de voltar ao corpo
            dstancia = (((self.__centro_y) - (self.y)) ** 2 + (
                self.__centro_x - self.x) ** 2) ** (1 / 2) # distancia entre a mão e sua posiçaõ no corpo
            divisor = max(dstancia / self.__vel_projetil,0.001)

            self.velx = ((self.__centro_x - self.x)) / divisor
            self.vely = ((self.__centro_y) - (self.y)) / divisor
            if dstancia <= 8: #checagem para ver se chegou no corpo
                self.__atirando = False
        else:
            self.__espera -= 1 #contagem para a mão ficar um tempinho parada
        
        if abs(self.__centro_x - self.corpo.centerx) >= 700 or abs((self.__centro_y) - (self.y)) >= 700: #se a mão nunca chegar no chão começa a voltar
            self.__espera = 0
            self.__atirou = True # variavel para deixar a função de voltar ao corpo rodar só depois de ter atirado

        #### FUNÇÂO PARA ATIRAR ####
        if atira == 1:
            self.__atirando = True 
            dstancia = (((jogador.corpo.centery) - (self.corpo.centery)) ** 2 + (
                    jogador.corpo.centerx - self.corpo.centerx) ** 2) ** (1 / 2) #distancia entre a mão e o jogador
            divisor = max(dstancia / self.__vel_projetil,0.001)

            self.velx = ((jogador.corpo.centerx - self.corpo.centerx)) / divisor
            self.vely = ((jogador.corpo.centery) - (self.corpo.centery)) / divisor
        
        #### Atualiza a posição da mão ####
        self.x += self.velx
        self.y += self.vely
        

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
                self.__quebrado = True #Toma dano se o jogador pina nela
                return 0
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
        #self.__rei = 0
        self.__vel_projetil = 3
        self.__descanso_poder_max = 125
        self.__descanso_poder = randrange(0, 25)
        self.__poder = Projetil()
        self.__quebrado = False
        altura = 59
        largura = 56
        dano_contato = 1
        cor = (255,128,0)
        limiteVel = 10
        super().__init__("cabeca", x, y, altura, largura, limiteVel, 0, dano_contato, "cabeca", cor, 0)


    @property
    def quebrado(self):
        return self.__quebrado

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

    def renderizar(self, tela, mapa):
        "renderiza na tela na posicao correta"

        if renderizar_hitbox:
            pygame.draw.rect(tela, (255, 128, 0), [self.corpo.x - mapa.campo_visivel.x, self.corpo.y - mapa.campo_visivel.y,
                                                   self.corpo.w, self.corpo.h])
        if renderizar_sprite:
            self.sprite.imprimir(tela, "cabeca", self.x - mapa.campo_visivel.x, self.y - mapa.campo_visivel.y, self.face, 1 * (self.__quebrado), 0,
                                        int((self.escala_tempo != 0)*mapa.ciclo/6) % 8)

    def atualizar(self, tela, mapa, dimensoes_tela):

        if not self.montado: self.montar(mapa)

        if mapa.jogador.x >= self.x:
            self.face = 1
        else:
            self.face = -1

        self.renderizar(tela, mapa)

        ##### ATUALIZACAO DA CABECA #####
        self.x = self.rei.x + 45
        self.y = self.rei.y - 59
        self.corpo = pygame.Rect(self.x, self.y, self.largura, self.altura)

        ##### FAZ ELE ATIRAR FOGO #####
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

        ##### FALA PRA ELE QUANDO ATIRAR FOGO #####
        if self.fase == 1:
            numero_de_projeteis = 0
            self.descanso_poder_max = 150
        elif self.fase == 2:
            numero_de_projeteis = 5
            self.descanso_poder_max = 150
        else:
            numero_de_projeteis = 2
            self.descanso_poder_max = 150
        if self.__descanso_poder <= 0:
            for i in range(numero_de_projeteis):
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
                    if jogador.velx <= -8: #cabeça toma dano se for batida via dash
                        self.__quebrado = True
                    jogador.velx = 0
                    jogador.aceleracao = 0
                    jogador.x = self.corpo.right + 1
            ##### COLISAO DIREITA #####
            elif direcao == "direita":
                if jogador.velx >= 0:
                    if jogador.velx >= 8: #cabeça toma dano se for batida via dash
                        self.__quebrado = True
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
        #self.__rei = 0
        altura = 29
        largura = 29
        dano_contato = 0
        cor = (255,0,255)
        limiteVel = 4
        self.__tempo_parado = 500 #contador de tempo parado
        super().__init__("coracao", x, y, altura, largura, limiteVel, 0, dano_contato, "coracao", cor, 0)

    def parar_o_tempo(self, jogador):
        if self.__tempo_parado < 0: self.__tempo_parado -= 1
        if self.__tempo_parado:
            jogador.congelar()
        else:
            jogador.descongelar()

    def renderizar(self, tela, mapa):
        "renderiza na tela na posicao correta"

        if renderizar_hitbox:
            pygame.draw.rect(tela, self.cor,
                             [self.corpo.x - mapa.campo_visivel.x, self.corpo.y - mapa.campo_visivel.y,
                              self.corpo.w, self.corpo.h])
        if renderizar_sprite:
            self.sprite.imprimir(tela, "coracao", self.x - mapa.campo_visivel.x, self.y - mapa.campo_visivel.y,
                                 self.face, 0, 0, 0)

    def atualizar(self, tela, mapa, dimensoes_tela):
        if not self.montado: self.montar(mapa)
        if self.fase == 4:
            self.parar_o_tempo(mapa.jogador)
        self.renderizar(tela, mapa)
        ##### ATUALIZACAO DO CORACAO #####
        self.x = self.rei.x + 61
        self.y = self.rei.y + 100
        self.corpo = pygame.Rect(self.x, self.y, self.largura,self.altura)

    def sofreu_colisao_jogador(self, jogador, direcao, mapa):
        "Determina que o jogador fique mais lento ao passar"
        if not jogador.invisivel:
            if self.__tempo_parado:
                jogador.escala_tempo = 0
            else:
                jogador.escala_tempo = 0.25
        return 0

    def sofreu_colisao_outros(self, entidade, direcao, mapa):
        pass


@instanciavel
class ReiDasCores(Entidade):
    def __init__(self, x, y):
        ##### PARTES DO CORPO #####
        self.__cabeca = 0
        self.__punho_esquerdo = 0
        self.__punho_direito = 0
        self.__coracao = 0
        super().__init__("corpo_das_cores", x, y, 300, 150, 0, 0, 0, "corpo_das_cores", (0,0,255),9, True)
        self.velx = 1

        ##### ATRIBUTOS REFERENTES A FASE DA LUTA #####
        self.__descanso_ate_prox_fase = 500
        self.__fase = 0 #0, 1-Vermelho, 2-Laranja, 3-Azul, 4-Roxo
        self.__entidades_da_fase = []
        self.__vida_gelatinosa = 15
        self.__cristais = 3
        self.__enjoo = 15

        ##### ATRIBUTOS DE POSICIONAMENTO #####
        self.__posicao_inicial = x
        self.__posicao_final = x + 500

    @property
    def fase(self):
        return self.__fase

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

    def toma_dano_de_fogo(self):
        self.__vida_gelatinosa -= 1


    def fase_1(self):
        self.__entidades_da_fase = [TintaVermelha(400, 450),
                                    Chao("chao", 200, 200, 400),
                                    Chao("chao", 300, 200, 400),
                                    Chao("chao", 400, 200, 400)]

    def fase_2(self):
        self.__entidades_da_fase = [TintaLaranja(400,450)
                                    ]

    def fase_3(self):
        self.__entidades_da_fase = [Gota(600,450,self)]

    def fase_4(self):
        self.__entidades_da_fase = []

    def passar_fase(self, mapa):
        ##### INCREMENTA A FASE #####
        self.__fase += 1
        self.__cabeca.passar_fase()
        self.__coracao.passar_fase()
        self.__punho_esquerdo.passar_fase()
        self.__punho_direito.passar_fase()

        ##### LIMPA ENTIDADES DA FASE ANTERIOR #####
        for entidade in self.__entidades_da_fase:
            if entidade in mapa.lista_de_entidades:
                mapa.lista_de_entidades.remove(entidade)

        if self.__fase == 1: self.fase_1()
        if self.__fase == 2: self.fase_2()
        if self.__fase == 3: self.fase_3()
        if self.__fase == 4: self.fase_4()
        for entidade in self.__entidades_da_fase:

        ##### CRIA INIMIGOS DA NOVA FASE #####
            mapa.lista_de_entidades.append(entidade)
    
    def jogador_pega_gota(self):
        if self.__cristais > 0:
            self.__cristais -= 1
        else:
            pass # AQUI PASSA PRA FASE 4

    def atualizar(self, tela, mapa, dimensoes_tela):
        ##### PASSA A FASE APOS CERTO TEMPO (PROVISORIO) #####
        if self.__enjoo: self.__enjoo -= 1 #Da 25 frames pro jogo carregar tudo
        else:
            print(self.__fase)
            if self.__fase == 0:
                if self.punho_direito.quebrado and self.punho_esquerdo.quebrado:
                    self.passar_fase(mapa)
            if self.__fase == 1:
                if self.__cabeca.quebrado:
                    self.passar_fase(mapa)
            if self.__fase == 2:
                if self.__vida_gelatinosa <= 0:
                    self.passar_fase(mapa)
        # if self.__descanso_ate_prox_fase:
        #     self.__descanso_ate_prox_fase = self.__descanso_ate_prox_fase-1
        # else:
        #     self.passar_fase(mapa)
        #     self.__descanso_ate_prox_fase = 500

        ##### COISA BASICA #####
        self.mover(dimensoes_tela, mapa)
        self.renderizar(tela, mapa)

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

        if self.x > self.__posicao_final  or self.x < self.__posicao_inicial:
            self.velx = -self.velx

        self.corpo = pygame.Rect(self.x, self.y, self.largura, self.altura)

    def sofreu_colisao_jogador(self, jogador, direcao, mapa):
        "Determina que o jogador fique mais lento ao passar"
        if not jogador.invisivel:
            jogador.escala_tempo = 0.25
        return 0

    def sofreu_colisao_outros(self, entidade, direcao, mapa):
        pass