"""
Dette er staten for spillet. Det er her du legger til Spillobjekter, logikk, etc...
"""


from states.base_state import BaseState
import pygame


class GameState(BaseState):
    def __init__(self):
        super().__init__()

    def handle_events(self, events : list[pygame.event.Event]):
        for event in events:
            if event.type == pygame.QUIT:
                self.next_state = None
                self.done = True
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.next_state = "MENU"
                    self.done = True

    def update(self, dt: float):
        pass

    def draw(self, surface: pygame.Surface):
        surface.fill((0, 0, 0))
        self.draw_text(surface, "Du er i spillet! Trykk ESC for å gå tilbake til hovedmenyen.", self.font, (255, 255, 255), (500, 400))

class Spillobjekt():
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(x - width // 2, y - height // 2, width, height)

class Spiller(Spillobjekt):
    def __init__(self, x, y):
        super().__init__(x, y, width = 10, height = 10)
        self.color = (0, 200, 0)
        self.speed = 2
        self.hp = 3

    def update(self, dt):
        self.rect = pygame.Rect(self.x - self.width // 2, self.y - self.height // 2, self.width, self.height)

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)

class Fiende(Spillobjekt):
    def __init__(self, x, y):
        super().__init__(x, y, width = 20, height = 20)
        self.color = (200, 0, 0)
        self.speed = 2
        self.hp = 3

    def update(self, dt):
        self.rect = pygame.Rect(self.x - self.width // 2, self.y - self.height // 2, self.width, self.height)

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect) 