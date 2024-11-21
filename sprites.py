import pygame
import random

class Player(pygame.sprite.Sprite):
    def __init__(self, screen_width, screen_height):
        super().__init__()
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.image = pygame.Surface((30, 30))
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.center = (screen_width // 2, screen_height // 2)
        self.speed = 5
        self.health = 100

    def move(self, dx, dy):
        self.rect.x += dx * self.speed
        self.rect.y += dy * self.speed
        # Keep player on screen
        self.rect.clamp_ip(pygame.Rect(0, 0, self.screen_width, self.screen_height))

    def update(self):
        keys = pygame.key.get_pressed()
        dx = keys[pygame.K_d] - keys[pygame.K_a]
        dy = keys[pygame.K_s] - keys[pygame.K_w]
        self.move(dx, dy)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction, screen_width, screen_height, gunshot_sound):
        super().__init__()
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.image = pygame.Surface((5, 5))
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 10
        self.direction = direction
        gunshot_sound.play()

    def update(self):
        self.rect.x += self.direction[0] * self.speed
        self.rect.y += self.direction[1] * self.speed
        # Remove bullet if it goes off-screen
        if not pygame.Rect(0, 0, self.screen_width, self.screen_height).colliderect(self.rect):
            self.kill()

class Enemy(pygame.sprite.Sprite):
    def __init__(self, screen_width, screen_height, player):
        super().__init__()
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.player = player
        self.image = pygame.Surface((20, 20))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, screen_width - self.rect.width)
        self.rect.y = random.randint(0, screen_height - self.rect.height)
        self.speed = random.randint(1, 3)

    def update(self):
        player_center = self.player.rect.center
        if self.rect.centerx < player_center[0]:
            self.rect.x += self.speed
        elif self.rect.centerx > player_center[0]:
            self.rect.x -= self.speed
        if self.rect.centery < player_center[1]:
            self.rect.y += self.speed
        elif self.rect.centery > player_center[1]:
            self.rect.y -= self.speed