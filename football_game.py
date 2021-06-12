import pygame
import random
import sys

pygame.init()

# setting
WINDOW_WIDTH = 1500
WINDOW_HEIGHT = 800
FPS = 120
clock = pygame.time.Clock()

COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_RED = (255, 0, 0)
COLOR_GREEN = (0,255,0)
COLOR_BLUE = (0, 0, 255)

BACKGROUND = pygame.image.load("football_field")
BACKGROUND = pygame.transform.scale(BACKGROUND, (WINDOW_WIDTH, WINDOW_HEIGHT))

# Game window
game_window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('First Game')

class Player1(pygame.sprite.Sprite):
    def __init__(self, name):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((25, 60))
        self.image.fill(COLOR_RED)
        self.rect = self.image.get_rect()
        self.rect.left = 37
        self.rect.centery = WINDOW_HEIGHT / 2
        self.name = name
        self.dx = 0
        self.dy = 0

    def update(self):
        self.dy = 0
        self.dx = 0

        keystate = pygame.key.get_pressed()

        if keystate[pygame.K_w]:
            self.dy = -2

        if keystate[pygame.K_s]:
            self.dy = 2

        if keystate[pygame.K_a]:
            self.dx = -2

        if keystate[pygame.K_d]:
            self.dx = 2

        self.rect.x += self.dx
        self.rect.y += self.dy

        collion = pygame.sprite.spritecollideany(goaly, ball_sprite)
        if collion and not ball.shoot:
            if(type(collion) == Ball):
                ball.shoot = False
                ball.rect.x = self.rect.x + 20
                ball.rect.y = self.rect.y + 55

                if keystate[pygame.K_f]:
                    ball.shoot = True
                    ball.rect.x -= ball.dx
                    ball.dx *= -1
                    ball.dy += random.choice([-1, 1])
                    ball.dx += random.choice([1, 2])

        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > WINDOW_HEIGHT:
            self.rect.bottom = WINDOW_HEIGHT

class Ball(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((15, 15))
        self.image.fill(COLOR_WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)
        self.dx = 0
        self.dy = 0
        self.shoot = False

    def update(self):
        if self.shoot:
            self.rect.x += self.dx
            self.rect.y += self.dy
        else:
            self.dx = 0
            self.dy = 0

        if self.rect.top < 0:
            self.dy = 1

        if self.rect.bottom > WINDOW_HEIGHT:
            self.dy = -1

        # collion = pygame.sprite.spritecollideany(ball, all_sprites)
        # if collion:
        #     if(type(collion) == Player1):
        #         self.dx = 3

        # self.rect.x += self.dx


#main
all_sprites = pygame.sprite.Group()
ball_sprite = pygame.sprite.GroupSingle()

goaly = Player1("playerA")
all_sprites.add( goaly )

ball = Ball()
ball_sprite.add( ball )

while True:
    # set framerate
    clock.tick(FPS)

    # process event
    for event in pygame.event.get():
        # close screen
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            print( pos )

    # Update the movement of the sprite
    all_sprites.update()
    ball_sprite.update()

    # clean the movment of the sprite
    # game_window.fill(COLOR_BLACK)
    game_window.blit(BACKGROUND, (0, 0))
    # Draw
    # Draw the  sprite on the screnn
    all_sprites.draw(game_window)
    ball_sprite.draw(game_window)
    # Flip
    pygame.display.flip()