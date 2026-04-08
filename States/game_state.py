"""
Dette er staten for spillet. Det er her du legger til Spillobjekter, logikk, etc...
"""

from states.base_state import BaseState
import pygame
import math
import random


class GameState(BaseState):
    def __init__(self):
        super().__init__()
        self.spillere = []
        self.fiender  = []
        self.prosjektiler = []
        self.spiller_base = Base(147, 0, 44, 800, (255, 255, 0))
        self.fiende_base  = Base(1197, 0, 42, 800, (255, 255, 255))
        self.knsoldat1 = Knapp(1100, 0, 50, 50, "assets/soldat_button.png")
        self.knrobot = Knapp(1160, 0, 50, 50, "assets/robot_button.png")
        self.knsettings = Knapp(0, 0, 50, 50, "assets/settings_button.png")

        self.spawn_timer = 0
        self.spawn_intervall = random.uniform(1, 5)
        self.gull = 100
        self.gull_timer = 0
        self.image = pygame.image.load("assets/bakgrunn.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (1500, 800))

    def on_enter(self):
        pygame.mixer.music.load("assets/gamestate_music.mp3")
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(1)
        
    def handle_events(self, events : list[pygame.event.Event]):
        for event in events:
            if event.type == pygame.QUIT:
                self.next_state = None
                self.done = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.next_state = "MENU"
                    self.done = True
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.knsettings.sjekk_klikk(event.pos):
                    self.next_state = "MENU"
                    self.done = True
                elif self.knsoldat1.sjekk_klikk(event.pos):
                    if self.gull >= 50:
                        self.spillere.append(Spiller(145, 613, 170, 100, 150, 300, 20, 1, 2, "ranged", "assets/tank.png"))
                        self.gull -= 50
                elif self.knrobot.sjekk_klikk(event.pos):
                    if self.gull >= 100:
                        self.spillere.append(Spiller(145, 620, 120, 200, 450 , 50, 100, 0.67, 4, "melee", "assets/robot.png"))
                        self.gull -= 100

    def update(self, dt: float):
        self.gull_timer += dt
        if self.gull_timer >= 1:
            self.gull += 10
            self.gull_timer = 0

        self.spawn_timer += dt
        if self.spawn_timer >= self.spawn_intervall:
            self.fiender.append(Fiende(1500, 622, 70, 80, 100, 600, 20, 1, 2, "ranged", "assets/alian.png"))
            self.spawn_timer = 0
            self.spawn_intervall = random.uniform(2, 5)

        for soldat in self.spillere:
            soldat.update(dt)
            soldat.speed = soldat.speed_std
            for fiende in self.fiender:
                if soldat.sjekk_rekkevidde(fiende):
                    soldat.speed = 0
                    soldat.angrip(fiende, self.prosjektiler)

        for fiende in self.fiender:
            fiende.update(dt)
            fiende.speed = fiende.speed_std
            for soldat in self.spillere:
                if fiende.sjekk_rekkevidde(soldat):
                    fiende.speed = 0
                    fiende.angrip(soldat, self.prosjektiler)



        for skudd in self.prosjektiler[:]:
            skudd.update(dt)
            if skudd.team == "spiller":
                for fiende in self.fiender:
                    if fiende.rect.collidepoint(skudd.x, skudd.y):
                        fiende.hp -= skudd.skade
                        self.prosjektiler.remove(skudd)
                        break
            if skudd.team == "fiende":
                for soldat in self.spillere:
                    if soldat.rect.collidepoint(skudd.x, skudd.y):
                        soldat.hp -= skudd.skade
                        self.prosjektiler.remove(skudd)
                        break

        self.prosjektiler = [s for s in self.prosjektiler if 0 < s.x < 1500] # sltter prosjektiler som er utenfor skjermen


        for soldat in self.spillere[:]:
            if soldat.rect.colliderect(self.fiende_base.rect):
                if self.fiende_base.hp > 0:
                    self.fiende_base.hp -= 1
                    self.spillere.remove(soldat)
            elif soldat.hp <= 0:
                self.spillere.remove(soldat)
        
        for fiende in self.fiender[:]:
            if fiende.rect.colliderect(self.spiller_base.rect):
                if self.spiller_base.hp > 0:
                    self.spiller_base.hp -= 1
                    self.fiender.remove(fiende)
            elif fiende.hp <= 0:
                self.fiender.remove(fiende)


        # Sjekker base statusen
        if self.fiende_base.hp <= 0:
            self.next_state = "VICTORY"
            self.done = True

        elif self.spiller_base.hp <= 0:
            self.next_state = "MENU"
            self.done = True

    def draw(self, surface: pygame.Surface):
        surface.blit(self.image, (0, 0))
        self.spiller_base.draw(surface, self.font)
        self.fiende_base.draw(surface, self.font)
        for soldat in self.spillere:
            soldat.draw(surface)
        for fiende in self.fiender:
            fiende.draw(surface)
        for skudd in self.prosjektiler:
            skudd.draw(surface)
        self.knsoldat1.draw(surface)
        self.knsettings.draw(surface)
        self.knrobot.draw(surface)
        self.draw_text(surface, f"Gull: {self.gull}", self.font, (255, 215, 0), (500, 20))

        mouse_pos = pygame.mouse.get_pos()
        text = self.font.render(f"{mouse_pos}", True, (255, 255, 255))
        surface.blit(text, (300, 300))




# ================================
# Hjelpeklasser
# ================================

class Spillobjekt():
    def __init__(self, x, y, width, height, hp, rekkevidde, skade, speed, cooldown, atk_type, team, bilde_navn):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.hp = hp
        self.rekkevidde = rekkevidde
        self.skade = skade
        self.speed_std = speed
        self.speed = speed
        self.cooldown_std = cooldown
        self.cooldown_count = 0
        self.atk_type = atk_type
        self.team = team

        self.bilde = pygame.image.load(bilde_navn).convert_alpha()
        self.bilde = pygame.transform.scale(self.bilde, (width, height))

        self.rect = pygame.Rect(x - width // 2, y - height, width, height)

    def sjekk_rekkevidde(self, target):
        dx = self.x - target.x
        dy = self.y - target.y
        avstand = dx**2 + dy**2
        return avstand <= self.rekkevidde**2
       

    def angrip(self, target, prosjektiler):

        if self.cooldown_count > 0:
            return
        
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
            prosjektiler.append(Prosjektil(self.x, self.y - self.height // 2, retning_x, retning_y, self.skade, self.team))
        self.cooldown_count = self.cooldown_std

    def update_base(self, dt):
        self.cooldown_count -= dt
        self.rect = pygame.Rect(self.x - self.width // 2, self.y - self.height, self.width, self.height)

    def draw(self, surface):
        surface.blit(self.bilde, self.rect)


class Spiller(Spillobjekt):
    def __init__(self, x, y, width, height, hp, rekkevidde, skade,speed, cooldown, atk_type, bilde_navn):
        super().__init__(x, y, width, height, hp, rekkevidde, skade, speed, cooldown,  atk_type, team="spiller", bilde_navn=bilde_navn)
        self.speed = speed
        self.cooldown_std = cooldown

    def update(self, dt):
        self.x += self.speed
        self.update_base(dt)


class Fiende(Spillobjekt):
    def __init__(self, x, y, width, height, hp, rekkevidde, skade, speed, cooldown, atk_type, bilde_navn):
        super().__init__(x, y, width, height, hp, rekkevidde, skade,speed, cooldown, atk_type, team="fiende", bilde_navn=bilde_navn)
        self.speed = speed
        self.cooldown_std = cooldown
        self.color = (255, 0, 0)

    def update(self, dt):
        self.x -= self.speed
        self.update_base(dt)


class Base:
    def __init__(self, x, y, width, height, color):
        self.rect = pygame.Rect(x , y, width, height)
        self.color = color
        self.hp = 10

    def draw(self, surface, font):
        pygame.draw.rect(surface, self.color, self.rect)
        surface.blit(font.render(f"HP: {self.hp}", True, (255, 255, 255)), (self.rect.x, self.rect.y - 20))


class Knapp:
    def __init__(self, x, y, width, height, bildenavn):
        self.rect = pygame.Rect(x, y, width, height)
        self.knapp1_bilde = pygame.image.load(bildenavn).convert_alpha()
        self.knapp1_bilde = pygame.transform.scale(self.knapp1_bilde, (self.rect.width, self.rect.height))

    def draw(self, surface):
        surface.blit(self.knapp1_bilde, self.rect)

    def sjekk_klikk(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)


class Prosjektil:
    def __init__(self, x, y, retning_x, retning_y, skade, team):
        self.x = x + retning_x * 20
        self.y = y + retning_y * 20
        self.retning_x = retning_x
        self.retning_y = retning_y
        self.skade = skade
        self.speed = 5
        self.team = team

    def update(self, dt):
        self.x += self.retning_x * self.speed
        self.y += self.retning_y * self.speed

    def draw(self, surface):
        pygame.draw.circle(surface, (255, 255, 0), (int(self.x), int(self.y)), 5)