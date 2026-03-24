"""
Dette er staten for hovedmenyen.
"""

from states.base_state import BaseState
import pygame

class MenuState(BaseState):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("assets/settings_menu.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (1000, 600))
        self.font = pygame.font.SysFont("Arial", 24)

    def handle_events(self, events : list[pygame.event.Event]):
        for event in events:
            if event.type == pygame.QUIT:
                self.next_state = None
                self.done = True
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.next_state = "GAME"
                    self.done = True

    def update(self, dt: float):
        pass

    def draw(self, surface: pygame.Surface):
        surface.blit(self.image, (0, 0))
         
        
        self.draw_text(surface, "Welcome! to the game Trykk SPACE for å starte.", self.font, (255, 255, 255), (500, 400))