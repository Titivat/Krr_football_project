from typing import Tuple
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
COLOR_GREEN = (0, 255, 0)
COLOR_BLUE = (0, 0, 255)

BACKGROUND = pygame.image.load("football_field")
BACKGROUND = pygame.transform.scale(BACKGROUND, (WINDOW_WIDTH, WINDOW_HEIGHT))

# Game window
game_window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('First Game')


class Player1(pygame.sprite.Sprite):
    def __init__(self, name):
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        self.image = pygame.Surface((25, 60))
        self.image.fill(COLOR_RED)
        self.rect = self.image.get_rect()
        self.goalPositionX = 1467
        self.goalPositionY = 386
        self.haveBall = False
        self.target_obj = None
        self.action_dic = {
            'follow': False,
            'shoot': False,
            'forward': False,
            'backward': False,
            "passto": False,
        }
        self.dx = 0
        self.dy = 0

    def update(self):
        self.dy = 0
        self.dx = 0

        if self.action_dic['follow']:
            self.action_dic['follow'] = False
            if self.target_obj == None:
                pass
            else:
                #self.dy = (self.target_obj.rect.y-self.rect.y) * 0.04
                self.dy = min((self.target_obj.rect.y-self.rect.y), 10)
                #self.dx = (self.target_obj.rect.x-self.rect.x) * 0.04
                self.dx = min((self.target_obj.rect.x-self.rect.x), 10)
        
        if self.action_dic['forward']:
            self.action_dic['forward'] = False
            if self.name in "playerB":
                self.dx = 10
            else:
                self.dx = -10
        
        if self.action_dic['backward']:
            self.action_dic['backward'] = False
            if self.name in "playerB":
                self.dx = -10
            else:
                self.dx = 10

        self.rect.y += self.dy
        self.rect.x += self.dx

    def follow(self, obj):
        self.action_dic['follow'] = True
        self.target_obj = obj

    def shoot(self):
        self.action_dic['shoot'] = True

    def passto(self, obj):
        self.action_dic['passto'] = True
        self.target_obj = obj

    def forward(self):
        self.action_dic['forward'] = True

    def backward(self):
        self.action_dic['backward'] = True

    def setPosition(self, left, center):
        self.rect.left = left
        self.rect.centery = center


class Player2(Player1):
    def __init__(self, name):
        super().__init__(name)
        self.image.fill(COLOR_BLUE)
        self.goalPositionX = 32
        self.goalPositionY = 396


class Ball(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((15, 15))
        self.image.fill(COLOR_WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)
        self.shoot = False
        self.player = None

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

        collion = pygame.sprite.spritecollideany(ball, all_sprites)
        if collion:
            if(type(collion) == Player1 or type(collion) == Player2):
                collion.haveBall = True
                self.player = collion
                self.shoot = False
                self.rect.x = collion.rect.x + 20
                self.rect.y = collion.rect.y + 55

            if collion.action_dic['shoot']:
                collion.action_dic['shoot'] = False
                collion.haveBall = False
                self.player = None
                self.shoot = True
                self.rect.x -= self.dx
                self.dx *= -1
                dx = (collion.goalPositionX-collion.rect.x) * 0.1
                dy = (collion.goalPositionY-collion.rect.y) * 0.1
                self.dy += dy
                self.dx += dx

            if collion.action_dic['passto']:
                collion.action_dic['passto'] = False
                collion.haveBall = False
                self.player = None
                self.shoot = True
                self.rect.x -= self.dx
                self.dx *= -1
                dx = (collion.target_obj.rect.x-collion.rect.x) * 0.1
                dy = (collion.target_obj.react.y-collion.rect.y) * 0.1
                self.dy += dy
                self.dx += dx

# main
all_sprites = pygame.sprite.Group()
ball_sprite = pygame.sprite.GroupSingle()
ball = Ball()
ball_sprite.add(ball)

field_object = {}
player1Number = 1
player1 = Player1('playerA'+str(player1Number))
player1.setPosition(40, WINDOW_HEIGHT / 2)
field_object['playerA'+str(player1Number)] = player1

all_sprites.add(player1)

player2 = Player2('playerB'+str(player1Number))
player2.setPosition(WINDOW_WIDTH - 65, WINDOW_HEIGHT / 2)
field_object['playerB'+str(player1Number)] = player2
all_sprites.add(player2)

player1Number += 1

position = 150
for _ in range(2):
    bot1 = Player1('playerA'+str(player1Number))
    bot1.setPosition(300, position)
    all_sprites.add(bot1)

    bot2 = Player2('playerB'+str(player1Number))
    bot2.setPosition(1170, position)
    all_sprites.add(bot2)

    position += 500
    field_object['playerA'+str(player1Number)] = bot1
    field_object['playerB'+str(player1Number)] = bot2
    player1Number += 1

position = 110
for _ in range(3):
    bot1 = Player1('playerA'+str(player1Number))
    bot1.setPosition(470, position)
    all_sprites.add(bot1)

    bot2 = Player2('playerB'+str(player1Number))
    bot2.setPosition(1000, position)
    all_sprites.add(bot2)

    position += 300
    field_object['playerA'+str(player1Number)] = bot1
    field_object['playerB'+str(player1Number)] = bot2
    player1Number += 1

botAttack1 = Player1('playerA' + str(player1Number))
botAttack1.setPosition(650, 400)
all_sprites.add(botAttack1)
field_object['playerA' + str(player1Number)] = botAttack1

botAttack2 = Player2('playerB'+str(player1Number))
botAttack2.setPosition(820, 400)
all_sprites.add(botAttack2)
field_object['playerB'+str(player1Number)] = botAttack2

ball = Ball()
field_object['ball'] = ball
ball_sprite.add(ball)
print( field_object )

count = 0
prolog.retractall('is_at(_,_,_)')
prolog.retractall('has(_,_,_)')
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
            print(pos)

    prolog.retractall('is_at(_,_,_)')
    prolog.retractall('has(_,_,_)')
    
    for k, v in field_object.items():
        prolog.assertz(f'is_at({k},{v.rect.x},{v.rect.y})')
        if isinstance(v, Ball) and v.player:
            prolog.assertz(f'has({v.player.name},ball)')

    for q in prolog.query('mi(A)'):
        for action in q['A']:
            #print(action)
            functor = str(action.name)
            if action.arity == 1:
                argv = str(action.args[0])
                if functor == "forward":
                    field_object[argv].forward()
                elif functor == "backward":
                    field_object[argv].backward()
                elif functor == "shoot":
                    field_object[argv].shoot()
            elif action.arity == 2:
                argv1 = str(action.args[0])
                argv2 = str(action.args[1])
                if functor == "follow":
                    field_object[argv1].follow(field_object[argv2])
                    #field_object[argv1].isFollow = True
                # elif functor == "tackle":
                #    field_object[argv1].tackle(field_object[argv2])
                elif functor == "pass":
                    field_object[argv1].passto(field_object[argv2])

    all_sprites.update()
    ball_sprite.update()

    game_window.blit(BACKGROUND, (0, 0))

    all_sprites.draw(game_window)
    ball_sprite.draw(game_window)

    count += 1

    pygame.display.flip()
