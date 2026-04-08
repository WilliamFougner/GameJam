from states.base_state import BaseState
import pygame

class WelcomeState(BaseState):
    def __init__(self):
        super().__init__()
        self.font_big = pygame.font.SysFont("Arial", 50)
        self.font_small = pygame.font.SysFont("Arial", 24)


        self.background = pygame.image.load("assets/kratos.jpg").convert()
        self.background = pygame.transform.scale(self.background, (1500, 800))

    def on_enter(self):
        pygame.mixer.music.load("assets/gamestate_music.mp3")
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.5)
        
    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self.next_state = None
                self.done = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.next_state = "GAME"
                    self.done = True

    def update(self, dt):
        pass

    def draw(self, surface):
        surface.blit(self.background, (0, 0))


        overlay = pygame.Surface((1500, 800))
        overlay.set_alpha(120)
        overlay.fill((0, 0, 0))
        surface.blit(overlay, (0, 0))


        self.draw_text(surface, "VELKOMMEN!", self.font_big, (255,255,255), (750, 150))

        self.draw_text(
            surface,
            "Målet er å ødelegge fiendens base.",
            self.font_small,
            (255,255,255),
            (750, 400)
        )

        self.draw_text(
            surface,
            "Klikk for å spawn soldater.",
            self.font_small,
            (255,255,255),
            (750, 500)
        )

        self.draw_text(
            surface,
            "Trykk SPACE for å starte",
            self.font_small,
            (200,200,200),
            (750, 570)
        )