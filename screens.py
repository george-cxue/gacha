import pygame
import random
import json
import os
from sprites import Pistol, TwoPumpGun, ShotgunGun, MinugunGun

def get_gun_from_name(gun_name):
    gun_map = {
        "TwoPumpGun": TwoPumpGun(),
        "ShotgunGun": ShotgunGun(),
        "MinugunGun": MinugunGun()
    }
    return gun_map.get(gun_name, Pistol())

def load_game_data():
    if os.path.exists('save_data.json'):
        with open('save_data.json', 'r') as f:
            data = json.load(f)
            return {
                'total_money': data.get('total_money', 0),
                'current_gun': get_gun_from_name(data.get('current_gun', 'TwoPumpGun'))
            }
    return {
        'total_money': 0,
        'current_gun': TwoPumpGun()
    }

def save_game_data(total_money, current_gun):
    with open('save_data.json', 'w') as f:
        json.dump({
            'total_money': total_money,
            'current_gun': current_gun.__class__.__name__
        }, f)

def get_random_gun():
    guns = [
        {"type": TwoPumpGun(), "probability": 0.7},
        {"type": ShotgunGun(), "probability": 0.2},
        {"type": MinugunGun(), "probability": 0.1}
    ]

    random_val = random.random()
    cumulative_prob = 0

    for gun in guns:
        cumulative_prob += gun['probability']
        if random_val <= cumulative_prob:
            return gun['type']
    
    return guns[0]['type']

def start_screen(screen, screen_width, screen_height, click_sound):
    total_money = load_game_data()['total_money']
    title_font = pygame.font.Font(None, 72)
    button_font = pygame.font.Font(None, 48)

    # Define button rectangles
    play_button_rect = pygame.Rect((screen_width // 2 - 100, screen_height // 2), (200, 50))
    lottery_button_rect = pygame.Rect((screen_width // 2 - 100, screen_height // 2 + 100), (200, 50))
    quit_button_rect = pygame.Rect((screen_width // 2 - 100, screen_height // 2 + 200), (200, 50))

    title_surface = title_font.render("GACHA SHOOTER PEW PEW", True, (255, 255, 255))
    play_button_surface = button_font.render("PLAY", True, (0, 0, 0))
    lottery_button_surface = button_font.render("LOTTERY", True, (0, 0, 0))
    quit_button_surface = button_font.render("QUIT", True, (0, 0, 0))
    money_surface = button_font.render(f"Money: {total_money}", True, (255, 255, 255))

    running = True
    while running:
        screen.fill((0, 0, 0))
        screen.blit(title_surface, (screen_width // 2 - title_surface.get_width() // 2, screen_height // 2 - 200))
        screen.blit(money_surface, (10, 10))

        # Draw buttons
        pygame.draw.rect(screen, (128, 128, 128), play_button_rect)
        screen.blit(play_button_surface, (play_button_rect.x + 70, play_button_rect.y + 10))

        pygame.draw.rect(screen, (128, 128, 128), lottery_button_rect)
        screen.blit(lottery_button_surface, (lottery_button_rect.x + 50, lottery_button_rect.y + 10))

        pygame.draw.rect(screen, (128, 128, 128), quit_button_rect)
        screen.blit(quit_button_surface, (quit_button_rect.x + 70, quit_button_rect.y + 10))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'quit'
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if play_button_rect.collidepoint(event.pos):
                    click_sound.play()
                    return 'play'
                elif lottery_button_rect.collidepoint(event.pos):
                    click_sound.play()
                    return 'lottery'
                elif quit_button_rect.collidepoint(event.pos):
                    click_sound.play()
                    return 'quit'

        pygame.display.flip()
        pygame.time.Clock().tick(60)

def death_screen(screen, screen_width, screen_height, score, money, total_money, current_gun):
    total_money += money  # Add earned money to total
    save_game_data(total_money, current_gun)  # Save total money

    title_font = pygame.font.Font(None, 72)
    button_font = pygame.font.Font(None, 48)

    game_over_surface = title_font.render("GAME OVER", True, (255, 255, 255))
    score_surface = button_font.render(f"Final Score: {score}", True, (255, 255, 255))
    money_surface = button_font.render(f"Money Earned: {money}", True, (255, 255, 255))
    total_money_surface = button_font.render(f"Total Money: {total_money}", True, (255, 255, 255))

    replay_button_rect = pygame.Rect((screen_width // 2 - 150, screen_height // 2 + 100), (300, 50))
    home_button_rect = pygame.Rect((screen_width // 2 - 150, screen_height // 2 + 200), (300, 50))

    replay_surface = button_font.render("REPLAY", True, (0, 0, 0))
    home_surface = button_font.render("HOME SCREEN", True, (0, 0, 0))

    running = True
    while running:
        screen.fill((0, 0, 0))
        screen.blit(game_over_surface, (screen_width // 2 - game_over_surface.get_width() // 2, screen_height // 2 - 200))
        screen.blit(score_surface, (screen_width // 2 - score_surface.get_width() // 2, screen_height // 2 - 100))
        screen.blit(money_surface, (screen_width // 2 - money_surface.get_width() // 2, screen_height // 2 - 50))
        screen.blit(total_money_surface, (screen_width // 2 - total_money_surface.get_width() // 2, screen_height // 2))

        pygame.draw.rect(screen, (128, 128, 128), replay_button_rect)
        screen.blit(replay_surface, (replay_button_rect.x + 100, replay_button_rect.y + 10))

        pygame.draw.rect(screen, (128, 128, 128), home_button_rect)
        screen.blit(home_surface, (home_button_rect.x + 70, home_button_rect.y + 10))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'quit'
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if replay_button_rect.collidepoint(event.pos):
                    return 'play'
                elif home_button_rect.collidepoint(event.pos):
                    return 'home'

        pygame.display.flip()
        pygame.time.Clock().tick(60)

def lottery_screen(screen, screen_width, screen_height, total_money, current_gun):
    title_font = pygame.font.Font(None, 72)
    button_font = pygame.font.Font(None, 48)
    text_font = pygame.font.Font(None, 36)

    lottery_surface = title_font.render("GUN LOTTERY", True, (255, 255, 255))
    money_surface = text_font.render(f"Total Money: {total_money}", True, (255, 255, 255))
    current_gun_surface = text_font.render(f"Current Gun: {current_gun.__class__.__name__}", True, (255, 255, 255))

    # Lottery draw button
    draw_button_rect = pygame.Rect((screen_width // 2 - 150, screen_height // 2), (300, 50))
    draw_surface = button_font.render("DRAW GUN (50 $)", True, (0, 0, 0))

    home_button_rect = pygame.Rect((screen_width // 2 - 100, screen_height - 100), (200, 50))
    home_surface = button_font.render("HOME", True, (0, 0, 0))

    new_gun_surface = None

    running = True
    while running:
        screen.fill((0, 0, 0))
        screen.blit(lottery_surface, (screen_width // 2 - lottery_surface.get_width() // 2, screen_height // 2 - 250))
        screen.blit(money_surface, (10, 10))
        screen.blit(current_gun_surface, (10, 50))

        pygame.draw.rect(screen, (128, 128, 128), draw_button_rect)
        screen.blit(draw_surface, (draw_button_rect.x + 20, draw_button_rect.y + 10))

        pygame.draw.rect(screen, (128, 128, 128), home_button_rect)
        screen.blit(home_surface, (home_button_rect.x + 70, home_button_rect.y + 10))

        # Display new gun if drawn
        if new_gun_surface:
            screen.blit(new_gun_surface, (screen_width // 2 - new_gun_surface.get_width() // 2, screen_height // 2 + 100))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return total_money, current_gun, 'quit'
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if home_button_rect.collidepoint(event.pos):
                    return total_money, current_gun, 'home'
                
                if draw_button_rect.collidepoint(event.pos):
                    if total_money >= 50:
                        total_money -= 50
                        drawn_gun = get_random_gun()
                        new_gun_surface = text_font.render(f"You drew: {drawn_gun.__class__.__name__}!", True, (255, 255, 255))
                        current_gun = drawn_gun
                        save_game_data(total_money, current_gun)

        pygame.display.flip()
        pygame.time.Clock().tick(60)