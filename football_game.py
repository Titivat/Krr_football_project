import pygame
import random
import sys
import math
from pyswip import Prolog, Atom, Functor

prolog = Prolog()
prolog.consult('mi.pl')

pygame.init()

# setting
WINDOW_WIDTH = 1500
WINDOW_HEIGHT = 800
FPS = 60
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
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((25, 60))
        self.image.fill(COLOR_RED)
        self.rect = self.image.get_rect()
        self.rect.left = 37
        self.rect.centery = WINDOW_HEIGHT / 2
        self.haveBall = False
        self.isFollow = False
        self.name = None
        self.goalPositionX = 1467
        self.goalPositionY = 386
        self.dx = 0
        self.dy = 0

    def setName(self, name ):
        self.name = name 

    def shootPositionY(self):
        #hypotenuse = math.sqrt((GOAL_POSITION_X-self.rect.x) ** 2 + (GOAL_POSITION_Y-self.rect.y) ** 2)
        dx = (self.goalPositionX-self.rect.x) * 0.01
        dy = (self.goalPositionY-self.rect.y) * 0.01
        return dx,dy

    def tackle(self, obj):
        pass

    def follow(self, obj):
        pass

    def backward(self):
        pass

    def shoot(self):
        pass

    def forward(self):
        pass

    def update(self):
        if self.dx > 2:
            self.dx = 1
        if self.dy > 2:
            self.dy = 1
        
        self.dx = 0
        self.dy = 0

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

        collion = pygame.sprite.spritecollideany(self, ball_sprite)
        if collion and not ball.shoot:
            if(type(collion) == Ball):
                self.haveBall = True
                ball.shoot = False
                ball.rect.x = self.rect.x + 20
                ball.rect.y = self.rect.y + 55

                if keystate[pygame.K_f]:
                    self.haveBall = False
                    ball.shoot = True
                    ball.rect.x -= ball.dx
                    ball.dx *= -1
                    dx,dy = self.shootPositionY()
                    ball.dy += dy
                    ball.dx += dx

        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > WINDOW_HEIGHT:
            self.rect.bottom = WINDOW_HEIGHT

    def setPosition(self, left, center):
        self.rect.left = left
        self.rect.centery = center
class Bot1(Player1):
    def __init__(self):
        super().__init__()
        self.tempDy = 0
        self.tempDx = 0

    def update(self):
        if self.dx > 1:
            self.dx = 0.5
        if self.dy > 1:
            self.dy = 0.5

        self.dx = 0
        self.dy = 0

        collion = pygame.sprite.spritecollideany(self, ball_sprite)
        if collion and not ball.shoot:
            if(type(collion) == Ball):
                self.haveBall = True
                ball.shoot = False
                ball.rect.x = self.rect.x + 20
                ball.rect.y = self.rect.y + 55

        self.dx = self.tempDx
        self.dy = self.tempDy

        self.rect.x += self.dx
        self.rect.y += self.dy

    def follow(self, obj):
        self.isFollow = True
        dx = (obj.rect.x-self.rect.x) * 0.01
        dy = (obj.rect.y-self.rect.y) * 0.01
        self.dx -= -1
        if self.dy > 1:
            self.dy = 0.5
        if self.dx > 1:
            self.dx = 0.5

        self.dy = dy 
        self.dx = dx 
        self.tempDy = self.dy % 1
        self.tempDx = self.dx % 1
        print(self.tempDy, self.tempDx)
        #print( self.dx, self.dy)

    def backward(self):
        self.dx -= 1

    def shoot(self):
        print('UI shoot')
        self.haveBall = False
        ball.shoot = True
        ball.rect.x -= ball.dx
        ball.dx *= -1
        dx,dy = self.shootPositionY()
        ball.dy += dy
        ball.dx += dx

class Player2(Bot1):
    def __init__(self):
        super().__init__() 
        self.image.fill(COLOR_BLUE)

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
    
    def follow(self, obj):
        pass

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

field_object = {}
goaly = Player1()
player1Number = 1
field_object['playerA'+str(player1Number)] = goaly
all_sprites.add( goaly )

player2 = Player2()
player2.setPosition( WINDOW_WIDTH - 65, WINDOW_HEIGHT / 2)
field_object['playerB'+str(player1Number)] = goaly
all_sprites.add( player2 )

player1Number += 1

position = 150
for _ in range(2):
    bot1 = Bot1()
    bot1.setPosition( 300, position)
    all_sprites.add( bot1 )

    bot2 = Player2()
    bot2.setPosition( 1170, position)
    all_sprites.add( bot2 )

    position += 500
    field_object['playerA'+str(player1Number)] = bot1
    field_object['playerB'+str(player1Number)] = bot2
    player1Number += 1

position = 110
for _ in range(3):
    bot1 = Bot1()
    bot1.setPosition( 470, position)
    all_sprites.add( bot1 )

    bot2 = Player2()
    bot2.setPosition( 1000, position)
    all_sprites.add( bot2 )    

    position += 300
    field_object['playerA'+str(player1Number)] = bot1
    field_object['playerB'+str(player1Number)] = bot2
    player1Number += 1

botAttack1 = Bot1()
botAttack1.setPosition( 650, 400)
all_sprites.add( botAttack1 )
field_object['playerA'+ str(player1Number)] = botAttack1

botAttack2 = Player2()
botAttack2.setPosition( 820, 400)
all_sprites.add( botAttack2 )
field_object['playerB'+str(player1Number)] = botAttack1

ball = Ball()
field_object['ball'] = ball
ball_sprite.add( ball )

print( field_object )
i = 0
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
    
    prolog.retractall('is_at')
    prolog.retractall('has')

    if i % 120 == 0:
        for k,v in field_object.items():
            prolog.assertz(f'is_at({k},{v.rect.x},{v.rect.y})')
            if isinstance(v, Player1) and v.haveBall:
                prolog.assertz(f'has({k},ball)')
        
        for q in prolog.query('mi(A)'):
            for action in q['A']:
                #print(action, action.arity)
                functor = str(action.name)
                if action.arity == 1:
                    argv = str(action.args[0])
                    #if argv not in field_object:
                    #    continue
                    if functor == "forward":
                        field_object[argv].forward()
                    elif functor == "backward":
                        field_object[argv].backward()
                    elif functor == "shoot":
                        print('Shoot!')
                        field_object[argv].shoot()
                elif action.arity == 2:
                    argv1 = str(action.args[0])
                    argv2 = str(action.args[1])
                    #if argv1 not in field_object or argv2 not in field_object:
                    #    continue
                    if functor == "follow":
                        field_object[argv1].follow(field_object[argv2])
                        field_object[argv1].isFollow = True
                    elif functor == "tackle":
                        field_object[argv1].tackle(field_object[argv2])
                    elif functor == "pass":
                        field_object[argv1].passball(field_object[argv2])

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

    i += 1