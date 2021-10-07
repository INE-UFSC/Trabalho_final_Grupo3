import pygame
import json

class Sprite():
    def __init__(self, arquivo):
        from DAOjogo import DAOJogo
        imagem = DAOJogo.carregar_sprite(arquivo)
        self.__imagem = "sprites/"+arquivo+".png"
        self.__sprite_sheet = imagem["sprite_sheet"]
        self.__dados = imagem["dados"]

    @property
    def imagem(self):
        return self.__imagem

    def imprimir(self, tela, nome, posx, posy, orientacao = None, velx = None, vely = None, frame = 0, largura = None, altura = None):
        if orientacao == 1: nome = nome + "_right"
        elif orientacao == -1: nome = nome + "_left"
        if velx: nome = nome + "_walk"
        if self.__imagem != "sprites/sprites.png": nome = nome + "_" + str(frame)
        self.carregar_sprite(nome, posx, posy, largura, altura, tela)

    def carregar_sprite(self, nome, posx, posy, width, height, tela):
        sprite = self.__dados[nome]
        x, y, w, h = sprite["x"], sprite["y"], sprite["w"], sprite["h"]
        if nome == "chao":
            ciclos_completos = int(width/w)
            extra = width - ciclos_completos * w
            for i in range(ciclos_completos):
                tela.blit(self.__sprite_sheet, (posx+i*w, posy), (x, y, w, h))
            tela.blit(self.__sprite_sheet, (posx+ciclos_completos*w, posy), (x, y, extra, h))
        else:
            if width: w = width
            if height: h = height
            tela.blit(self.__sprite_sheet, (posx, posy), (x, y, w, h))

class SpriteJogador():
    def __init__(self,cor_borda,cor_corpo):
        from DAOjogo import DAOJogo
        self.__pasta_dados = DAOJogo.pasta_assets
        self.montar_sprite(cor_borda,cor_corpo)
        with open(self.__pasta_dados + "rabisco.json") as f:
            self.__dados = json.load(f)
    
    def montar_sprite(self,cor_borda,cor_corpo):

        mask_rosto = pygame.image.load(self.__pasta_dados + "mask_rosto.png").convert()
        mask_rosto.set_colorkey((0,255,0))

        mask_contorno = pygame.image.load(self.__pasta_dados + "mask_contorno.png").convert()
        mask_contorno.set_colorkey((0,255,0))

        mask_corpo = pygame.image.load(self.__pasta_dados + "mask_corpo.png").convert()
        mask_corpo.set_colorkey((0,255,0))

        carimbo = pygame.Surface((90,120))
        carimbo.set_colorkey((0,0,0))

        sprites = pygame.Surface((90,120))
        sprites.set_colorkey((0,0,0))

        carimbo.fill((1,1,1))
        carimbo.blit(mask_rosto,(0,0))
        sprites.blit(carimbo, (0,0))

        carimbo.fill(cor_borda)
        carimbo.blit(mask_contorno,(0,0))
        sprites.blit(carimbo, (0,0))

        carimbo.fill(cor_corpo)
        carimbo.blit(mask_corpo,(0,0))
        sprites.blit(carimbo, (0,0))

        sprites = pygame.transform.scale(sprites, (270,360))

        self.__sprite_sheet = sprites

    @property
    def imagem(self):
        return self.__imagem

    def imprimir(self, tela, nome, posx, posy, orientacao = None, velx = None, vely = None, frame = 0, largura = None, altura = None):
        if orientacao == 1: nome = nome + "_right"
        elif orientacao == -1: nome = nome + "_left"
        if velx: nome = nome + "_walk"
        nome = nome + "_" + str(frame)
        self.carregar_sprite(nome, posx, posy, largura, altura, tela)

    def carregar_sprite(self, nome, posx, posy, width, height, tela):
        sprite = self.__dados[nome]
        x, y, w, h = sprite["x"], sprite["y"], sprite["w"], sprite["h"]
        if nome == "chao":
            ciclos_completos = int(width/w)
            extra = width - ciclos_completos * w
            for i in range(ciclos_completos):
                tela.blit(self.__sprite_sheet, (posx+i*w, posy), (x, y, w, h))
            tela.blit(self.__sprite_sheet, (posx+ciclos_completos*w, posy), (x, y, extra, h))
        else:
            if width: w = width
            if height: h = height
            tela.blit(self.__sprite_sheet, (posx, posy), (x, y, w, h))
