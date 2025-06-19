import pygame
from constants import *
from circleshape import CircleShape

class Shot(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, SHOT_RADIUS)

    def draw(self, screen):
        radius = int(self.radius)
        surface_size = radius * 4
        surface = pygame.Surface((surface_size, surface_size), pygame.SRCALPHA)

        center = surface_size // 2

        for i in range(3, 0, -1):
            glow_radius = radius + i * 2
            alpha = 30 * i
            pygame.draw.circle(
                surface,
                (255, 0, 255, alpha),
                (center, center),
                glow_radius
            )

        pygame.draw.circle(surface, (255, 0, 255), (center, center), radius)
        screen.blit(surface, self.position - pygame.Vector2(center))

    def update(self, dt):
        self.position += self.velocity * dt