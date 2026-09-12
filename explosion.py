import random

import pygame

from constants import PARTICAL_LIFETIME


class Explosion(pygame.sprite.Sprite):
    containers: tuple[pygame.sprite.Group, ...]

    def __init__(self, x: float, y: float, radius: float):
        if hasattr(self, "containers"):
            super().__init__(*self.containers)
        else:
            super().__init__()
        self.position = pygame.Vector2(x, y)
        self.lifetime = PARTICAL_LIFETIME
        self.max_lifetime = self.lifetime
        self.shockwave_radius = max(radius * 0.25, 2)
        self.shockwave_max_radius = max(radius * 2.5, 10)
        self.particles = []
        self.radius = radius
        particle_count = max(12, int(radius * 1.5))

        for _ in range(particle_count):
            direction = pygame.Vector2(
                random.uniform(-1.0, 1.0),
                random.uniform(-1.0, 1.0),
            )

            if direction.length_squared() == 0:
                direction = pygame.Vector2(1, 0)

            direction = direction.normalize()

            self.particles.append(
                {
                    "position": self.position.copy(),
                    "velocity": direction * random.uniform(60, 220),
                    "lifetime": random.uniform(0.25, PARTICAL_LIFETIME),
                    "max_lifetime": PARTICAL_LIFETIME,
                    "size": random.uniform(1.5, 4.0),
                }
            )

    def update(self, dt: float):
        self.lifetime -= dt

        for particle in self.particles:
            particle["position"] += particle["velocity"] * dt
            particle["velocity"] *= 0.94 ** (dt * 60)
            particle["lifetime"] -= dt
        progress = 1.0 - max(self.lifetime, 0) / self.max_lifetime
        self.shockwave_radius = (
            max(self.radius * 0.25, 2)
            + (self.shockwave_max_radius - max(self.radius * 0.25, 2)) * progress
        )

        if self.lifetime <= 0:
            self.kill()

    def draw(self, screen: pygame.Surface):
        for particle in self.particles:
            if particle["lifetime"] <= 0:
                continue

            alpha = int(
                255
                * max(
                    0,
                    particle["lifetime"] / particle["max_lifetime"],
                )
            )

            size = int(particle["size"] * 2 + 2)
            surface = pygame.Surface(
                (size, size),
                pygame.SRCALPHA,
            )

            pygame.draw.circle(
                surface,
                (255, 180, 50, alpha),
                (size // 2, size // 2),
                particle["size"],
            )

            screen.blit(
                surface,
                (
                    particle["position"].x - size / 2,
                    particle["position"].y - size / 2,
                ),
            )

        shockwave_alpha = int(180 * max(self.lifetime, 0) / self.max_lifetime)

        if shockwave_alpha > 0:
            pygame.draw.circle(
                screen,
                (255, 220, 100),
                self.position,
                int(self.shockwave_radius),
                width=2,
            )
