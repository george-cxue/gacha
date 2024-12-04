import pygame
import random
import math

## Player and Enemies ##

# pygame.image.load('image_file.png')


class Player(pygame.sprite.Sprite):
    def __init__(self, screen_width, screen_height):
        super().__init__()
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.image = pygame.image.load("assets/images/transparentFinal.png")
        self.image = pygame.transform.scale(self.image, (50, 90))
        # self.image.fill((255, 255, 255))
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


class Enemy(pygame.sprite.Sprite):
    def __init__(self, screen_width, screen_height, player):
        super().__init__()
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.player = player
        self.image = pygame.image.load("assets/images/owlTransparent.png")
        self.image = pygame.transform.scale(self.image, (60, 60))
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


## Guns and Bullets ##


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction, screen_width, screen_height, gunshot_sound):
        super().__init__()
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.image = pygame.Surface((5, 5))
        self.image.fill((0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 10
        self.direction = direction
        gunshot_sound.play()

    def update(self):
        self.rect.x += self.direction[0] * self.speed
        self.rect.y += self.direction[1] * self.speed
        # Remove bullet if it goes off-screen
        if not pygame.Rect(0, 0, self.screen_width, self.screen_height).colliderect(
            self.rect
        ):
            self.kill()


class Gun:
    def __init__(self, name, shoot_pattern):
        self.name = name
        self.shoot_pattern = shoot_pattern


class Pistol:
    def shoot(
        self,
        x,
        y,
        direction,
        screen_width,
        screen_height,
        gunshot_sound,
        bullets_group,
        all_sprites,
    ):
        bullet = Bullet(x, y, direction, screen_width, screen_height, gunshot_sound)
        all_sprites.add(bullet)
        bullets_group.add(bullet)


class TwoPumpGun:
    def shoot(
        self,
        x,
        y,
        direction,
        screen_width,
        screen_height,
        gunshot_sound,
        bullets_group,
        all_sprites,
    ):
        spread_angle = 15  # degrees
        rotation_matrix_positive = pygame.math.Vector2(
            math.cos(math.radians(spread_angle)), math.sin(math.radians(spread_angle))
        )
        rotation_matrix_negative = pygame.math.Vector2(
            math.cos(math.radians(-spread_angle)), math.sin(math.radians(-spread_angle))
        )

        bullet1_direction = direction
        bullet2_direction = pygame.math.Vector2(
            direction.x * rotation_matrix_positive.x
            - direction.y * rotation_matrix_positive.y,
            direction.x * rotation_matrix_positive.y
            + direction.y * rotation_matrix_positive.x,
        )

        bullet1 = Bullet(
            x, y, bullet1_direction, screen_width, screen_height, gunshot_sound
        )
        bullet2 = Bullet(
            x, y, bullet2_direction, screen_width, screen_height, gunshot_sound
        )

        all_sprites.add(bullet1, bullet2)
        bullets_group.add(bullet1, bullet2)


class ShotgunGun:
    def shoot(
        self,
        x,
        y,
        direction,
        screen_width,
        screen_height,
        gunshot_sound,
        bullets_group,
        all_sprites,
    ):
        # Shoots 8 bullets in different directions
        spread_angles = [-30, -22.5, -15, -7.5, 0, 7.5, 15, 22.5, 30]

        for angle in spread_angles:
            rotated_direction = pygame.math.Vector2(
                direction.x * math.cos(math.radians(angle))
                - direction.y * math.sin(math.radians(angle)),
                direction.x * math.sin(math.radians(angle))
                + direction.y * math.cos(math.radians(angle)),
            )

            bullet = Bullet(
                x, y, rotated_direction, screen_width, screen_height, gunshot_sound
            )
            all_sprites.add(bullet)
            bullets_group.add(bullet)


class MinugunGun:
    def __init__(self):
        self.last_shot_time = 0
        self.shot_cooldown = 100  # Milliseconds between shots

    def shoot(
        self,
        x,
        y,
        direction,
        screen_width,
        screen_height,
        gunshot_sound,
        bullets_group,
        all_sprites,
    ):
        current_time = pygame.time.get_ticks()

        # Check if enough time has passed since last shot
        if current_time - self.last_shot_time >= self.shot_cooldown:
            self.last_shot_time = current_time

            # Rapid fire, shoots 3-5 bullets in a very tight spread
            num_bullets = random.randint(3, 5)

            for _ in range(num_bullets):
                tiny_spread = random.uniform(-3, 3)
                rotated_direction = pygame.math.Vector2(
                    direction.x * math.cos(math.radians(tiny_spread))
                    - direction.y * math.sin(math.radians(tiny_spread)),
                    direction.x * math.sin(math.radians(tiny_spread))
                    + direction.y * math.cos(math.radians(tiny_spread)),
                )

                bullet = Bullet(
                    x, y, rotated_direction, screen_width, screen_height, gunshot_sound
                )
                all_sprites.add(bullet)
                bullets_group.add(bullet)
