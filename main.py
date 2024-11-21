import pygame
import random
import sys
from sprites import Player, Bullet, Enemy
from screens import (
    start_screen, 
    death_screen, 
    lottery_screen, 
    load_game_data, 
    save_game_data
)

# Initialization
pygame.init()

# Game start parameters
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("GACHA SHOOTER PEW PEW")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GRAY = (128, 128, 128)

# Sounds
gunshot = pygame.mixer.Sound("assets/sound_effects/gunshot.wav")
bruh = pygame.mixer.Sound("assets/sound_effects/bruh.wav")
womp = pygame.mixer.Sound("assets/sound_effects/wompWomp.wav")
click = pygame.mixer.Sound("assets/sound_effects/clickSound.wav")

clock = pygame.time.Clock()

def main_game(total_money, current_gun):
    all_sprites = pygame.sprite.Group()
    bullets = pygame.sprite.Group()
    enemies = pygame.sprite.Group()

    player = Player(SCREEN_WIDTH, SCREEN_HEIGHT)
    all_sprites.add(player)

    score = 0
    money = 0

    game = True
    while game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_game_data(total_money + money, current_gun)
                return total_money, current_gun, 'quit'
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    direction = pygame.math.Vector2(mouse_x - player.rect.centerx, mouse_y - player.rect.centery)
                    if direction.length() > 0:
                        direction = direction.normalize()
                    
                    # Use the current gun's shoot method
                    current_gun.shoot(
                        player.rect.centerx, 
                        player.rect.centery, 
                        direction, 
                        SCREEN_WIDTH, 
                        SCREEN_HEIGHT, 
                        gunshot, 
                        bullets, 
                        all_sprites
                    )

        # Spawn enemies
        if len(enemies) < 5 and random.random() < 0.02:
            enemy = Enemy(SCREEN_WIDTH, SCREEN_HEIGHT, player)
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

        gun_surface = font.render(f"Gun: {current_gun.__class__.__name__}", True, WHITE)
        screen.blit(gun_surface, (SCREEN_WIDTH - 250, 50))

        pygame.display.flip()
        clock.tick(60)

    return total_money + money, current_gun, 'death'

def main():
    # Load game data
    game_data = load_game_data()
    total_money = game_data['total_money']
    current_gun = game_data['current_gun']
    
    while True:
        # Start Screen
        start_action = start_screen(screen, SCREEN_WIDTH, SCREEN_HEIGHT, click)
        
        if start_action == 'quit':
            break
        elif start_action == 'play':
            # Main Game
            total_money, current_gun, result = main_game(total_money, current_gun)
            save_game_data(total_money, current_gun)
            
            if result == 'quit':
                break
            elif result == 'death':
                # Death Screen
                death_action = death_screen(screen, SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0, total_money, current_gun)
                
                if death_action == 'quit':
                    break
                elif death_action == 'home':
                    continue
        
        elif start_action == 'lottery':
            # Lottery Screen
            total_money, current_gun, lottery_action = lottery_screen(screen, SCREEN_WIDTH, SCREEN_HEIGHT, total_money, current_gun)
            save_game_data(total_money, current_gun)
            
            if lottery_action == 'quit':
                break
            elif lottery_action == 'home':
                continue

    # Cleanup
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()