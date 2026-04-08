"""
En generell spill-klasse. Dette er hovedprogrammet.
"""

import pygame
from states.base_state import BaseState
from states.menu_state import MenuState
from states.game_state import GameState
from states.welcome_state import WelcomeState
from states.victory_state import VictoryState

# legger til lydsystemet
pygame.mixer.init()

class Spill:
    def __init__(self):
        pygame.init()  # Initialiser pygame
        self.screen = pygame.display.set_mode((1500, 800))  # Oppretter vindu
        self.clock = pygame.time.Clock()  # Brukes for å holde FPS stabil
        self.running = True  # Flag for hovedløkken
        
        # Lag alle states i en ordbok
        self.states = {
            "WELCOME": WelcomeState(),
            "MENU": MenuState(),
            "GAME": GameState(),
            "VICTORY": VictoryState()
        }
        
        # Sett startstate
        self.current_state = self.states["WELCOME"]
        self.current_state.on_enter()  # Kjør on_enter-metoden for startstate

    def main_loop(self):
        # Hovedløkken kalles for hver frame
        self.handle_events()  # Håndterer input
        self.update()         # Oppdaterer logikk
        self.render()         # Tegner alt

    def handle_events(self):
        # Hent alle events fra pygame
        events = pygame.event.get()
        # La current_state håndtere events
        self.current_state.handle_events(events)

    def update(self):
        # Beregn tidsdifferanse siden forrige frame 
        dt = self.clock.tick(60) / 1000.0  # Begrenses til 60 FPS

        # Oppdater staten
        self.current_state.update(dt)

        # Sjekk om staten er ferdig
        if self.current_state.done:
            next_state = self.current_state.next_state
            self.current_state.done = False  # Reset done-flag

            if next_state:
                # Hvis vi går inn i "GAME", lages ny GameState for ny start
                if next_state == "GAME":
                    self.states["GAME"] = GameState()
                # Bytt til neste state og kjør on_enter
                self.current_state = self.states[next_state]
                self.current_state.on_enter()
            else:
                # Hvis ingen next_state, stopp spillet
                self.running = False

    def render(self):
        # Tegn alt fra staten
        self.current_state.draw(self.screen)
        pygame.display.flip()  # Oppdater skjermen

# Start spillet
spill = Spill()
while spill.running:
    spill.main_loop()  # Kjører hovedløkken