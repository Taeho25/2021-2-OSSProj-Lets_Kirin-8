import pygame
import random
import math
from pygame.locals import *
from load import load_image


class MasterSprite(pygame.sprite.Sprite):
    allsprites = None
    speed = None


class Explosion(MasterSprite):
    pool = pygame.sprite.Group()
    active = pygame.sprite.Group()

    def __init__(self):
        super().__init__()
        self.image, self.rect = load_image('explosion.png', -1)
        self.linger = MasterSprite.speed * 3

    @classmethod
    def position(cls, loc):
        if len(cls.pool) > 0:
            explosion = cls.pool.sprites()[0]
            explosion.add(cls.active, cls.allsprites)
            explosion.remove(cls.pool)
            explosion.rect.center = loc
            explosion.linger = 12

    def update(self):
        self.linger -= 1
        if self.linger <= 0:
            self.remove(self.allsprites, self.active)
            self.add(self.pool)


class Leaf(MasterSprite):
    pool = pygame.sprite.Group()
    active = pygame.sprite.Group()

    def __init__(self):
        super().__init__()
        self.image, self.rect = load_image('leaf.png', -1)
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()

    @classmethod
    def position(cls, loc):
        if len(cls.pool) > 0:
            leaf = cls.pool.sprites()[0]
            leaf.add(cls.allsprites, cls.active)
            leaf.remove(cls.pool)
            leaf.rect.midbottom = loc
    
    def table(self):
        self.add(self.pool)
        self.remove(self.allsprites, self.active)

    def update(self):
        newpos = self.rect.move(0, -4 * MasterSprite.speed)
        self.rect = newpos
        if self.rect.top < self.area.top:
            self.table()


class Bomb(pygame.sprite.Sprite):
    def __init__(self, kirin):
        super().__init__()
        self.image = None
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.radius = 20
        self.radiusIncrement = 4
        self.rect = kirin.rect

    def update(self):
        self.radius += self.radiusIncrement
        pygame.draw.circle(
            pygame.display.get_surface(),
            pygame.Color(153, 76, 0, 128),
            self.rect.center, self.radius, 3)
        if (self.rect.center[1] - self.radius <= self.area.top
            and self.rect.center[1] + self.radius >= self.area.bottom
            and self.rect.center[0] - self.radius <= self.area.left
                and self.rect.center[0] + self.radius >= self.area.right):
            self.kill()


class Powerup(MasterSprite):
    def __init__(self, kindof):
        super().__init__()
        self.image, self.rect = load_image(kindof + '_powerup.png', -1)
        self.original = self.image
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.rect.midtop = (random.randint(
                            self.area.left + self.rect.width // 2,
                            self.area.right - self.rect.width // 2),
                            self.area.top)
        self.angle = 0

    def update(self):
        center = self.rect.center
        self.angle = (self.angle + 2) % 360
        rotate = pygame.transform.rotate
        self.image = rotate(self.original, self.angle)
        self.rect = self.image.get_rect(
            center=(
                center[0],
                center[1] +
                MasterSprite.speed))


class BombPowerup(Powerup):
    def __init__(self):
        super().__init__('bomb')
        self.pType = 'bomb'


class ShieldPowerup(Powerup):
    def __init__(self):
        super().__init__('shield')
        self.pType = 'shield'

class DoubleleafPowerup(Powerup):
    def __init__(self):
        super().__init__('doubleleaf')
        self.pType = 'doubleleaf'

class FriendPowerup(Powerup):
    def __init__(self):
        super().__init__('friendkirin')
        self.pType = 'friendkirin'

class LifePowerup(Powerup):
    def __init__(self):
        super().__init__('life')
        self.pType = 'life'

class Kirin(MasterSprite):
    def __init__(self, screen_size):
        super().__init__()
        self.image, self.rect = load_image('kirin.png', -1)
        self.original = self.image
        self.shield, self.rect = load_image('kirin_shield.png', -1)
        # 수정 쉴드랑 조금 다른 방법이 필요함
        # self.bomb, self.rect = load_image('kirin_bomb.png', -1)
        self.screen_size = screen_size
        self.ratio = (self.screen_size / 500)
        self.screen = pygame.display.set_mode((self.screen_size, self.screen_size), HWSURFACE|DOUBLEBUF|RESIZABLE)
        self.area = self.screen.get_rect()
        self.rect.midbottom = (self.screen.get_width() // 2, self.area.bottom)
        self.radius = max(self.rect.width, self.rect.height)
        self.alive = True
        self.shieldUp = False
        # 수정
        # self.bombUp = False
        self.vert = 0
        self.horiz = 0
        self.life = 3  

    def initializeKeys(self):
        keyState = pygame.key.get_pressed()
        self.vert = 0
        self.horiz = 0
        if keyState[pygame.K_w]:
            self.vert -= 2 * MasterSprite.speed
        if keyState[pygame.K_a]:
            self.horiz -= 2 * MasterSprite.speed
        if keyState[pygame.K_s]:
            self.vert += 2 * MasterSprite.speed
        if keyState[pygame.K_d]:
            self.horiz += 2 * MasterSprite.speed

    def update(self): # argument - screen_size
        #self.screen_size = screen_size
        newpos = self.rect.move((self.horiz, self.vert))
        newhoriz = self.rect.move((self.horiz, 0))
        newvert = self.rect.move((0, self.vert))

        if not (newpos.left <= self.area.left
                or newpos.top <= self.area.top
                or newpos.right >= self.area.right
                or newpos.bottom >= self.area.bottom):
            self.rect = newpos
        elif not (newhoriz.left <= self.area.left
                  or newhoriz.right >= self.area.right):
            self.rect = newhoriz
        elif not (newvert.top <= self.area.top
                  or newvert.bottom >= self.area.bottom):
            self.rect = newvert

        if self.shieldUp and self.image != self.shield:
            self.image = self.shield

        if not self.shieldUp and self.image != self.original:
            self.image = self.original
        
        # 수정
        # if self.bombUp and self.image != self.bomb:
        #     self.image = self.bomb

        # if not self.bombUp and self.image != self.original:
        #     self.image = self.original

    def bomb(self):
        return Bomb(self)

class Friendkirin(MasterSprite):
    def __init__(self):
        super().__init__()
        self.image, self.rect = load_image('friendkirin.png', -1)
        self.original = self.image
        self.screen = pygame.display.get_surface()
        self.area = self.screen.get_rect()
        self.radius = max(self.rect.width, self.rect.height)
   
    def remove(self) :
        pygame.sprite.Sprite.kill(self)

class Kirin2(MasterSprite):
    def __init__(self):
        super().__init__()
        self.image, self.rect = load_image('kirin.png', -1)
        self.original = self.image
        self.shield, self.rect = load_image('kirin_shield.png', -1)
        self.screen = pygame.display.get_surface()
        self.area = self.screen.get_rect()
        self.rect.midbottom = (self.screen.get_width() * (1/4) , self.area.bottom)
        # self.rect.midbottom = (500 * 1/3, 500)
        self.radius = max(self.rect.width, self.rect.height)
        self.alive = True
        self.shieldUp = False
        self.vert = 0
        self.horiz = 0
        self.life = 3   

    def initializeKeys(self):
        keyState = pygame.key.get_pressed()
        self.vert = 0
        self.horiz = 0

    def update(self):
        newpos = self.rect.move((self.horiz, self.vert))
        newhoriz = self.rect.move((self.horiz, 0))
        newvert = self.rect.move((0, self.vert))

        if not (newpos.left <= self.area.left
                or newpos.top <= self.area.top
                or newpos.right >= (self.area.width / 2)
                or newpos.bottom >= self.area.bottom):
            self.rect = newpos
        elif not (newhoriz.left <= self.area.left
                  or newhoriz.right >= (self.area.width / 2)):
            self.rect = newhoriz
        elif not (newvert.top <= self.area.top
                  or newvert.bottom >= self.area.bottom):
            self.rect = newvert

        if self.shieldUp and self.image != self.shield:
            self.image = self.shield

        if not self.shieldUp and self.image != self.original:
            self.image = self.original

    def bomb(self):
        return Bomb(self)

class Kirin3(MasterSprite):
    def __init__(self):
        super().__init__()
        self.image, self.rect = load_image('kirin.png', -1)
        self.original = self.image
        self.shield, self.rect = load_image('kirin_shield.png', -1)
        self.screen = pygame.display.get_surface()
        self.area = self.screen.get_rect()
        self.rect.midbottom = (self.screen.get_width() * (3/4), self.area.bottom)
        # self.rect.midbottom = (500 * 0.5, 500)
        self.radius = max(self.rect.width, self.rect.height)
        self.alive = True
        self.shieldUp = False
        self.vert = 0
        self.horiz = 0
        self.life = 3   # 초기 생명 3개

    def initializeKeys(self):
        keyState = pygame.key.get_pressed()
        self.vert = 0
        self.horiz = 0

    def update(self):
        newpos = self.rect.move((self.horiz, self.vert))
        newhoriz = self.rect.move((self.horiz, 0))
        newvert = self.rect.move((0, self.vert))

        if not (newpos.left <= (self.area.width / 2)
                or newpos.top <= self.area.top
                or newpos.right >= self.area.right
                or newpos.bottom >= self.area.bottom):
            self.rect = newpos
        elif not (newhoriz.left <= (self.area.width / 2)
                  or newhoriz.right >= self.area.right):
            self.rect = newhoriz
        elif not (newvert.top <= self.area.top
                  or newvert.bottom >= self.area.bottom):
            self.rect = newvert

        if self.shieldUp and self.image != self.shield:
            self.image = self.shield

        if not self.shieldUp and self.image != self.original:
            self.image = self.original

    def bomb(self):
        return Bomb(self)

class Bear(MasterSprite):
    pool = pygame.sprite.Group()
    active = pygame.sprite.Group()

    def __init__(self, color):
        super().__init__()
        self.image, self.rect = load_image(
            'bear_' + color + '.png', -1)
        self.initialRect = self.rect
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.loc = 0
        self.radius = min(self.rect.width // 2, self.rect.height // 2)

    @classmethod
    def position(cls):
        if len(cls.pool) > 0 and cls.numOffScreen > 0:
            bear = random.choice(cls.pool.sprites())
            if isinstance(bear, Crawly):
                bear.rect.midbottom = (random.choice(
                    (bear.area.left, bear.area.right)),
                    random.randint(
                    (bear.area.bottom * 3) // 4,
                    bear.area.bottom))
            else:
                bear.rect.midtop = (random.randint(
                    bear.area.left
                    + bear.rect.width // 2,
                    bear.area.right
                    - bear.rect.width // 2),
                    bear.area.top)
            bear.initialRect = bear.rect
            bear.loc = 0
            bear.add(cls.allsprites, cls.active)
            bear.remove(cls.pool)
            Bear.numOffScreen -= 1

    def update(self):
        horiz, vert = self.moveFunc()
        if horiz + self.initialRect.x > 500:
            horiz -= 500 + self.rect.width
        elif horiz + self.initialRect.x < 0 - self.rect.width:
            horiz += 500 + self.rect.width
        self.rect = self.initialRect.move((horiz, self.loc + vert))
        self.loc = self.loc + MasterSprite.speed
        if self.rect.top > self.area.bottom:
            self.table()
            Bear.numOffScreen += 1

    def table(self):
        self.kill()
        self.add(self.pool)


class Siney(Bear):
    def __init__(self):
        super().__init__('green')
        self.amp = random.randint(self.rect.width, 3 * self.rect.width)
        self.freq = (1 / 20)
        self.moveFunc = lambda: (self.amp * math.sin(self.loc * self.freq), 0)
        self.pType = 'green'


class Roundy(Bear):
    def __init__(self):
        super().__init__('red')
        self.amp = random.randint(self.rect.width, 2 * self.rect.width)
        self.freq = 1 / (20)
        self.moveFunc = lambda: (
            self.amp *
            math.sin(
                self.loc *
                self.freq),
            self.amp *
            math.cos(
                self.loc *
                self.freq))
        self.pType = 'red'


class Spikey(Bear):
    def __init__(self):
        super().__init__('blue')
        self.slope = random.choice(list(x for x in range(-3, 3) if x != 0))
        self.period = random.choice(list(4 * x for x in range(10, 41)))
        self.moveFunc = lambda: (self.slope * (self.loc % self.period)
                                 if self.loc % self.period < self.period // 2
                                 else self.slope * self.period // 2
                                 - self.slope * ((self.loc % self.period)
                                 - self.period // 2), 0)
        self.pType = 'orange'


class Fasty(Bear):
    def __init__(self):
        super().__init__('white')
        self.moveFunc = lambda: (0, 1.5 * self.loc)
        self.pType = 'white'


class Crawly(Bear):
    def __init__(self):
        super().__init__('yellow')
        self.moveFunc = lambda: (self.loc, 0)
        self.pType = 'yellow'

    def update(self):
        horiz, vert = self.moveFunc()
        horiz = (-horiz if self.initialRect.center[0] == self.area.right
                 else horiz)
        if (horiz + self.initialRect.left > self.area.right
                or horiz + self.initialRect.right < self.area.left):
            self.table()
            Bear.numOffScreen += 1
        self.rect = self.initialRect.move((horiz, vert))
        self.loc = self.loc + MasterSprite.speed
