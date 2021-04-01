class Estatico():

    def __init__(self, nome: str, x:int, y:int, tamanho: int):
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
    def x(self):
        return self.__x
     
    @x.setter
    def x(self, x):
         self.__x = x

    @property
    def y(self):
        return self.__y

    @y.setter
    def y(self, y):
        self.__y = y

    def inicializacao(self):
        pass

    def Atualizacao(self):
        pass
