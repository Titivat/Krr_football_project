import pygame
import sys
#--Init Pygame
pygame.init()

#setting
WINDOW_WIDTH = 900
WINDOW_HEIGHT = 600
FPS = 120
clock =  pygame.time.Clock()

COLOR_WHITE = (255,255,255)

#Game window
game_window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('First Game')

#--Sprite -- ##
class Player1( pygame.sprite.Sprite ):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10,80))
        self.image.fill( COLOR_WHITE )
        self.rect = self.image.get_rect()
        self.rect.left = 25
        self.rect.centery = WINDOW_HEIGHT / 2

class Player2( pygame.sprite.Sprite ):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10,80))
        self.image.fill( COLOR_WHITE )
        self.rect = self.image.get_rect()
        self.rect.right = WINDOW_WIDTH - 25
        self.rect.centery = WINDOW_HEIGHT / 2

#--Sprite Groups
all_sprites = pygame.sprite.Group()

player1 = Player1()
all_sprites.add( player1 )
player2 = Player2()
all_sprites.add( player2 )

#--Game loop--#
while True:
    #set framerate
    clock.tick( FPS )

    #process event
    for event in pygame.event.get():
        #close screen
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    #Update

    #Draw
    all_sprites.draw( game_window )
    #Flip
    pygame.display.flip()

pygame.quit()