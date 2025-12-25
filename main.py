import pygame
from constants import *
from logger import log_event, log_state
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot
from powerup import PowerUp
from screens import *
import sys
import random

title_screen(screen)
def main():
    pygame.init()
    clock = pygame.time.Clock()
    dt = 0
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    font = pygame.font.SysFont(None, 36)
    score = 0
    lives = PLAYER_LIVES
    next_extra_life_score = 10000
    

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    powerups = pygame.sprite.Group()

    PowerUp.containers = (powerups, updatable, drawable)
    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable,)
    Shot.containers = (shots, updatable, drawable)

    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    asteroid_field = AsteroidField()

    
    
    

    
    while True:
        log_state()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            
                pause_result = pause_menu(screen)
                if pause_result == "title":
                    title_screen(screen)
                    return  

        updatable.update(dt)

        if random.random() < 0.011:  # Power up Spawn Chance
            x = random.randint(50, SCREEN_WIDTH - 50)
            y = random.randint(50, SCREEN_HEIGHT - 50)
            PowerUp(x, y)
        
        collision_happened = False

        for asteroid in asteroids.copy():
            for shot in shots.copy():
                if asteroid.collides_with(shot):
                    log_event("asteroid_shot")
                    score += SCORE_ASTEROID_HIT
                    if score >= next_extra_life_score and lives < MAX_LIVES:
                        lives += 1
                        next_extra_life_score += 10000

                    if asteroid.radius > ASTEROID_MIN_RADIUS:
                        score += SCORE_ASTEROID_SPLIT

                    shot.kill()
                    asteroid.split()

                    collision_happened = True
                    break

            if collision_happened:
                break

        if collision_happened:
            continue

        for asteroid in asteroids:
            if player.collides_with(asteroid):
                if player.invincible_timer <= 0:
            
                    log_event("player_hit")
                    lives -= 1
                    player.shots_per_fire = 1
                    player.shoot_speed_multiplier = 1

                    if lives <= 0:
                        result = game_over_screen(screen, score)
                        if result == "restart":
                            main()  
                        elif result == "title":
                            title_screen(screen) 
                            main()  

                    player.position = pygame.Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
                    player.velocity = pygame.Vector2(0, 0)

                    player.invincible_timer = PLAYER_INVINCIBILITY_SECONDS

                break  

        for powerup in powerups.copy():
            if player.position.distance_to(powerup.position) < 20: 
                if powerup.type == "fast_shoot":
                    player.shoot_speed_multiplier = min(player.shoot_speed_multiplier + 1, player.max_shoot_speed_multiplier)
                elif powerup.type == "double_shot":
                    player.shots_per_fire = min(player.shots_per_fire + 1, player.max_shots)
                    
                powerup.kill()    

        screen.fill("black")

        for obj in drawable:
            obj.draw(screen)


        lives_label = font.render("Lives:", True, "white")
        screen.blit(lives_label, (10, 10))
        for i in range(lives):
    
            x_offset = 100 + i * 25  
            y_offset = 20
            mini_pos = pygame.Vector2(x_offset, y_offset)
            mini_tri = player.mini_triangle(mini_pos)
            pygame.draw.polygon(screen, "white", mini_tri, LINE_WIDTH)

        score_surface = font.render(f"Score: {score}", True, "white")
        score_rect = score_surface.get_rect()
        score_rect.centerx = SCREEN_WIDTH // 2  
        score_rect.top = 10                     
        screen.blit(score_surface, score_rect)
        pygame.display.flip()

        dt = clock.tick(60) / 1000


if __name__ == "__main__":
    main()
