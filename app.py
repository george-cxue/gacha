import pygame
import random

pygame.init()

# Game start parameters
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GRAY = (128, 128, 128)

# Sounds - need to update paths
gunshot = pygame.mixer.Sound("sound effects/gunshot.wav")
bruh = pygame.mixer.Sound("sound effects/bruh.wav")
womp = pygame.mixer.Sound("sound effects/wompWomp.wav")
click = pygame.mixer.Sound("sound effects/clickSound.wav")

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
        gunshot.play()

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

# Start Screen
def start_screen():
    title_font = pygame.font.Font(None, 72)
    button_font = pygame.font.Font(None, 48)

    title_surface = title_font.render("GACHA SHOOTER PEW PEW", True, WHITE)
    play_button_surface = button_font.render("PLAY ", True, BLACK)

    button_rect = pygame.Rect((SCREEN_WIDTH // 2 - 75, SCREEN_HEIGHT // 2 + 50), (150, 50))

    running = True
    while running:
        screen.fill(BLACK)
        screen.blit(title_surface, (SCREEN_WIDTH // 2 - title_surface.get_width() // 2, SCREEN_HEIGHT // 2 - 100))
        
        pygame.draw.rect(screen, GRAY, button_rect)
        screen.blit(play_button_surface, (button_rect.x + 40, button_rect.y + 10))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    click.play()
                    running = False

        pygame.display.flip()
        clock.tick(60)

# Death Screen
def death_screen(score, money):
    title_font = pygame.font.Font(None, 72)
    button_font = pygame.font.Font(None, 48)

    game_over_surface = title_font.render("GAME OVER", True, WHITE)
    score_surface = button_font.render(f"Final Score: {score}", True, WHITE)
    money_surface = button_font.render(f"Final Money: {money}", True, WHITE)

    running = True
    while running:
        screen.fill(BLACK)
        screen.blit(game_over_surface, (SCREEN_WIDTH // 2 - game_over_surface.get_width() // 2, SCREEN_HEIGHT // 2 - 150))
        screen.blit(score_surface, (SCREEN_WIDTH // 2 - score_surface.get_width() // 2, SCREEN_HEIGHT // 2))
        screen.blit(money_surface, (SCREEN_WIDTH // 2 - money_surface.get_width() // 2, SCREEN_HEIGHT // 2 + 50))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                running = False

        pygame.display.flip()
        clock.tick(60)

# Main Game Function
def main_game():
    all_sprites = pygame.sprite.Group()
    bullets = pygame.sprite.Group()
    enemies = pygame.sprite.Group()

    global player
    player = Player()
    all_sprites.add(player)

    score = 0
    money = 0

    game = True
    while game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
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
            bruh.play()
            if player.health <= 0:
                womp.play()
                game = False

        for enemy in pygame.sprite.groupcollide(enemies, bullets, True, True):
            score += 1
            money += 1

        # Render
        screen.fill(BLACK)
        all_sprites.draw(screen)

        # Display health, score, and money
        font = pygame.font.Font(None, 36)
        health_surface = font.render(f"Health: {player.health}", True, WHITE)
        screen.blit(health_surface, (10, 10))

        score_money_surface = font.render(f"Score: {score}  Money: {money}", True, WHITE)
        screen.blit(score_money_surface, (SCREEN_WIDTH - 250, 10))

        pygame.display.flip()
        clock.tick(60)

    death_screen(score, money)

# Run Start Screen
start_screen()

# Run Main Game
main_game()
