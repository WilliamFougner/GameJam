from states.base_state import BaseState
import pygame

class WelcomeState(BaseState):
    def __init__(self):
        super().__init__()
        # Sett opp fonter
        self.font_big = pygame.font.SysFont("Arial", 50)
        self.font_small = pygame.font.SysFont("Arial", 24)

        # Last inn og skaler bakgrunnsbilde
        self.background = pygame.image.load("assets/kratos.jpg").convert()
        self.background = pygame.transform.scale(self.background, (1500, 800))

    def on_enter(self):
        # Spill bakgrunnsmusikk for welcome screen
        pygame.mixer.music.load("assets/gamestate_music.mp3")
        pygame.mixer.music.play(-1)  # Loop musikk
        pygame.mixer.music.set_volume(0.5)
        
    def handle_events(self, events):
        for event in events:
            # Avslutt programmet hvis brukeren lukker vinduet
            if event.type == pygame.QUIT:
                self.next_state = None
                self.done = True
            # Start spillet hvis SPACE trykkes
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.next_state = "GAME"
                    self.done = True

    def update(self, dt):
        pass  # Ingen oppdatering nødvendig på velkomstskjerm

    def draw(self, surface):
        # Tegner bakgrunn
        surface.blit(self.background, (0, 0))

        # Tegner svart overlay
        overlay = pygame.Surface((1500, 800))
        overlay.set_alpha(120)
        overlay.fill((0, 0, 0))
        surface.blit(overlay, (0, 0))

        # Tekst på skjermen
        self.draw_text(surface, "VELKOMMEN!", self.font_big, (255,255,255), (750, 150))
        self.draw_text(surface, "Målet er å ødelegge fiendens base.", self.font_small, (255,255,255), (750, 400))
        self.draw_text(surface, "Klikk for å spawn soldater.", self.font_small, (255,255,255), (750, 500))
        self.draw_text(surface, "Trykk SPACE for å starte", self.font_small, (200,200,200), (750, 570))