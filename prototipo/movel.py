from estatico import Estatico

class Movel(Estatico):

    def __init__(self, nome: str, x: int, y: int, tamanho: int, limiteVel: int):
        super().__init__(nome, x, y, tamanho)
        self.__velx = 0
        self.__vely = 0
        self.__limiteVel = limiteVel

    @property
    def velx(self):
        return self.__velx

    @velx.setter
    def velx(self, velx):
        self.__velx = velx

    @property
    def vely(self):
        return self.__vely

    @vely.setter
    def vely(self, vely):
        self.__vely = vely

    @property
    def limiteVel(self):
        return self.__limiteVel

    @limiteVel.setter
    def limiteVel(self, limiteVel):
        self.__limiteVel = limiteVel

    def Mover(self):
        pass