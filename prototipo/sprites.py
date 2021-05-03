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

    def imprimir(self, nome, posx, posy, tela, orientacao):
        char = ""
        if self.__imagem == "andando.png":
            if orientacao == 1: char = "r"
            else: char = "l"
        sprite = self.__dados["frames"][nome+char+".png"]["frame"]
        x, y, w, h = sprite["x"], sprite["y"], sprite["w"], sprite["h"]
        tela.blit(self.__sprite_sheet, (posx, posy), (x, y, w, h))