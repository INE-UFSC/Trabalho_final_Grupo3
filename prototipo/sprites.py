import pygame
import json

class SpriteSheet():
    def __init__(self, arquivo):
        self.__imagem = arquivo+".png"
        self.__sprite_sheet = pygame.image.load(self.__imagem).convert_alpha()
        self.__arquivo_dados = arquivo+".json"
        self.__dados = {}
        with open(self.__arquivo_dados) as f:
            self.__dados = json.load(f)

    def imprimir(self, nome, posx, posy, tela, orientacao, velx):
        move = ""
        if velx: move = "move"
        face = ""
        if self.__imagem == "guri.png":
            if orientacao == 1: face = "r"
            else: face = "l"
        sprite = self.__dados["frames"][nome+move+face+".png"]["frame"]
        x, y, w, h = sprite["x"], sprite["y"], sprite["w"], sprite["h"]
        tela.blit(self.__sprite_sheet, (posx, posy), (x, y, w, h))