import pygame
import json

class Sprite():
    def __init__(self, arquivo):
        arquivo = "sprites/"+arquivo
        self.__imagem = arquivo+".png"
        self.__sprite_sheet = pygame.image.load(self.__imagem).convert_alpha()
        self.__arquivo_dados = arquivo+".json"
        self.__dados = {}
        with open(self.__arquivo_dados) as f:
            # print(self.__arquivo_dados)
            # print(f)
            self.__dados = json.load(f)

    @property
    def imagem(self):
        return self.__imagem

    def imprimir(self, tela, nome, posx, posy, orientacao, velx, vely, frame):
        if orientacao == 1: nome = nome + "_right"
        elif orientacao == -1: nome = nome + "_left"
        #if vely != 0 and nome != "rabisco": nome = nome + "_jump"
        if velx != 0: nome = nome + "_walk"
        if self.__imagem != "sprites/sprites.png": nome = nome + "_" + str(frame)
        self.carregar_sprite(nome, posx, posy, tela)

    def carregar_sprite(self, nome, posx, posy, tela):
        sprite = self.__dados[nome]
        x, y, w, h = sprite["x"], sprite["y"], sprite["w"], sprite["h"]
        tela.blit(self.__sprite_sheet, (posx, posy), (x, y, w, h))