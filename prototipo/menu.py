class Menu:
    def __init__(self, tela):
        self.__tela = tela
    
    @property
    def tela(self):
        return self.__tela
    
    @tela.setter
    def tela (self, tela):
        self.__tela = tela
    
    def trocar_tela():
        pass
