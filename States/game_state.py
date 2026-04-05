"""
Dette er staten for spillet. Det er her du legger til Spillobjekter, logikk, etc...
"""

from states.base_state import BaseState
import pygame
import math


class GameState(BaseState):
    def __init__(self):
        super().__init__()
        self.spillere = []
        self.fiender  = []
        self.knsoldat1 = Knapp(700, 0, 50, 50, "assets/soldat.png") #Soldat knapp
        self.knsettings = Knapp(0,0, 50, 50, "assets/settings_button.png") #Settins knapp

    def handle_events(self, events : list[pygame.event.Event]):
        for event in events:
            if event.type == pygame.QUIT:
                self.next_state = None
                self.done = True
            # Menu sjekk
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.knsettings.sjekk_klikk(event.pos):
                    self.next_state = "MENU"
                    self.done = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.next_state = "MENU"
                    self.done = True
            
            #Soldat sjekk
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: # venstre musen
                if self.knsoldat1.sjekk_klikk(event.pos):
                    self.spillere.append(Spiller(60, 400,hp=100, rekkevidde=100, skade=10, atk_type="Ranged"))
            


    def update(self, dt: float):
        #Spill karakterer
        for soldat in self.spillere:
            soldat.update(dt)
        for fiende in self.fiender:
            if soldat.sjekk_rekkevidde(fiende):
                soldat.angrrip(fiende, self.prosjektiler)

    def draw(self, surface: pygame.Surface):
        surface.fill((0, 0, 0))

        #Spill karakterer
        for soldat in self.spillere:
            soldat.draw(surface)
        for fiende in self.fiender:
            fiende.draw(surface)
        #self.draw_text(surface, "SPACE = send soldat | ESC = meny", self.font, (255, 255, 255), (250, 20))

        #----Knapper----

        #soldat_1 knapp
        self.knsoldat1.draw(surface)
        
        #settings knapp
        self.knsettings.draw(surface)


# Spill klasser

class Spillobjekt():
    def __init__(self, x, y, width, height, hp, rekkevidde, skade, atk_type):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.hp = hp
        self.rekkevidde = rekkevidde
        self.skade = skade
        self.atk_type = atk_type

        self.rect = pygame.Rect(x - width // 2, y - height // 2, width, height)
    
    def sjekk_rekkevidde(self, target):
        dx = self.x - target.x
        dy = self.y - target.y
        avstand = math.sqrt(dx**2 + dy**2)
        return avstand <= self.rekkevidde
    
    def angrip(self,target, prosejektiler):
        
        if self.atk_type == "melee":
            target.hp -= self.skade
        elif self.atk_type == "ranged":
            dx = target.x - self.x
            dy = target.y - self.y
            avstand = math.sqrt(dx**2 + dy**2)

            if avstand == 0:
                return
            retning_x = dx / avstand
            retning_y = dy / avstand
            
            prosjektiler.append(prosejektiler(self.x, self.y, retning_x, retning_y, skade=self.skade))

    def update_base(self, dt):
        self.rect = pygame.Rect(self.x - self.width // 2, self.y - self.height // 2, self.width, self.height)

class Spiller(Spillobjekt):
    def __init__(self, x, y, **kwargs):
        super().__init__(x, y, width = 20, height = 30, **kwargs)
        self.speed = 2
        self.color = (0, 200, 0)
        



    def update(self, dt):
        self.x += self.speed
        self.update_base(dt)


    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)


class Fiende(Spillobjekt):
    def __init__(self, x, y):
        super().__init__(x, y, width = 20, height = 20, **kwargs)
        self.speed = 2
        self.color = (200, 0, 0)

    def update(self, dt):
        self.x -= self.speed
        self.update_base(dt)

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