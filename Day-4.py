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

# Initialization
pygame.init()

WIDTH = 800
HEIGHT = 600
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


font       = pygame.font.SysFont("Arial",24)
small_font = pygame.font.SysFont("Arial",16)

# ==================== PLAYER CLASS =======================
class Player:
    SIZE  = 40
    SPEED = 5

    def __init__(self,x,y):
        self.rect        = pygame.Rect(x,y,self.SIZE,self.SIZE)
        self.flash_timer = 0
        self.color       = GREEN
        self.score       = 0
        self.health      = 3

    def handle_input(self):
        keys = pygame.key.get_pressed()
        speed = self.SPEED * 2 if keys[pygame.K_LSHIFT] else self.SPEED

        if keys[pygame.K_LEFT]  or keys[pygame.K_a] :  self.rect.x -= speed 
        if keys[pygame.K_RIGHT] or keys[pygame.K_d] :  self.rect.x += speed 
        if keys[pygame.K_UP]    or keys[pygame.K_w] :  self.rect.y -= speed 
        if keys[pygame.K_DOWN]  or keys[pygame.K_s] :  self.rect.y += speed 

    def update(self,screen_rect):
        self.rect.clamp_ip(screen_rect)

        # Flash Effect -> Restore Color after 20 frames
        if self.flash_timer > 0 :
            self.flash_timer -= 1
            self.color = (200,80,80)
        else:
            self.color = GREEN

    def draw(self,surface):
        pygame.draw.rect(surface,self.color,self.rect)

        for i in range(self.health):
            pygame.draw.rect(surface,RED,(self.rect.x+i*14,self.rect.y-14,10,8))

    def take_damage(self):
        self.health -= 1
        self.flash_timer = 20
        return self.health <= 0 #Return True when all health is gone (player is dead)

    def __str__(self):
        return f"Player | Score : {self.score+1} | Health : {self.health}"

    def collect(self):
        print(player)
        self.score += 1  


# ==================== ENEMY CLASS =======================
class Enemy:
    SIZE  = 30
    SPEED = 1
    random_widht  = random.choice([0,WIDTH-SIZE])
    random_height = random.choice([0,HEIGHT-SIZE])
    def __init__(self):
        self.color = ORANGE
        self.rect = self._random_rect()
    
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
    
    def draw(self,surface):
        pygame.draw.rect(surface,self.color,self.rect)

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
        self.color = AQUA
        self.vel_x = random.choice([-3,-2,2,3])
        self.vel_y = random.choice([-3,-2,2,3])

    def update(self):
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y

        if self.rect.left <= 0 or self.rect.right >= WIDTH:
            self.vel_x *= -1
        if self.rect.left <= 0 or self.rect.right >= HEIGHT:
            self.vel_y *= -1

    def draw(self,surface):
        pygame.draw.rect(surface,self.color,self.rect)

# ==================== TARGET CLASS =======================
class Target:
    MIN_SIZE = 15

    def __init__(self,size = 40):
        self.size = size   
        self.color = PURPLE
        self.rect = self._random_rect()

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

    def draw(self,surface):
        pygame.draw.rect(surface,self.color,self.rect)

# ==================== GAME SETUP =======================
player = Player(WIDTH // 2,HEIGHT // 2)
target = Target()
enemy  = Enemy()
hazards = [Hazard() for _ in range(3)]

WIN_SCORE = 5
GAME_STAT = "PLAYING"

TIME_LIMIT = 20
start_time = pygame.time.get_ticks()

# =====================================================

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type ==pygame.KEYDOWN:
            if event.key == pygame.K_r and GAME_STAT != "PLAYING":
                # Restart from win screen
                player        = Player(WIDTH // 2,HEIGHT // 2)
                GAME_STAT     = "PLAYING"
                player.center = (WIDTH // 2,HEIGHT // 2)
                target        = Target()
                enemy         = Enemy()
                hazards       = [Hazard() for _ in range(3)]
                start_time    = pygame.time.get_ticks()
    
    elapsed   = (pygame.time.get_ticks() - start_time) / 1000
    time_left = TIME_LIMIT - elapsed 

    if GAME_STAT == "PLAYING":

        enemy.move(player.rect.x,player.rect.y)

        if player.rect.colliderect(enemy.rect):
            dead = player.take_damage()
            enemy.rect.x += (enemy.rect.x - player.rect.x)
            enemy.rect.y += (enemy.rect.y - player.rect.y)
            if dead:
                GAME_STAT = "GAME_OVER"

        if time_left <= 0:
            GAME_STAT = "GAME_OVER"

        player.handle_input()
        player.update(screen.get_rect())

        for hazard in hazards:
            hazard.update()

        if player.rect.colliderect(target.rect):
            player.collect()
            target.respawn()
            if player.score >= WIN_SCORE:
                GAME_STAT = "WIN"

        for hazard in hazards :
            if player.rect.colliderect(hazard.rect):
                dead = player.take_damage()
                hazard.rect.x += hazard.vel_x * 10 
                hazard.rect.y += hazard.vel_y * 10 
                if dead:
                    GAME_STAT = "GAME_OVER"
        

    # Draw
    screen.fill(BLACK)

    if GAME_STAT == "PLAYING":
        target.draw(screen)
        enemy.draw(screen)
        for hazard in hazards:
            hazard.draw(screen)
        player.draw(screen)

        score_txt = font.render(f"SCORE : {player.score}/{WIN_SCORE}",True,WHITE)
        screen.blit(score_txt,(10,10))

        timer_color = RED if time_left < 5 else WHITE
        timer_txt = font.render(f"TIME : {time_left:.1f}s",True,timer_color)
        screen.blit(timer_txt,(WIDTH - timer_txt.get_width()-10, 10))

    elif GAME_STAT == "WIN":
        win_text = font.render(f"YOU WIN !",True,RED)
        sub_txt = small_font.render(f"SCORE : {player.score}",True,GREEN)
        restart = small_font.render(f"PRESS 'R' TO PLAY AGAIN",True,WHITE)
        timer = small_font.render(f"Time : {elapsed:.1f} seconds",True,WHITE)
    
        screen.blit(win_text, (WIDTH//2 - win_text.get_width()//2 , 120))   
        screen.blit(timer   , (WIDTH//2 - win_text.get_width()//2 , 160))   
        screen.blit(sub_txt ,  (WIDTH//2 - sub_txt.get_width()//2  , 200))
        screen.blit(restart ,  (WIDTH//2 - restart.get_width()//2  , 250))
    
    elif GAME_STAT == "GAME_OVER":
        over_txt = font.render(f"GAME OVER !",True,RED)
        slow_txt = small_font.render(f"TOO SLOW..!",True,WHITE)
        restart = small_font.render(f"PRESS 'R' TO PLAY AGAIN",True,WHITE)

        screen.blit(over_txt  ,(WIDTH//2 - over_txt.get_width()//2 , 100))
        screen.blit(slow_txt  ,(WIDTH//2 - over_txt.get_width()//2 , 150))
        screen.blit(restart   ,(WIDTH//2 - over_txt.get_width()//2 , 200))

    pygame.display.flip()
    clock.tick(FPS)