import pygame
import random

pygame.init()

# pygame Setup
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

clock = pygame.time.Clock()


# Sprite Classes
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.speed = 5
        self.health = 100

    def move(self, dx, dy):
        self.rect.x += dx * self.speed
        self.rect.y += dy * self.speed
        # Keep player on screen
        self.rect.clamp_ip(screen.get_rect())

    def update(self):
        keys = pygame.key.get_pressed()
        dx = keys[pygame.K_d] - keys[pygame.K_a]
        dy = keys[pygame.K_s] - keys[pygame.K_w]
        self.move(dx, dy)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        super().__init__()
        self.image = pygame.Surface((5, 5))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 10
        self.direction = direction

    def update(self):
        self.rect.x += self.direction[0] * self.speed
        self.rect.y += self.direction[1] * self.speed
        # Remove bullet if it goes off-screen
        if not screen.get_rect().colliderect(self.rect):
            self.kill()

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randint(0, SCREEN_HEIGHT - self.rect.height)
        self.speed = random.randint(1, 3)

    def update(self):
        player_center = player.rect.center
        if self.rect.centerx < player_center[0]:
            self.rect.x += self.speed
        elif self.rect.centerx > player_center[0]:
            self.rect.x -= self.speed
        if self.rect.centery < player_center[1]:
            self.rect.y += self.speed
        elif self.rect.centery > player_center[1]:
            self.rect.y -= self.speed


# Sprites
all_sprites = pygame.sprite.Group()
bullets = pygame.sprite.Group()
enemies = pygame.sprite.Group()

player = Player()
all_sprites.add(player)

# Game Loop
game = True
while game:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print()
            game = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # left click
            if event.button == 1:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                direction = pygame.math.Vector2(mouse_x - player.rect.centerx, mouse_y - player.rect.centery)
                if direction.length() > 0:
                    direction = direction.normalize()
                bullet = Bullet(player.rect.centerx, player.rect.centery, direction)
                all_sprites.add(bullet)
                bullets.add(bullet)

    # Spawn enemies
    if len(enemies) < 5 and random.random() < 0.02:
        enemy = Enemy()
        all_sprites.add(enemy)
        enemies.add(enemy)

    # Update
    all_sprites.update()

    # Check for collisions
    for enemy in pygame.sprite.spritecollide(player, enemies, False):
        player.health -= 1
        if player.health <= 0:
            game = False

    for enemy in pygame.sprite.groupcollide(enemies, bullets, True, True):
        # Here you could add score, money, etc.
        pass

    screen.fill(BLACK)
    all_sprites.draw(screen)
    
    health_text = f"Health: {player.health}"
    font = pygame.font.Font(None, 36)
    health_surface = font.render(health_text, True, WHITE)
    screen.blit(health_surface, (10, 10))

    pygame.display.flip()

    clock.tick(60)

pygame.quit()
