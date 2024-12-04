import pygame
import random
import json
import os
from sprites import Pistol, TwoPumpGun, ShotgunGun, MinugunGun

pygame.mixer.init()
click = pygame.mixer.Sound("assets/sound_effects/clickSound.wav")

titleScreen = pygame.image.load("assets/images/titleScreen.jpg")
test = pygame.image.load("assets/images/playButtonTransparent.png")
test = pygame.transform.scale(test, (200, 70))

lotteryButton = pygame.image.load("assets/images/lotteryButtonTransparent.png")
lotteryButton = pygame.transform.scale(lotteryButton, (200, 70))

quitButton = pygame.image.load("assets/images/quitButtonTransparent.png")
quitButton = pygame.transform.scale(quitButton, (200, 70))

lotteryScreen = pygame.image.load("assets/images/gunLotteryScreen.jpg")

drawGunButton = pygame.image.load("assets/images/drawGunButton.png")
drawGunButton = pygame.transform.scale(drawGunButton, (200, 70))

homeButton = pygame.image.load("assets/images/homeButton.png")
homeButton = pygame.transform.scale(homeButton, (200, 70))

gameOverScreen = pygame.image.load("assets/images/gameOverScreen.jpg")

replayButton = pygame.image.load("assets/images/replayButton.png")
replayButton = pygame.transform.scale(replayButton, (200, 70))


def get_gun_from_name(gun_name):
    gun_map = {
        "TwoPumpGun": TwoPumpGun(),
        "ShotgunGun": ShotgunGun(),
        "MinugunGun": MinugunGun(),
    }
    return gun_map.get(gun_name, Pistol())


def load_game_data():
    if os.path.exists("save_data.json"):
        with open("save_data.json", "r") as f:
            data = json.load(f)
            return {
                "total_money": data.get("total_money", 0),
                "current_gun": get_gun_from_name(data.get("current_gun", "TwoPumpGun")),
            }
    return {"total_money": 0, "current_gun": TwoPumpGun()}


def save_game_data(total_money, current_gun):
    with open("save_data.json", "w") as f:
        json.dump(
            {"total_money": total_money, "current_gun": current_gun.__class__.__name__},
            f,
        )


def get_random_gun():
    guns = [
        {"type": TwoPumpGun(), "probability": 0.7},
        {"type": ShotgunGun(), "probability": 0.2},
        {"type": MinugunGun(), "probability": 0.1},
    ]

    random_val = random.random()
    cumulative_prob = 0

    for gun in guns:
        cumulative_prob += gun["probability"]
        if random_val <= cumulative_prob:
            return gun["type"]

    return guns[0]["type"]


def start_screen(screen, screen_width, screen_height, click_sound):
    total_money = load_game_data()["total_money"]
    button_font = pygame.font.Font(None, 48)

    # Define button rectangles

    lottery_button_rect = pygame.Rect(
        (screen_width // 2 - 100, screen_height // 3 + 150), (200, 50)
    )
    quit_button_rect = pygame.Rect(
        (screen_width // 2 - 100, screen_height // 3 + 250), (200, 50)
    )
    test_image_rect = pygame.Rect(
        (screen_width // 2 - 100, screen_height // 3 + 50), (200, 50)
    )
    money_surface = button_font.render(f"Money: {total_money}", True, (0, 0, 0))

    running = True
    while running:
        screen.blit(titleScreen, (0, 0))
        screen.blit(money_surface, (10, 10))

        # Draw buttons
        screen.blit(test, (test_image_rect.x, test_image_rect.y))
        screen.blit(lotteryButton, (lottery_button_rect.x, lottery_button_rect.y))
        screen.blit(quitButton, (quit_button_rect.x, quit_button_rect.y))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if test_image_rect.collidepoint(
                    event.pos
                ):  # Check if test image is clicked
                    click_sound.play()
                    return "play"
                elif lottery_button_rect.collidepoint(event.pos):
                    click_sound.play()
                    return "lottery"
                elif quit_button_rect.collidepoint(event.pos):
                    click_sound.play()
                    return "quit"

        pygame.display.flip()
        pygame.time.Clock().tick(60)


def death_screen(
    screen, screen_width, screen_height, score, money, total_money, current_gun
):
    total_money += money  # Add earned money to total
    save_game_data(total_money, current_gun)  # Save total money

    button_font = pygame.font.Font(None, 48)

    score_surface = button_font.render(f"Final Score: {score}", True, (0, 0, 0))
    money_surface = button_font.render(f"Money Earned: {money}", True, (0, 0, 0))
    total_money_surface = button_font.render(
        f"Total Money: {total_money}", True, (0, 0, 0)
    )

    replay_button_rect = pygame.Rect(
        (screen_width // 2 - 100, screen_height // 2 + 100), (300, 50)
    )
    home_button_rect = pygame.Rect(
        (screen_width // 2 - 100, screen_height // 2 + 200), (300, 50)
    )

    replay_surface = button_font.render("REPLAY", True, (0, 0, 0))
    home_surface = button_font.render("HOME SCREEN", True, (0, 0, 0))

    running = True
    while running:
        screen.blit(gameOverScreen, (0, 0))
        screen.blit(
            score_surface,
            (
                screen_width // 2 - score_surface.get_width() // 2,
                screen_height // 2 - 100,
            ),
        )
        screen.blit(
            money_surface,
            (
                screen_width // 2 - money_surface.get_width() // 2,
                screen_height // 2 - 50,
            ),
        )
        screen.blit(
            total_money_surface,
            (
                screen_width // 2 - total_money_surface.get_width() // 2,
                screen_height // 2,
            ),
        )

        # pygame.draw.rect(screen, (128, 128, 128), replay_button_rect)
        # screen.blit(replay_surface, (replay_button_rect.x + 100, replay_button_rect.y + 10))
        screen.blit(replayButton, (replay_button_rect.x, replay_button_rect.y))
        screen.blit(homeButton, (home_button_rect.x, home_button_rect.y))
        # pygame.draw.rect(screen, (128, 128, 128), home_button_rect)
        # screen.blit(home_surface, (home_button_rect.x + 70, home_button_rect.y + 10))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                click.play()
                return "quit"
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if replay_button_rect.collidepoint(event.pos):
                    click.play()
                    return "play"
                elif home_button_rect.collidepoint(event.pos):
                    click.play()
                    return "home"

        pygame.display.flip()
        pygame.time.Clock().tick(60)


def lottery_screen(screen, screen_width, screen_height, total_money, current_gun):
    button_font = pygame.font.Font(None, 48)
    text_font = pygame.font.Font(None, 36)

    money_surface = text_font.render(
        f"Total Money: {total_money}", True, (255, 255, 255)
    )
    current_gun_surface = text_font.render(
        f"Current Gun: {current_gun.__class__.__name__}", True, (255, 255, 255)
    )

    # Lottery draw button
    draw_button_rect = pygame.Rect(
        (screen_width // 2 - 100, screen_height // 2), (200, 70)
    )
    home_button_rect = pygame.Rect(
        (screen_width // 2 - 100, screen_height - 100), (200, 70)
    )

    new_gun_surface = None

    running = True
    while running:
        screen.blit(lotteryScreen, (0, 0))
        # Update money display every frame
        money_surface = text_font.render(
            f"Total Money: {total_money}", True, (255, 255, 255)
        )
        current_gun_surface = text_font.render(
            f"Current Gun: {current_gun.__class__.__name__}", True, (255, 255, 255)
        )

        screen.blit(money_surface, (10, 10))
        screen.blit(current_gun_surface, (10, 50))

        screen.blit(drawGunButton, (draw_button_rect.x, draw_button_rect.y))
        screen.blit(homeButton, (home_button_rect.x, home_button_rect.y))

        # Display new gun if drawn
        if new_gun_surface:
            screen.blit(
                new_gun_surface,
                (
                    screen_width // 2 - new_gun_surface.get_width() // 2,
                    screen_height // 2 + 100,
                ),
            )

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                click.play()
                return total_money, current_gun, "quit"
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if home_button_rect.collidepoint(event.pos):
                    click.play()
                    return total_money, current_gun, "home"

                if draw_button_rect.collidepoint(event.pos):
                    click.play()
                    if total_money >= 50:
                        total_money -= 50
                        drawn_gun = get_random_gun()
                        new_gun_surface = text_font.render(
                            f"You drew: {drawn_gun.__class__.__name__}!",
                            True,
                            (0, 0, 0),
                        )
                        current_gun = drawn_gun
                        save_game_data(total_money, current_gun)

        pygame.display.flip()
        pygame.time.Clock().tick(60)
