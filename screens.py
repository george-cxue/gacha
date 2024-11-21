import pygame
import random
import json
import os

def load_money():
    """Load total money from a save file."""
    if os.path.exists('save_data.json'):
        with open('save_data.json', 'r') as f:
            data = json.load(f)
            return data.get('total_money', 0)
    return 0

def save_money(total_money):
    """Save total money to a save file."""
    with open('save_data.json', 'w') as f:
        json.dump({'total_money': total_money}, f)

def start_screen(screen, screen_width, screen_height, click_sound):
    """Display the start screen with Play, Lottery, and Quit buttons."""
    total_money = load_money()
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

def death_screen(screen, screen_width, screen_height, score, money, total_money):
    """Display the death screen with replay and home options."""
    total_money += money  # Add earned money to total
    save_money(total_money)  # Save total money

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

def lottery_screen(screen, screen_width, screen_height, total_money):
    """Display the lottery screen."""
    title_font = pygame.font.Font(None, 72)
    button_font = pygame.font.Font(None, 48)
    text_font = pygame.font.Font(None, 36)

    lottery_surface = title_font.render("LOTTERY", True, (255, 255, 255))
    money_surface = text_font.render(f"Total Money: {total_money}", True, (255, 255, 255))

    # Define different lottery options
    lottery_options = [
        {"cost": 10, "description": "Small Gun Upgrade", "chance": 0.3},
        {"cost": 50, "description": "Medium Gun Upgrade", "chance": 0.1},
        {"cost": 100, "description": "Legendary Gun Skin", "chance": 0.05}
    ]

    button_rects = []
    option_surfaces = []
    for i, option in enumerate(lottery_options):
        button_rect = pygame.Rect((screen_width // 2 - 200, screen_height // 2 + i * 100), (400, 50))
        option_surface = text_font.render(f"{option['description']} - Cost: {option['cost']}", True, (0, 0, 0))
        button_rects.append(button_rect)
        option_surfaces.append(option_surface)

    home_button_rect = pygame.Rect((screen_width // 2 - 100, screen_height - 100), (200, 50))
    home_surface = button_font.render("HOME", True, (0, 0, 0))

    running = True
    while running:
        screen.fill((0, 0, 0))
        screen.blit(lottery_surface, (screen_width // 2 - lottery_surface.get_width() // 2, screen_height // 2 - 250))
        screen.blit(money_surface, (10, 10))

        for i, (button_rect, option_surface) in enumerate(zip(button_rects, option_surfaces)):
            pygame.draw.rect(screen, (128, 128, 128), button_rect)
            screen.blit(option_surface, (button_rect.x + 20, button_rect.y + 10))

        pygame.draw.rect(screen, (128, 128, 128), home_button_rect)
        screen.blit(home_surface, (home_button_rect.x + 70, home_button_rect.y + 10))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return total_money, 'quit'
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if home_button_rect.collidepoint(event.pos):
                    return total_money, 'home'
                
                for i, button_rect in enumerate(button_rects):
                    if button_rect.collidepoint(event.pos):
                        option = lottery_options[i]
                        if total_money >= option['cost']:
                            total_money -= option['cost']
                            win = random.random() < option['chance']
                            if win:
                                # TODO: Implement actual upgrade logic
                                print(f"Won {option['description']}!")
                            save_money(total_money)

        pygame.display.flip()
        pygame.time.Clock().tick(60)