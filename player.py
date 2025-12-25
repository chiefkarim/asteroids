import pygame
from circleshape import CircleShape
from constants import (
    PLAYER_RADIUS,
    LINE_WIDTH,
    PLAYER_SHOOT_COOLDOWN_SECONDS,
    PLAYER_SHOT_SPEED,
    PLAYER_SPEED,
    PLAYER_TURN_SPEED,
    SHOT_RADIUS,
)
from shot import Shot


class Player(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.cool_down = 0

    def triangel(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]

    def draw(self, screen):
        pygame.draw.polygon(screen, "white", self.triangel(), LINE_WIDTH)

    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt

    def update(self, dt):
        self.cool_down -= dt
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            self.rotate(dt * -1)

        if keys[pygame.K_d]:
            self.rotate(dt)

        if keys[pygame.K_w]:
            self.move(dt)

        if keys[pygame.K_s]:
            self.move(dt * -1)

        if keys[pygame.K_SPACE]:
            self.shot()

    def move(self, dt):
        unite_vector = pygame.Vector2(0, 1)
        rotated_vector = unite_vector.rotate(self.rotation)
        speed_vector = rotated_vector * PLAYER_SPEED * dt
        self.position += speed_vector

    def shot(self):
        if not self.cool_down > 0:
            shot = Shot(self.triangel()[0], self.triangel()[1], SHOT_RADIUS)
            direction = pygame.Vector2(0, 1).rotate(self.rotation)
            shot.velocity = direction * PLAYER_SHOT_SPEED
            self.cool_down = PLAYER_SHOOT_COOLDOWN_SECONDS
