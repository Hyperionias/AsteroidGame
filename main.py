import sys
import pygame
from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from logger import log_state, log_event
from player import Player
from shot import Shot
from asteroid import Asteroid
from asteroidField import AsteroidField


def main():
    pygame.init()
    clock = pygame.time.Clock()
    dt = 0.0

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()

    AsteroidField.containers = (updatable,)
    Asteroid.containers = (asteroids, updatable, drawable)
    Player.containers = (updatable, drawable)
    Shot.containers = (shots, updatable, drawable)

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    asteroid_field = AsteroidField()

    print("Starting Asteroids...")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")

    while True:
        log_state()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        # 1. Update adımı
        updatable.update(dt)

        # 2. Çarpışma kontrolü
        for asteroid in asteroids:
            # Asteroid vs Players
            if asteroid.collides_with(player):
                log_event("player_hit")
                print("Game over!")
                sys.exit()

            # Asteroid vs Shots
            for shot in shots:
                if asteroid.collides_with(shot):
                    log_event("asteroid_shot")
                    shot.kill()
                    asteroid.split()

        # 3. Çizim adımı
        screen.fill("black")
        for obj in drawable:
            obj.draw(screen)
        pygame.display.flip()

        dt = clock.tick(60) / 1000


if __name__ == "__main__":
    main()
