# OOP -> Bulidling a proper player class
# Why Class(oop concept) needs for player?
'''
    Right Now the day 3 game is only single player ,
    But When We Need to Create Multiplayer Game Then 
    We can't Initialize the player like this..
    👎🏽👎🏽👎🏽❎❎❎
    player      = pygame.Rect(...)
    PLAYER_SPEED= 5
    SCORE       = 0
'''
import pygame
import sys
import random
import math
import numpy as np

# Initialization
pygame.init()
pygame.mixer.init()

WIDTH ,HEIGHT = 600,400
FPS = 60

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("MY FIRST GAME WINDOW")
clock = pygame.time.Clock()

# Colors
BLACK     = (0  , 0  , 0  )
RED       = (255, 0  , 0  )
ORANGE    = (255, 166,  80)
WHITE     = (255, 255, 255)
GREEN     = (0  , 200, 0  )
AQUA      = (164, 255, 240)
PURPLE    = (236, 125, 255)
LIGHT_RED = (255, 183, 150)


font       = pygame.font.SysFont("Arial",46)
small_font = pygame.font.SysFont("Arial",18)

# ==================== SOUND GENERATOR ====================
def make_beep(frequency = 400,duration = 0.1, volume = 0.3):
    sample_rate = 44100
    frames      = int(sample_rate * duration)
    t           = np.linspace(0,duration,frames,False)
    wave        = (np.sin(2*np.pi*frequency*t)*volume*32767).astype(np.int16)
    stereo      = np.column_stack([wave,wave])
    return pygame.sndarray.make_sound(stereo)

sound_collect        = make_beep(frequency=500,duration=0.08,volume=0.4)
sound_hit            = make_beep(frequency=200,duration=0.5 ,volume=0.5)
sound_win            = make_beep(frequency=700,duration=0.5 ,volume=0.4)
sound_gameover       = make_beep(frequency=200,duration=0.6 ,volume=0.4)
sound_gameover_beep2 = make_beep(frequency=170,duration=0.6 ,volume=0.4)
sound_gameover_beep3 = make_beep(frequency=150,duration=0.6 ,volume=0.4)

# ==================== PLAYER CLASS =======================
class Player:
    SIZE  = 40
    SPEED = 5

    # ANIMATION FRAMES : (COLOR,WIDTH,HEIGHT)
    FRAMES = [
        (GREEN      ,40,40),
        ((80,220,80),42,38),
        (GREEN      ,40,40),
        ((80,220,80),38,42)
    ]

    def __init__(self,x,y):
        self.rect        = pygame.Rect(x,y,self.SIZE,self.SIZE)
        self.color       = GREEN
        self.score       = 0
        self.health      = 3
        self.flash_timer = 0
        self.frame_index = 0
        self.frame_timer = 0
        self.frame_speed = 8
        self.is_moving   = False
        self.alive       = True 

    def handle_input(self):
        keys = pygame.key.get_pressed()
        speed = self.SPEED * 2 if keys[pygame.K_LSHIFT] else self.SPEED

        self.is_moving = False

        if keys[pygame.K_LEFT]  or keys[pygame.K_a] :  
            self.rect.x -= speed 
            self.is_moving = True
        if keys[pygame.K_RIGHT] or keys[pygame.K_d] :  
            self.rect.x += speed
            self.is_moving = True
        if keys[pygame.K_UP]    or keys[pygame.K_w] :
            self.rect.y -= speed
            self.is_moving = True
        if keys[pygame.K_DOWN]  or keys[pygame.K_s] :
            self.rect.y += speed
            self.is_moving = True

    def update(self,screen_rect):
        self.rect.clamp_ip(screen_rect)

        # Flash Effect -> Restore Color after 20 frames
        if self.flash_timer > 0 :
            self.flash_timer -= 1
            # self.color = (200,80,80)
        # else:
        #     self.color = GREEN

        if self.is_moving :
            self.flash_timer += 1
            if self.frame_timer >= self.frame_speed:
                self.frame_timer = 0
                self.frame_index = (self.frame_index + 1) % len(self.FRAMES)
        else:
            self.frame_index = 0
            self.frame_timer = 0

    def draw(self,surface):
         # $$$$$$$$$$$$$$$$$$$$ Day 5
        color,w,h = self.FRAMES[self.frame_index]
        if self.flash_timer > 0:
            color = RED

        draw_rect = pygame.Rect(
            self.rect.centerx - w // 2,
            self.rect.centery - h // 2,
            w , h
        )
        # $$$$$$$$$$$$$$$$$$$$$$$$$$$$
        
        pygame.draw.rect(surface,color,draw_rect,border_radius=7)

        for i in range(self.health):
            pygame.draw.rect(surface,RED,(self.rect.x+i*14,self.rect.y-14,10,8))

    def take_damage(self):
        self.health -= 1
        self.flash_timer = 20
        sound_hit.play()    
        return self.health <= 0 #Return True when all health is gone (player is dead)

    def collect(self):
        print(G["player"])
        sound_collect.play()
        self.score += 1  

    def __str__(self):
        return f"Player | Score : {self.score} | Health : {self.health}"

# ==================== ENEMY CLASS =======================
class Enemy:
    SIZE  = 30
    SPEED = 1
    random_widht  = random.choice([0,WIDTH-SIZE])
    random_height = random.choice([0,HEIGHT-SIZE])
    def __init__(self):
        # self.color = ORANGE
        self.rect = self._random_rect()
        self.tick = 0
    
    def _random_rect(self):
        sides =  random.choice(["RIGHT","LEFT","BOTTOM","TOP"])
        if sides == "TOP"     : x,y = random.randint(0,WIDTH-self.SIZE),0
        elif sides == "BOTTOM": x,y = random.randint(0,WIDTH-self.SIZE),HEIGHT-self.SIZE
        elif sides == "RIGHT" : x,y = WIDTH-self.SIZE                  ,random.randint(0,HEIGHT-self.SIZE)
        else                  : x,y = 0                                ,random.randint(0,HEIGHT-self.SIZE)
        return pygame.Rect(x,y,self.SIZE,self.SIZE)
    
    def move(self,target_x,target_y):
        
        if self.rect.x < target_x : self.rect.x += self.SPEED
        if self.rect.x > target_x : self.rect.x -= self.SPEED
        
        if self.rect.y < target_y : self.rect.y += self.SPEED
        if self.rect.y > target_y : self.rect.y -= self.SPEED
        self.tick += 1
    
    def draw(self,surface):
        effect = int(math.sin(self.tick*0.2)*3)
        draw_rect = pygame.Rect(
            self.rect.x - effect,
            self.rect.y - effect,
            self.SIZE + effect * 2,
            self.SIZE + effect * 2,
        )
        pygame.draw.rect(surface,ORANGE,draw_rect,border_radius=4)
        pygame.draw.rect(surface,RED   ,draw_rect,2,border_radius=4)

# ==================== HAZARD CLASS =======================
class Hazard:
    """A Bouncing Obstacle that damages the player on touch"""
    SIZE = 20

    def __init__(self):
        self.rect = pygame.Rect(
            random.randint(20,WIDTH-self.SIZE),        
            random.randint(20,HEIGHT-self.SIZE),
            self.SIZE,        
            self.SIZE        
        )
        # self.color = AQUA
        self.vel_x = random.choice([-3,-2,2,3])
        self.vel_y = random.choice([-3,-2,2,3])
        self.tick  = 0

    def update(self):
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y
        self.tick   += 1

        if self.rect.left <= 0 or self.rect.right >= WIDTH:
            self.vel_x *= -1
        if self.rect.top <= 0 or self.rect.bottom >= HEIGHT:
            self.vel_y *= -1

    def draw(self,surface):
        radius = int((math.sin(self.tick * 0.15) + 1) * 5)
        pygame.draw.rect(surface,WHITE,self.rect,border_radius=radius)

# ==================== TARGET CLASS =======================
class Target:
    MIN_SIZE = 15

    def __init__(self,size = 40):
        self.size = size   
        # self.color = PURPLE
        self.rect = self._random_rect()
        self.tick = random.randint(0,100)

    def _random_rect(self):
        return pygame.Rect(
            random.randint(0,WIDTH  - self.size),
            random.randint(0,HEIGHT - self.size),
            self.size,
            self.size
        )
    
    def respawn(self):
        """Shrink by 5px and move to new random position"""
        self.size = max(self.size - 5,self.MIN_SIZE)
        self.rect = self._random_rect()
        self.tick = 0

    def update(self):
        self.tick += 1

    def draw(self,surface):
        bob_y = int(math.sin(self.tick*0.08) * 5)
        draw_r = pygame.Rect(self.rect.x,self.rect.y+bob_y,self.size,self.size)
        pygame.draw.rect(surface,LIGHT_RED,draw_r,border_radius=5)

        outline_size = self.size + int(math.sin(self.tick * 0.1)*3)
        outline_rect = pygame.Rect(
            self.rect.centerx - outline_size // 2, 
            self.rect.centery - outline_size // 2 + bob_y,
            outline_size, 
            outline_size 
        )
        pygame.draw.rect(surface,ORANGE,outline_rect,2,border_radius=5)

# ==================== GAME SETUP =======================
def reset_game():
    return {
        "player"    : Player(WIDTH // 2,HEIGHT // 2),
        "target"    : Target(),
        "enemy"     : Enemy(),
        "hazards"   : [Hazard() for _ in range(3)],
        "GAME_STAT" : "MENU",
        "start_time":pygame.time.get_ticks(),
        "reason"    : ""
    }

G = reset_game()

WIN_SCORE  = 5
TIME_LIMIT = 20
is_muted   = False
mute       = "UNMUTE"
all_sound  = [sound_collect ,sound_gameover ,sound_hit ,sound_win,sound_gameover_beep2,sound_gameover_beep3]

# =====================================================

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type ==pygame.KEYDOWN:
            if event.key == pygame.K_r and G["GAME_STAT"] != "PLAYING":
                G = reset_game()
                G["GAME_STAT"] = "PLAYING"
            if event.key == pygame.K_m:
                is_muted = not is_muted
                mute     = "MUTE" if is_muted else "UNMUTE"
                for sound in all_sound:
                    sound.set_volume(0 if is_muted else 0.4)
            if event.key == pygame.K_SPACE and G["GAME_STAT"] == "MENU":
                G["GAME_STAT"] = "PLAYING"
                print("Space pressed")
            if event.key == pygame.K_q and G["GAME_STAT"] == "MENU":
                pygame.quit()
                sys.exit()
    
    elapsed   = (pygame.time.get_ticks() - G["start_time"]) / 1000
    time_left = TIME_LIMIT - elapsed 

    if G["GAME_STAT"] == "PLAYING":

        G["enemy"].move(G["player"].rect.x,G["player"].rect.y)

        if G["player"].rect.colliderect(G["enemy"].rect):
            dead = G["player"].take_damage()
            G["enemy"].rect.x +=G["enemy"].SPEED * 15 * (1 if G["enemy"].rect.x > G["player"].rect.x else -1)
            G["enemy"].rect.y +=G["enemy"].SPEED * 15 * (1 if G["enemy"].rect.y > G["player"].rect.y else -1)
            if dead:
                sound_gameover.play()
                sound_gameover_beep2.play()
                sound_gameover_beep3.play()
                G["reason"] = "YOU ARE DEFEATED!"
                G["GAME_STAT"] = "GAME_OVER"

        if time_left <= 0:
            G["reason"] = "TOO SLOW!"
            G["GAME_STAT"] = "GAME_OVER"

        G["player"].handle_input()
        G["player"].update(screen.get_rect())

        for hazard in G["hazards"]:
            hazard.update()

        G["target"].update()

        if G["player"].rect.colliderect(G["target"].rect):
            G["player"].collect()
            G["target"].respawn()
            if G["player"].score >= WIN_SCORE:
                G["GAME_STAT"] = "WIN"

        for hazard in G["hazards"] :
            if G["player"].rect.colliderect(hazard.rect):
                dead = G["player"].take_damage()
                hazard.rect.x += hazard.vel_x * 10 
                hazard.rect.y += hazard.vel_y * 10 
                if dead:
                    sound_gameover.play()
                    sound_gameover_beep2.play()
                    sound_gameover_beep3.play()
                    G["reason"] = "YOU ARE DEFEATED!"
                    G["GAME_STAT"] = "GAME_OVER"
        
    # Draw
    screen.fill(BLACK)

    if G["GAME_STAT"] == "PLAYING":
        G["target"].draw(screen)
        G["enemy"].draw(screen)
        for hazard in G["hazards"]:
            hazard.draw(screen)
        G["player"].draw(screen)

        score_txt = small_font.render(f"SCORE : {G["player"].score}/{WIN_SCORE}",True,WHITE)
        screen.blit(score_txt,(10,10))

        timer_color = RED if time_left < 5 else WHITE
        timer_txt = small_font.render(f"TIME : {time_left:.1f}s",True,timer_color)
        screen.blit(timer_txt,(WIDTH - timer_txt.get_width()-10, 10))

    elif G["GAME_STAT"] == "WIN":
        win_text = font.render(f"YOU WIN !",True,RED)
        sub_txt = small_font.render(f"SCORE : {G["player"].score}",True,GREEN)
        restart = small_font.render(f"PRESS 'R' TO PLAY AGAIN",True,WHITE)
        timer = small_font.render(f"Time : {elapsed:.1f} seconds",True,WHITE)
    
        screen.blit(win_text, (WIDTH//2 - win_text.get_width()//2 , 120))   
        screen.blit(timer   , (WIDTH//2 - win_text.get_width()//2 , 160))   
        screen.blit(sub_txt ,  (WIDTH//2 - sub_txt.get_width()//2  , 200))
        screen.blit(restart ,  (WIDTH//2 - restart.get_width()//2  , 250))
    
    elif G["GAME_STAT"] == "GAME_OVER":
        over_txt = font.render(f"GAME OVER !",True,RED)
        reason_txt = small_font.render(G["reason"],True,WHITE)
        restart = small_font.render(f"PRESS 'R' TO PLAY AGAIN",True,WHITE)

        screen.blit(over_txt  ,(WIDTH//2 - over_txt.get_width()//2 , 100))
        screen.blit(reason_txt  ,(WIDTH//2 - over_txt.get_width()//2 , 150))
        screen.blit(restart   ,(WIDTH//2 - over_txt.get_width()//2 , 200))

    elif G["GAME_STAT"] == "MENU":
        bob = int(math.sin(pygame.time.get_ticks() * 0.003) * 10)
        title = font.render(f"COLLECTOR GAME",True,ORANGE)
        start = small_font.render(f"Press Space To Start!",True,WHITE)
        quit  = small_font.render(f"Press Q To Quit Game!",True,WHITE)

        screen.blit(title,(WIDTH//2 - title.get_width()//2,100 + bob))
        screen.blit(start,(WIDTH//2 - start.get_width()//2,200 + bob))
        screen.blit(quit ,(WIDTH//2 - quit.get_width()//2,250  + bob))

    sound_txt = small_font.render(f"[M] {mute}",True,WHITE)
    screen.blit(sound_txt,(WIDTH - sound_txt.get_width()-10,380))

    pygame.display.flip()
    clock.tick(FPS)