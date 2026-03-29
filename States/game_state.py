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
        self.knapp = Knapp(700, 0, 50, 50, "assets/soldat.png") #Knapp

    def handle_events(self, events : list[pygame.event.Event]):
        for event in events:
            if event.type == pygame.QUIT:
                self.next_state = None
                self.done = True
            # Menu sjekk button ESC
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.next_state = "MENU"
                    self.done = True
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: # venstre musen
                if self.knapp.sjekk_klikk(event.pos):
                    self.spillere.append(Spiller(60, 250))
            


    def update(self, dt: float):
        #Spill karakterer
        for soldat in self.spillere:
            soldat.update(dt)
        for fiende in self.fiender:
            fiende.update(dt)

    def draw(self, surface: pygame.Surface):
        surface.fill((0, 0, 0))

        #Spill karakterer
        for soldat in self.spillere:
            soldat.draw(surface)
        for fiende in self.fiender:
            fiende.draw(surface)
        self.draw_text(surface, "SPACE = send soldat | ESC = meny", self.font, (255, 255, 255), (250, 20))

        #Send soldat_1 knapp
        self.knapp.draw(surface)


# Spill klasser

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
        self.x += self.speed
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
        self.x -= self.speed
        self.rect = pygame.Rect(self.x - self.width // 2, self.y - self.height // 2, self.width, self.height)

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)


class Knapp:
    def __init__(self, x, y , width, height, bildenavn):
        self.rect = pygame.Rect(x, y, width, height)
        self.knapp1_bilde = pygame.image.load(bildenavn).convert_alpha()
        self.knapp1_bilde = pygame.transform.scale(self.knapp1_bilde, (self.rect.width, self.rect.height))
    def draw(self, surface):
        surface.blit(self.knapp1_bilde, self.rect)
        
    
    def sjekk_klikk(self,mouse_pos):
        return self.rect.collidepoint(mouse_pos)