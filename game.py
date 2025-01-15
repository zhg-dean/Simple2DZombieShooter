#Frozen Jam by tgfcoder <https://twitter.com/tgfcoder> licensed under CC-BY-3 

import pygame
import random
from os import path

img_folder = path.join(path.dirname(__file__), 'Img')

HEIGHT = 400
WIDTH = 1200
FPS = 60

#define colors
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
YELLOW = (255,255,0)

pygame.init()
pygame.mixer.init()
window = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption('WASD')
clock = pygame.time.Clock()

font_name = pygame.font.match_font('arial')
def draw_text(surf,text,size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x,y)
    surf.blit(text_surface, text_rect)

def new_mob():
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)

def show_go_screen():
    window.fill(BLUE)
    window.blit(background, background_rect)
    draw_text(window, 'COWBOY!', 54, WIDTH / 2, HEIGHT / 4)
    draw_text(window, 'Up/Down to move. Space to shoot', 22, WIDTH / 2, HEIGHT / 2)
    draw_text(window, 'Press a key to begin', 18, WIDTH / 2, HEIGHT * 3/4)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                waiting = False
                
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img, (50,38))
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        #pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.centery = HEIGHT / 2
        self.rect.left = 1.5 * self.rect.right
        self.speedy = 0
        self.shoot_delay = 750
        self.last_shot = pygame.time.get_ticks()

    def update(self):
        #timeout for gun
        self.speedy = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_UP]:
            self.speedy = -5
        if keystate[pygame.K_DOWN]:
            self.speedy = 5
        if keystate[pygame.K_UP] and keystate[pygame.K_DOWN]:
            self.speedy = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
        if self.rect.top < 90:
            self.rect.top = 90
        if keystate[pygame.K_SPACE]:
            self.shoot()
        self.rect.y += self.speedy

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            bullet = Bullet(self.rect.right, self.rect.centery)
            all_sprites.add(bullet)
            bullets.add(bullet)

 
class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_orig = zombie_img
        self.image_orig.set_colorkey(WHITE)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * 0.85 / 2)
        #pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.y = random.randrange( 100, HEIGHT - self.rect.height)
        self.rect.x = random.randrange(WIDTH + self.rect.width,WIDTH + 3 * self.rect.width)
        self.speedx = random.randrange(-3,-1)
        self.last_update = pygame.time.get_ticks()


    def update(self):
        self.rect.x += self.speedx

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.left = x
        self.rect.centery = y
        self.speedx = 5

    def update(self):
        self.rect.x += self.speedx
        if self.rect.left > WIDTH:
            self.kill()

#load all graphics
background = pygame.image.load(path.join(img_folder, 'background.png')).convert()
background = pygame.transform.scale(background, (WIDTH, HEIGHT))
background_rect = background.get_rect()
player_img = pygame.image.load(path.join(path.join(img_folder, 'Cowboy\\Cowboy2_idle with gun_0.png')), ).convert()
bullet_img = pygame.image.load(path.join(path.join(img_folder, 'Bullet\\bullet.png')), ).convert()
bullet_img =  pygame.transform.scale(bullet_img,(50,25))
zombie_img = pygame.image.load(path.join(path.join(img_folder, 'Zombie\\Zombie1.png')), ).convert()

game_over = True
#game loop
running = True
score = 0
while running:
    if game_over:
        show_go_screen()
        game_over = False
        all_sprites = pygame.sprite.Group()
        mobs = pygame.sprite.Group()
        bullets = pygame.sprite.Group()
        powerups = pygame.sprite.Group()
        player = Player()
        all_sprites.add(player)
        for i in range(8):
            new_mob()
        score = 0
    #running at right speed
    clock.tick(FPS)
    #process input(event)
    for event in pygame.event.get():    
        if event.type == pygame.QUIT:
            pygame.quit() 

    #update
    all_sprites.update()

    #check if hit
    hits = pygame.sprite.spritecollide(player, mobs, True, pygame.sprite.collide_circle) 
    for hit in hits:   #empty list==False
        new_mob()
        game_over = True



    #check if bullet hit a mob
    hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
    for hit in hits:
        score += 50 - hit.radius
        new_mob()

        if random.random() < 0.10:
            new_mob()
            player.shoot_delay *= 0.90


    for mob in mobs:
        if (mob.rect.right < 0):
            game_over = True

    #draw/render
    window.fill(BLUE)
    window.blit(background, background_rect)
    all_sprites.draw(window)
    draw_text(window, str(score), 20, WIDTH/2, 10)
    #after drawing everything
    pygame.display.flip()

pygame.quit()
