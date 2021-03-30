class Jogador: 
    def __init__(self, nome: str, posicao: tuple(), velocidae: int):
        self.__nome = nome 
        self.__posicao = posicao 
        self.__velocidade = velocidae

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
    def posicao (self, posicao):
        self.__posicao = posicao

    @property
    def velocidae (self):
        return self.__velocidade
    
    @velocidae.setter
    def nome (self, velocidae):
        self.__velocidade = velocidae
