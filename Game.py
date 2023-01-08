import pygame
import random
from classes.player import Player
from classes.mob import Mob
from classes.explosion import Explosion

WIDTH = 480
HEIGHT = 600
FPS = 60


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)


pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My game")
clock = pygame.time.Clock()

background = pygame.image.load("image/back.jpg").convert()
background = pygame.transform.scale(background,(WIDTH,HEIGHT))
background_rect = background.get_rect()

font_name = pygame.font.match_font('arial')

pygame.mixer.music.load("music/2cac23a4fb05632.mp3")
pygame.mixer.music.set_volume(0.3)

shoot_sound = pygame.mixer.Sound("music/sfx_laser1.ogg")
shoot_sound.set_volume(0.2)
pygame.mixer.music.play(-1)
def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

def draw_shield_bar(surf, x, y, pct):
    if pct < 0:
        pct = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    fill = (pct / 100) * BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surf, GREEN, fill_rect)
    pygame.draw.rect(surf, WHITE, outline_rect, 2)



all_sprites = pygame.sprite.Group()
mobs = pygame.sprite.Group()
bullets = pygame.sprite.Group()

player = Player()
all_sprites.add(player)
def newmob():
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)

for i in range(8):
    newmob()



score = 0
running = True
while running:

    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bullet = player.shoot()
                all_sprites.add(bullet)
                bullets.add(bullet)
                shoot_sound.play()
    all_sprites.update()
    hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
    for hit in hits:
        score += 50
        expl = Explosion(hit.rect.center, 'lg')
        all_sprites.add(expl)
        newmob()
    hits = pygame.sprite.spritecollide(player, mobs,True, pygame.sprite.collide_circle)
    if hits:
        player.shield -= 35
        expl = Explosion(hit.rect.center, 'sm')
        all_sprites.add(expl)
        newmob()
        if player.shield <= 0:
            running = False




    screen.fill(BLACK)
    screen.blit(background, background_rect)
    all_sprites.draw(screen)
    draw_text(screen, str(score), 18, WIDTH / 2, 10)
    draw_shield_bar(screen, 5, 5, player.shield)
    pygame.display.flip()
pygame.quit()
