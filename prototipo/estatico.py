from abc import ABC

class Estatico(ABC):
    def __init__(nome: str, posicao: tuple, tamanho: tuple):
        self.__nome = nome
        self.__posicao = posicao
        self.__tamanho = tamanho 

    def inicializacao():
        pass
    def atualizacao():
        pass