import pygame
from abc import ABC, abstractmethod

class BaseState(ABC):
    """Abstrakt klasse for states. Alle states må arve fra denne."""
    
    def __init__(self):
        self.done = False
        self.next_state = None
        self.font = pygame.font.SysFont(None, 20)

    def on_enter(self):
        pass  # Kan overstyres i subklasser
    
    def draw_text(self, surface : pygame.Surface, string : str, font : pygame.font.Font, color : tuple, center : tuple):
        # Lag tekst og plasser den på midten
        text = font.render(string, False, color)
        text_rect = text.get_rect(center = center)
        surface.blit(text, text_rect)

    @abstractmethod
    def handle_events(self, events : list[pygame.event.Event]):
        pass

    @abstractmethod
    def update(self, dt: float):
        pass

    @abstractmethod    
    def draw(self, surface: pygame.Surface):
        pass