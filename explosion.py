import pygame
import random
import math

class Explosion(pygame.sprite.Sprite):
    def __init__(self, position, num_particles=20):
        if hasattr(self, "containers"):
            super().__init__(self.containers)
        else:
            super().__init__()
        self.position = pygame.Vector2(position)
        self.lifetime = 0.5
        self.age = 0

        self.particles = []
        for _ in range(num_particles):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(30, 100)
            velocity = pygame.Vector2(math.cos(angle), math.sin(angle)) * speed
            radius = random.uniform(3, 16)
            color = random.choice(["orange", "red", "yellow", "white"])
            self.particles.append({
                "pos": pygame.Vector2(self.position),
                "vel": velocity,
                "age": 0,
                "radius": radius,
                "color": color
            })

    def update(self, dt):
        self.age += dt
        if self.age > self.lifetime:
            self.kill()
            return
        
        for particle in self.particles:
            particle["pos"] += particle["vel"] * dt
            particle["radius"] = max(0, particle["radius"] - dt * 5)

    def draw(self, screen):
        for particle in self.particles:
            if particle["radius"] > 0:
                pygame.draw.circle(screen, particle["color"], particle["pos"], int(particle["radius"]))

