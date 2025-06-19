import pygame
import random
import math
from circleshape import CircleShape
from constants import *

class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        self.points = self.generate_lumpy_shape(radius)

    def generate_lumpy_shape(self, radius):
        points = []
        num_points = random.randint(10, 16)
        for i in range(num_points):
            angle = (math.pi * 2) * (i / num_points)
            offset = random.uniform(0.8, 1.2)
            r = radius * offset
            x = math.cos(angle) * r
            y = math.sin(angle) * r
            points.append(pygame.Vector2(x, y))
        return points
        
    def draw(self, screen):
        transformed = [self.position + point for point in self.points]
        pygame.draw.polygon(screen, (100, 100, 100), transformed)
        pygame.draw.polygon(screen, "white", transformed, 2)

    def update(self, dt):
        self.position += self.velocity * dt

    def split(self):
        self.kill()

        if self.radius <= ASTEROID_MIN_RADIUS:
            return
        
        random_angle = random.uniform(20, 50)

        a = self.velocity.rotate(random_angle)
        b = self.velocity.rotate(-random_angle)

        new_radius = self.radius - ASTEROID_MIN_RADIUS
        asteroid = Asteroid(self.position.x, self.position.y, new_radius)
        asteroid.velocity = a * 1.2
        asteroid = Asteroid(self.position.x, self.position.y, new_radius)
        asteroid.velocity = b * 1.2
