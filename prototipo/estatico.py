import abc from ABC

def __init__(nome: str, x: int, y:int, tamanho: int):
    self.__nome = nome
    self.__x = x
    self.__y = y
    self.__tamanho = tamanho 

@property
def nome (self):
    return self.__nome 

@nome.setter
def nome (self, nome):
     self.__nome = nome

@property
def posicao (self):
    return self.__posicao 
 
@posicao.setter
def nome (self, posicao):
     self.__posicao = posicao

def inicializacao():
    pass

def Atualizacao():
    pass