import pygame
from circleshape import CircleShape
from constants import *
from shot import Shot

class Player(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 180
        self.shoot_cooldown = 0.15
        self.time_since_last_shot = 0

        original_image = pygame.image.load("assets/spaceship.png").convert_alpha()
        scale = (PLAYER_RADIUS * 2, PLAYER_RADIUS * 2)
        original_image = pygame.transform.smoothscale(original_image, scale)
        original_image = pygame.transform.rotate(original_image, 180)
        self.original_image = original_image
        self.image = self.original_image

    def draw(self, screen):
        rotated_image = pygame.transform.rotate(self.original_image, -self.rotation)
        rect = rotated_image.get_rect(center=self.position)
        screen.blit(rotated_image, rect.topleft)
              
    def update(self, dt):
        self.time_since_last_shot += dt

        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            self.rotate(-dt)
        if keys[pygame.K_d]:
            self.rotate(dt)
        if keys[pygame.K_w]:
            self.move(dt)
        if keys[pygame.K_s]:
            self.move(-dt)
        if keys[pygame.K_SPACE] and self.time_since_last_shot >= self.shoot_cooldown:
            self.shoot()
            self.time_since_last_shot = 0

    def shoot(self):
        shot = Shot(self.position.x, self.position.y)
        shot.velocity = pygame.Vector2(0, 1).rotate(self.rotation) * PLAYER_SHOOT_SPEED

    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt

    def move(self, dt):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        self.position += forward * PLAYER_SPEED * dt

    def respawn(self):
        self.position = pygame.Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        self.velocity = pygame.Vector2(0, 0)
        self.rotation = 180