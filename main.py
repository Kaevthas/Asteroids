import sys
import pygame
from constants import *
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot
from explosion import Explosion

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    explosions = pygame.sprite.Group()

    Asteroid.containers = (asteroids, updatable, drawable)
    Shot.containers = (shots, updatable, drawable)
    AsteroidField.containers = (updatable)
    asteroid_field = AsteroidField()
    Explosion.containers = (explosions, updatable, drawable)
    Player.containers = (updatable, drawable)

    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    dt = 0

    score = 0
    font = pygame.font.Font(None, 36)

    lives = 3
    invincible = False
    invincibility_time = 2
    invincibility_timer = 0
    blink = False
    blink_timer = 0

    # Game loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        updatable.update(dt)

        for asteroid in asteroids:
            if not invincible and asteroid.collides_with(player):
                asteroid.kill()
                lives -= 1

                if lives > 0:
                    player.respawn()
                    invincible = True
                    invincibility_timer = invincibility_time
                    blink_timer = 0
                    blink = True
                else:
                    print("Game Over! Final Score:", score)
                    sys.exit()
                break

            for shot in shots:
                if asteroid.collides_with(shot):
                    Explosion(shot.position)
                    asteroid.split()
                    shot.kill()
                    score += int(100 * (asteroid.radius / ASTEROID_MIN_RADIUS))
                    
        screen.fill("black")

        score_surface = font.render(f"Score: {score}", True, pygame.Color("white"))
        screen.blit(score_surface, (10, 10))

        lives_surface = font.render(f"Lives: {lives}", True, pygame.Color("white"))
        screen.blit(lives_surface, (10, 50))
        
        for obj in drawable:
            if isinstance(obj, Player):
                if not (invincible and not blink):
                    obj.draw(screen)
            else:
                obj.draw(screen)

        pygame.display.flip()

        # Limit the framerate to 60 FPS
        dt = clock.tick(60) / 1000

        if invincible:
            invincibility_timer -= dt
            blink_timer += dt

            if blink_timer >= 0.1:
                blink = not blink
                blink_timer = 0

            if invincibility_timer <= 0:
                invincible = False
                blink = False


if __name__ == "__main__":
    main()