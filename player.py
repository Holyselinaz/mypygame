import constants
import pygame
from circleshape import CircleShape
from shot import Shot
from constants import *


class Player(CircleShape):
    def __init__(self, x: int, y: int):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.invincible_timer = 0

        self.shots_per_fire = 1
        self.max_shots = 5

        self.double_shot = False 
        self.shoot_speed_multiplier = 1
        self.max_shoot_speed_multiplier = 4
        self.shot_cooldown = PLAYER_SHOOT_COOLDOWN_SECONDS / self.shoot_speed_multiplier
        
               
    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]
    
    def draw(self, screen):
        if self.invincible_timer > 0:
            if int(self.invincible_timer * 10) % 2 == 0:  
                return  
        pygame.draw.polygon(
            screen,
            "white",
            self.triangle(),
            LINE_WIDTH,
        )
        
    def mini_triangle(self, position, scale=0.6):
        forward = pygame.Vector2(0, -1) * self.radius * scale
        right = pygame.Vector2(1, 0) * self.radius * scale / 1.5
        a = position + forward
        b = position - forward - right
        c = position - forward + right
        return [a, b, c]
    
    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt
        
          
    def update(self, dt):
        if self.invincible_timer > 0:
            self.invincible_timer -= dt
        if self.invincible_timer < 0:
            self.invincible_timer = 0

        if self.shot_cooldown > 0:
            self.shot_cooldown -= dt
        if self.shot_cooldown < 0:
            self.shot_cooldown = 0

        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            self.rotate(-dt)
        if keys[pygame.K_d]:
            self.rotate(dt)
        if keys[pygame.K_w]:
            self.move(dt)
        if keys[pygame.K_s]:
            self.move(-dt)
        if keys[pygame.K_SPACE]:
            self.shoot()

    def move(self, dt):
        unit_vector = pygame.Vector2(0, 1)
        rotated_vector = unit_vector.rotate(self.rotation)
        rotated_with_speed_vector = rotated_vector * PLAYER_SPEED * dt
        self.position += rotated_with_speed_vector

    def shoot(self):
        if self.shot_cooldown > 0 or Shot.containers is None:
            return
        
        direction = pygame.Vector2(0, 1).rotate(self.rotation)

        
        num_shots = self.shots_per_fire
        if num_shots == 1:
        
            shot = Shot(self.position.x, self.position.y)
            shot.velocity = direction * PLAYER_SHOOT_SPEED
        else:
        
            spacing = 10  
            total_width = spacing * (num_shots - 1)
            start_offset = -total_width / 2

            for i in range(num_shots):
                offset = pygame.Vector2(1, 0).rotate(self.rotation) * (start_offset + i * spacing)
                shot = Shot(self.position.x + offset.x, self.position.y + offset.y)
                shot.velocity = direction * PLAYER_SHOOT_SPEED
            

        self.shot_cooldown = PLAYER_SHOOT_COOLDOWN_SECONDS / self.shoot_speed_multiplier