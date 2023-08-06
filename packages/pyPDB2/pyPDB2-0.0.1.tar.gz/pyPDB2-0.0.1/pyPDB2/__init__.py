import pygame
from pygame.locals import *
import pygame.freetype

red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
black = (0, 0, 0)
white = (255, 255, 255)


class ynBox:
    def __init__(self):
        self.length = 300
        self.width = 100
    
    def draw(self):
        pygame.init()

        yBut = pygame.Rect(40, 60, 100, 30)
        nBut = pygame.Rect(160, 60, 100, 30)

        font1 = pygame.font.SysFont("comicsansms", 20)
        font2 = pygame.font.SysFont("comicsansms", 25)
        
        loop = True

        self.disp = pygame.display.set_mode((self.length, self.width))

        pygame.display.set_caption("Dialogue Box")

        

        while loop == True:

            mouseClicked = False

            for event in pygame.event.get():
                if event.type == MOUSEBUTTONUP:
                    mouseClicked = True
                    (mX, mY) = event.pos
                    
                    
            pygame.display.update()
            self.disp.fill(black)

            pygame.draw.rect(self.disp, green, (yBut))
            pygame.draw.rect(self.disp, red, (nBut))

            sText = font1.render('Are you sure?', True, (white))
            self.disp.blit(sText, (80, 10))

            yText = font2.render('Yes', True, (black))
            nText = font2.render('No', True, (black))
            self.disp.blit(yText, (70, 55))
            self.disp.blit(nText, (190, 55))

            if mouseClicked and yBut.collidepoint(mX, mY):
                loop = False
                pygame.quit()
                return(1)

            elif mouseClicked and nBut.collidepoint(mX, mY):
                loop = False
                pygame.quit()
                return(0)

        
        





