import pygame 

#mudar no UML- Sem parametro
class ObstaculoGenerico: 
    def __init__(self, tipo):
        self.__tipo = ''
    
    @property
    def tipo(self):
        return self.__tipo

