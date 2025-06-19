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
                "color": color,
                "alpha": 255
            })

    def update(self, dt):
        self.age += dt
        if self.age > self.lifetime:
            self.kill()
            return
        
        for particle in self.particles:
            particle["pos"] += particle["vel"] * dt
            particle["radius"] = max(0, particle["radius"] - dt * 5)
            particle["alpha"] = max(0, particle["alpha"] - dt * 500)

    def draw(self, screen):
        for particle in self.particles:
            if particle["radius"] > 0 and particle["alpha"] > 0:
                surface_size = int(particle["radius"] * 4)
                surface = pygame.Surface((surface_size, surface_size), pygame.SRCALPHA)

                glow_color = pygame.Color(particle["color"])
                glow_color.a = int(particle["alpha"] * 0.4)
                pygame.draw.circle(
                    surface,
                    glow_color,
                    (surface_size // 2, surface_size // 2),
                    surface_size // 2
                )

                core_color = pygame.Color(particle["color"])
                core_color.a = int(particle["alpha"])
                pygame.draw.circle(
                    surface,
                    core_color,
                    (surface_size // 2, surface_size // 2),
                    int(particle["radius"])
                )
                
                screen.blit(surface, particle["pos"] - pygame.Vector2(particle["radius"]))

