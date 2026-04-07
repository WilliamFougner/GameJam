from states.base_state import BaseState
import pygame

class WelcomeState(BaseState):
    def __init__(self):
        super().__init__()
        self.font_big = pygame.font.SysFont("Arial", 50)
        self.font_small = pygame.font.SysFont("Arial", 24)

        # 🖼️ Bakgrunnsbilde
        self.background = pygame.image.load("assets/kratos.jpg").convert()
        self.background = pygame.transform.scale(self.background, (1000, 600))

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self.next_state = None
                self.done = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.next_state = "MENU"
                    self.done = True

    def update(self, dt):
        pass

    def draw(self, surface):
        surface.blit(self.background, (0, 0))


        overlay = pygame.Surface((1000, 600))
        overlay.set_alpha(120)
        overlay.fill((0, 0, 0))
        surface.blit(overlay, (0, 0))


        self.draw_text(surface, "VELKOMMEN!", self.font_big, (255,255,255), (500, 150))

        self.draw_text(
            surface,
            "Målet er å ødelegge fiendens base.",
            self.font_small,
            (255,255,255),
            (500, 300)
        )

        self.draw_text(
            surface,
            "Klikk for å spawn soldater.",
            self.font_small,
            (255,255,255),
            (500, 340)
        )

        self.draw_text(
            surface,
            "Trykk SPACE for å starte",
            self.font_small,
            (200,200,200),
            (500, 450)
        )