"""
Dette er staten for spillet. Det er her du legger til Spillobjekter, logikk, etc...
"""

from states.base_state import BaseState
import pygame


class GameState(BaseState):
    def __init__(self):
        super().__init__()
        self.spillere = []
        self.fiender  = []
        self.spiller_base = Base(50, 250, (0, 180, 0))
        self.fiende_base  = Base(750, 250, (180, 0, 0))

    def handle_events(self, events : list[pygame.event.Event]):
        for event in events:
            if event.type == pygame.QUIT:
                self.next_state = None
                self.done = True
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.next_state = "MENU"
                    self.done = True
                if event.key == pygame.K_SPACE:
                    self.spillere.append(Spiller(60, 250))

    def update(self, dt: float):
        for soldat in self.spillere:
            soldat.update(dt)
        for fiende in self.fiender:
            fiende.update(dt)

        # Sjekk om soldater når fiendens base
        self.spillere = [
            soldat for soldat in self.spillere
            if not soldat.rect.colliderect(self.fiende_base.rect)
        ]

        # Sjekk om fiender når spillerens base
        self.fiender = [
            fiende for fiende in self.fiender
            if not fiende.rect.colliderect(self.spiller_base.rect)
        ]

    def draw(self, surface: pygame.Surface):
        surface.fill((0, 0, 0))
        self.spiller_base.draw(surface, self.font)
        self.fiende_base.draw(surface, self.font)
        for soldat in self.spillere:
            soldat.draw(surface)
        for fiende in self.fiender:
            fiende.draw(surface)
        self.draw_text(surface, "SPACE = send soldat | ESC = meny", self.font, (255, 255, 255), (250, 20))


# ================================
# Hjelpeklasser — brukes av GameState
# ================================

class Spillobjekt():
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(x - width // 2, y - height // 2, width, height)

class Spiller(Spillobjekt):
    def __init__(self, x, y):
        super().__init__(x, y, width=10, height=10)
        self.color = (0, 200, 0)
        self.speed = 2
        self.hp = 3

    def update(self, dt):
        self.x += self.speed
        self.rect = pygame.Rect(self.x - self.width // 2, self.y - self.height // 2, self.width, self.height)

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)

class Fiende(Spillobjekt):
    def __init__(self, x, y):
        super().__init__(x, y, width=20, height=20)
        self.color = (200, 0, 0)
        self.speed = 2
        self.hp = 3

    def update(self, dt):
        self.x -= self.speed
        self.rect = pygame.Rect(self.x - self.width // 2, self.y - self.height // 2, self.width, self.height)

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)

class Base(Spillobjekt):
    def __init__(self, x, y, color):
        super().__init__(x, y, width=30, height=100)
        self.color = color
        self.hp = 10

    def draw(self, surface, font):
        pygame.draw.rect(surface, self.color, self.rect)
        hp_tekst = font.render(f"HP: {self.hp}", True, (255, 255, 255))
        surface.blit(hp_tekst, (self.rect.x, self.rect.y - 20))