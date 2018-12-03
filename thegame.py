import serial
import pygame
import sys
import math
from pygame.locals import *
from random import randint


class Ship(pygame.sprite.Sprite):
    # Constructor. Pass in the color of the block,
    # and its x and y position
    def __init__(self, image, width, height):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)
        raw_image = pygame.image.load(image)
        self.image = pygame.transform.scale(raw_image, (width, height)).convert_alpha()
        self.vanilla_image = self.image.copy()
        self.rot = 0
        self.fire = False
        self.last_shot = 0

        # Fetch the rectangle object that has the dimensions of the image
        # Update the position of this object by setting the values of rect.x and rect.y
        self.rect = self.image.get_rect()
        self.rect.x = 512
        self.rect.y = 800
        self.arduino = serial.Serial('/dev/ttyACM0', 4800)

    def update(self):
        x_speed = 0.02
        y_speed = 0.03
        line = self.arduino.readline()

        # If you fail, try try again
        while len(line.split()) != 6:
            line = self.arduino.readline()

        shoot, player_x, player_y, tilt_x, tilt_y, tilt_z = line.split()

        # Rate limit the firing
        self.fire = self.last_shot > 4 and int(shoot) == 0
        if self.fire:
            self.last_shot = 0
        else:
            self.last_shot += 1

        self.rect.x = min(max(0, self.rect.x - ((max(0, float(player_x)) - 508) * x_speed)), 965)
        self.rect.y = min(max(700, self.rect.y + ((max(0, float(player_y)) - 503) * y_speed)), 965)
        self.rot = (self.rot + float(tilt_x) * 40) / 2  # Smooths rotation out a bit instead of raw accel values
        self.image = pygame.transform.rotate(self.vanilla_image, self.rot)


class Baddies(pygame.sprite.Sprite):
    """ This class represents the baddies. """

    def __init__(self, x, y):
        # Call the parent class (Sprite) constructor
        super().__init__()

        raw_image = pygame.image.load('assets/hack.png')
        self.image = pygame.transform.scale(raw_image, (96, 96)).convert_alpha()

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        """ Move the bullet. """
        self.rect.y += randint(0, 15)
        self.rect.x -= randint(0, 50) - 25


class Bullet(pygame.sprite.Sprite):
    """ This class represents the bullets. """

    def __init__(self, x, y, rot):
        # Call the parent class (Sprite) constructor
        super().__init__()

        self.image = pygame.Surface([4, 10])
        self.image.fill((255, 255, 255))

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.rot = rot

    def update(self):
        """ Move the bullet. """
        self.rect.y -= 30 * math.cos(math.radians(self.rot))
        self.rect.x -= 30 * math.sin(math.radians(self.rot))


def calc_bullet_init(sprite_ship):
    x, y = sprite_ship.rect.midtop
    center_x, center_y = sprite.rect.center
    rad = math.radians(sprite_ship.rot)

    new_x = (math.cos(rad) * (center_x - x)) + (math.sin(rad) * (y - center_y)) + x
    new_y = (math.sin(rad) * (center_x - x)) - (math.cos(rad) * (y - center_y)) + y

    if rad > 0:
        new_x += 64 / 2

    return new_x, new_y, sprite_ship.rot


pygame.init()
pygame.display.set_caption("Sp00k Invaders!")
screen = pygame.display.set_mode((1024, 1024))
clock = pygame.time.Clock()

def init_game():
    global player_sprite, bullet_sprites, baddies_sprites, player, score, running, since_spawn
    player_sprite = pygame.sprite.Group()
    bullet_sprites = pygame.sprite.Group()
    baddies_sprites = pygame.sprite.Group()
    ship_parking_spot = 'assets/blueship2.png'
    player = Ship(ship_parking_spot, 64, 64)
    player_sprite.add(player)
    score = 0
    running = True
    since_spawn = 0
5

global best_scare
best_scare = 0


init_game()

while running:
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        # Check escape key
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
        # Check quit signal
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    for sprite in player_sprite:
        if sprite.fire:
            bullet_sprites.add(Bullet(*calc_bullet_init(sprite)))

    for bullet in bullet_sprites:
        # Remove the bullet if it flies up off the screen
        if bullet.rect.y < -10:
            bullet_sprites.remove(bullet)

    kills = pygame.sprite.groupcollide(bullet_sprites, baddies_sprites, True, True)

    if since_spawn > 10:
        for i in range(score//500 + 1):
            bad = Baddies(randint(25, 1000), 25)
            baddies_sprites.add(bad)
        since_spawn = 0
    else:
        since_spawn += 1

    score += len(kills) * 100

    player_sprite.update()
    player_sprite.draw(screen)

    bullet_sprites.update()
    bullet_sprites.draw(screen)

    baddies_sprites.update()
    baddies_sprites.draw(screen)

    if pygame.sprite.spritecollideany(player, baddies_sprites):
        running = False

    font_name = pygame.font.match_font('arial')
    if running:
        font = pygame.font.Font(font_name, 30)
        text_surface = font.render("Ur Scare: " + str(score), True, (255, 255, 255))
        text_rect = text_surface.get_rect()
        text_rect.midtop = (900, 30)
        screen.blit(text_surface, text_rect)
    else:
        screen.fill((0, 0, 0))
        font = pygame.font.Font(font_name, 100)

        text_surface_spook = font.render("2 sp00kd", True, (255, 255, 255))
        text_rect = text_surface_spook.get_rect()
        text_rect.midtop = (512, 250)
        screen.blit(text_surface_spook, text_rect)

        text_surface_scare = font.render("Ur Scare: " + str(score), True, (255, 255, 255))
        text_rect = text_surface_scare.get_rect()
        text_rect.midtop = (512, 450)
        screen.blit(text_surface_scare, text_rect)

        best_scare = max(best_scare, score)
        text_surface_best_scare = font.render("Best Scare: " + str(best_scare), True, (255, 255, 255))
        text_rect = text_surface_best_scare.get_rect()
        text_rect.midtop = (512, 650)
        screen.blit(text_surface_best_scare, text_rect)

        pygame.display.update()
        pygame.time.wait(3500)
        init_game()

    pygame.display.update()
    clock.tick(300)
