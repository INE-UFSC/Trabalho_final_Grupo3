import pygame
import math
import random

pygame.init()
pygame.display.set_caption("cumchalice")
window = pygame.display.set_mode((400,400))
clock = pygame.time.Clock()
radius = 0
color = 0

def colorwheel(value):
    return max(0,min(2-abs(120-value%360)/60,1))
    
class Player():
    def __init__(self):
        self.x = 30
        self.y = 30
        self.v = 1.5
        self.w = 20
        self.h = 20
        self.d = [0,0]
    def render(self,surface):
        pygame.draw.rect(surface,(150,150,150),[self.x,self.y,self.w,self.h])
    def xvel(self,x):
        self.d[0] = x
    def yvel(self,y):
        self.d[1] = y
    def move(self):
        self.x += self.d[0]*self.v
        self.y += self.d[1]*self.v
player = Player()
while True:
    color += 1
    radius += 1
    r = 255 * colorwheel(color-120)
    g = 255 * colorwheel(color)
    b = 255 * colorwheel(color+120)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                player.yvel(1)
            elif event.key == pygame.K_UP:
                player.yvel(-1)
            elif event.key == pygame.K_LEFT:
                player.xvel(-1)
            elif event.key == pygame.K_RIGHT:
                player.xvel(1)
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN or event.key == pygame.K_UP:
                player.yvel(0)
            elif event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player.xvel(0)
    player.move()
    window.fill([255-r,255-g,255-b])
    pygame.draw.ellipse(window,[r,g,b],(80-25*math.sin((radius+45)/30),80-25*math.sin((radius+45)/30),240+50*math.sin((radius+45)/30),240+50*math.sin((radius+45)/30)),10)
    pygame.draw.circle(window,[r,g,b],(200,200),80 + 10 * math.sin(radius/30))
    player.render(window)
    pygame.display.update()
    clock.tick(60)
    
quit