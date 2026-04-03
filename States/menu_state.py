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

        self.knfortsett = knapp(310, 275, 380, 105)
        self.knstopp = knapp(310, 440, 380, 105)
        

    def handle_events(self, events : list[pygame.event.Event]):
        for event in events:

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: #Venstre mus knapp er 1
                if self.knstopp.sjekk_klikk(event.pos):
                    self.next_state = None
                    self.done = True

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: #Venstre mus knapp er 1 
                if self.knfortsett.sjekk_klikk(event.pos):
                    self.next_state = "GAME"
                    self.done = True

    def update(self, dt: float):
        pass

    def draw(self, surface: pygame.Surface):
        surface.blit(self.image, (0, 0))

        self.knfortsett.draw(surface)
        self.knstopp.draw(surface)
         
        
        self.draw_text(surface, "Welcome! to the game Trykk SPACE for å starte.", self.font, (255, 255, 255), (500, 400))

class knapp():
    def __init__(self, x, y, width, height, tykkelse = 2):
        self.rect = pygame.Rect(x, y, width, height, )
        self.farge = (255, 0, 0)
        self.tykkelse = tykkelse

    
    def draw(self, surface):
         pygame.draw.rect(surface, self.farge, self.rect, self.tykkelse)
    
    def sjekk_klikk(self,mouse_pos):
        return self.rect.collidepoint(mouse_pos)