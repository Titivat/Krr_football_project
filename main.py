import pygame, random
import sys
# --Init Pygame
pygame.init()

# setting
WINDOW_WIDTH = 900
WINDOW_HEIGHT = 600
FPS = 120
clock = pygame.time.Clock()

COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)

# Game window
game_window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('First Game')

#--Sprite -- ##


class Player1(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10, 80))
        self.image.fill(COLOR_WHITE)
        self.rect = self.image.get_rect()
        self.rect.left = 25
        self.rect.centery = WINDOW_HEIGHT / 2
        #self.top = self.rect.centery
        self.dy = 0

    # function that move the spriteq
    def update(self):
        self.dy = 0
        keystate = pygame.key.get_pressed()
        # go down
        if keystate[pygame.K_w]:
            self.dy = -3
        # go up
        if keystate[pygame.K_s]:
            self.dy = 3
        self.rect.y += self.dy

        # condition so that the sprite do not move out the screen
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > WINDOW_HEIGHT:
            self.rect.bottom = WINDOW_HEIGHT


class Player2(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10, 80))
        self.image.fill(COLOR_WHITE)
        self.rect = self.image.get_rect()
        self.rect.right = WINDOW_WIDTH - 25
        self.rect.centery = WINDOW_HEIGHT / 2

    # function that move the sprite
    def update(self):
        self.dy = 0
        keystate = pygame.key.get_pressed()
        # go down
        if keystate[pygame.K_UP]:
            self.dy = -3
        # go up
        if keystate[pygame.K_DOWN]:
            self.dy = 3
        self.rect.y += self.dy

        # condition so that the sprite do not move out the screen
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > WINDOW_HEIGHT:
            self.rect.bottom = WINDOW_HEIGHT

class Ball( pygame.sprite.Sprite ):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10, 10))
        self.image.fill(COLOR_WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = ( WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)
        self.dx = random.choice([-1, 1])
        self.dy = random.choice([-2, -1, 1, 2])

    def update( self ):
        self.rect.x += self.dx
        self.rect.y += self.dy
        # colusion
        if self.rect.top < 0:
            self.dy *= -1
        if self.rect.bottom > WINDOW_HEIGHT:
            self.dy *= -1

        #collision with player
        collion = pygame.sprite.spritecollideany( ball, all_sprites)
        if collion:
            if( collion == player1 ):
                self.rect.x -= self.dx
                self.dx *= -1
                self.dx += random.choice([0,1])
            if( collion == player2 ):
                self.rect.x -= self.dx
                self.dx *= -1
                self.dx += random.choice([0,1])
            #extra condition to make it fun
            if self.dy == 0:
                self.dy += random.choice([-1,1])
            if self.dy <= 0:
                self.dy += random.choice([-1,0,1])
            if self.dy >= 0:
                self.dy += random.choice([-1,0,1])

class Score():
    def __init__(self):
        self.score1 = 0
        self.score2 = 0
        self.score_font = pygame.font.SysFont(None, 100)

    def update( self ):
        #if a player scores
        if ball.rect.right < 0:
            self.score2 += 1
            ball.__init__()
        if ball.rect.left > WINDOW_WIDTH:
            self.score1 += 1
            ball.__init__()
        self.player1_score = self.score_font.render(str(self.score1), True, COLOR_WHITE, COLOR_BLACK)
        self.player2_score = self.score_font.render(str(self.score2), True, COLOR_WHITE, COLOR_BLACK)

    def draw(self):
        game_window.blit( self.player1_score, (WINDOW_WIDTH / 4, WINDOW_HEIGHT / 8))
        game_window.blit( self.player2_score, (WINDOW_WIDTH * 3 / 4, WINDOW_HEIGHT / 8))

# --Sprite Groups
all_sprites = pygame.sprite.Group()
ball_sprite = pygame.sprite.GroupSingle()

#player added
player1 = Player1()
all_sprites.add(player1)
player2 = Player2()
all_sprites.add(player2)

#ball added
ball = Ball()
ball_sprite.add( ball )

#score
score = Score()
score.__init__()

#--Game loop--#
while True:
    # set framerate
    clock.tick(FPS)

    # process event
    for event in pygame.event.get():
        # close screen
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Update the movement of the sprite
    all_sprites.update()
    ball_sprite.update()
    score.update()

    # clean the movment of the sprite
    game_window.fill(COLOR_BLACK)
    #Draw
    #Field
    pygame.draw.line( game_window, COLOR_WHITE, (WINDOW_WIDTH / 2, 0), (WINDOW_WIDTH/2, WINDOW_HEIGHT))
    pygame.draw.circle( game_window, COLOR_WHITE, (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2), 80, 1)
    #score
    score.draw()
    # Draw the  sprite on the screnn
    all_sprites.draw(game_window)
    ball_sprite.draw(game_window)

    # Flip
    pygame.display.flip()

pygame.quit()
