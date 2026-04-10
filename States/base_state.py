"""
En abstrakt klasse for states.

Har lagt til tegnefunksjonalitet som alle States har tilgang til. Her kan du legge til generell funksjonalitet for alle states.
"""

import pygame # For å få autocomplete og typer.
from abc import ABC, abstractmethod # For å lage en abstrakt klasse. Alle states må arve fra denne klassen.

class BaseState(ABC):
    """En abstrakt klasse for states. Alle states må arve fra denne klassen.
    
    Attributter:
        next_state (str): String-navnet til neste state i states-ordboken.
        done (bool): Om staten er ferdig og skal byttes ut. 
    """

    def __init__(self):
        """Initialiserer staten."""
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