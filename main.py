import sys
import pygame
from constants import *
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    Asteroid.containers = (asteroids, updatable, drawable)
    Shot.containers = (shots, updatable, drawable)
    AsteroidField.containers = (updatable)
    asteroid_field = AsteroidField()

    Player.containers = (updatable, drawable)

    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    dt = 0

    score = 0
    font = pygame.font.Font(None, 36)

    lives = 3

    # Game loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        updatable.update(dt)

        for asteroid in asteroids:
            if asteroid.collides_with(player):
                asteroid.kill()
                lives -= 1
                if lives > -0:
                    player.respawn()
                else:
                    print("Game Over! Final Score:", score)
                    sys.exit()

            for shot in shots:
                if asteroid.collides_with(shot):
                    shot.kill()
                    asteroid.split()
                    score += int(100 * (asteroid.radius / ASTEROID_MIN_RADIUS))
                    
        screen.fill("black")

        score_surface = font.render(f"Score: {score}", True, pygame.Color("white"))
        screen.blit(score_surface, (10, 10))

        lives_surface = font.render(f"Lives: {lives}", True, pygame.Color("white"))
        screen.blit(lives_surface, (10, 50))
        
        for obj in drawable:
            obj.draw(screen)

        pygame.display.flip()

        # Limit the framerate to 60 FPS
        dt = clock.tick(60) / 1000


if __name__ == "__main__":
    main()