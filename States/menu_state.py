from states.base_state import BaseState
import pygame

class MenuState(BaseState):
    def __init__(self):
        super().__init__()
        # Last inn og skaler meny-bakgrunn
        self.image = pygame.image.load("assets/settings_menu.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (1500, 800))
        self.font = pygame.font.SysFont("Arial", 24)

        # Definer knapper
        self.knfortsett = knapp(464, 369, 574, 136)
        self.knstopp = knapp(464, 587, 574, 136)
        
    def on_enter(self):
        # Spill meny-musikk
        pygame.mixer.music.load("assets/menu_music.mp3")
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.5)
 
    def handle_events(self, events : list[pygame.event.Event]):
        for event in events:
            # Avslutt hvis lukker vinduet
            if event.type == pygame.QUIT:
                self.next_state = None
                self.done = True

            # Klikk på stopp-knapp
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.knstopp.sjekk_klikk(event.pos):
                    self.next_state = None
                    self.done = True

            # Klikk på fortsett-knapp
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.knfortsett.sjekk_klikk(event.pos):
                    self.next_state = "GAME"
                    self.done = True

    def update(self, dt: float):
        pass  # ikke viktig

    def draw(self, surface: pygame.Surface):
        # Tegn bakgrunn
        surface.blit(self.image, (0, 0))

        # Tegn knapper
        self.knfortsett.draw(surface)
        self.knstopp.draw(surface)

        # Debug: tegn museposisjon
        """
        mouse_pos = pygame.mouse.get_pos()
        text = self.font.render(f"{mouse_pos}", True, (255, 255, 255))
        surface.blit(text, (300, 300))
        """

# Klasse for knapper
class knapp():
    def __init__(self, x, y, width, height, tykkelse = 2):
        self.rect = pygame.Rect(x, y, width, height)
        self.farge = (255, 0, 0)
        self.tykkelse = tykkelse

    def draw(self, surface):
        pass  # Tegner ingenting foreløpig
    
    def sjekk_klikk(self,mouse_pos):
        # Returner True hvis museposisjon er innenfor knappens rektangel
        return self.rect.collidepoint(mouse_pos)