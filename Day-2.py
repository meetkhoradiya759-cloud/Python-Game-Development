# Keyword input & movements

# There 2 ways to handle Keyboard input
import pygame
import sys
import random

pygame.init()

WIDTH  = 600
HEIGHT = 400
FPS    = 60

screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption(("Keyword Input & Movement"))
clock = pygame.time.Clock()

WHITE   = (255,255,255)
BLACK   = (0,0,0)
RED     = (255,0,0)
GREEN   = (0,150,0)

# Font
font = pygame.font.SysFont("arial",24)
small_font = pygame.font.SysFont("arial",16)

# Player setup
PLAYER_SIZE  = 50
PLAYER_SPEED = 5
TARGET_SIZE = 50
current_target_size = TARGET_SIZE

player = pygame.Rect(
    WIDTH // 2 - PLAYER_SIZE // 2,  #Position WIDTH
    HEIGHT // 2 - PLAYER_SIZE // 2, #Position HEIGHT
    PLAYER_SIZE,
    PLAYER_SIZE
)

# ====================== Day 3 ============================

def new_target(size):
    return pygame.Rect(
        random.randint(0,WIDTH-size) ,
        random.randint(0,HEIGHT-size) ,
        size,
        size
    )

target = new_target(TARGET_SIZE)

GAME_STATE = "PLAYING"
SCORE = 0
WIN_SCORE = 5

# Millisecond timer 
TIME_LIMIT = 15
start_timer = pygame.time.get_ticks() 
# =========================================================

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # 1st Method : Event-based (fire once per keypress)
        # Disadvantage : Fills laggy
        '''
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                print("Left key pressed")
        '''

        # ============== Day 3 ====================
        if event.type ==pygame.KEYDOWN:
            if event.key == pygame.K_r and GAME_STATE in ("WIN","GAME OVER"):
                # Restart from win screen
                SCORE               = 0
                GAME_STATE          = "PLAYING"
                player.center       = (WIDTH // 2,HEIGHT // 2)
                target              = new_target(TARGET_SIZE)
                current_target_size = TARGET_SIZE
                start_timer         = pygame.time.get_ticks()
            elif event.key == pygame.K_q and GAME_STATE in ("WIN","GAME OVER"):
                pygame.quit()
                sys.exit()

        #==========================================
            
    # 2nd Method : State-based (checks every frames)
    '''
    keys = pygame.key.get_pressed()
    if keys[pygame.K_RIGHT]:
        print("Right key pressed")  
    '''

# =========================== Day 3 =========================================

    time_color = RED if time_left <= 5 else WHITE
    timer_txt = font.render(f"Time Left : {time_left:.1f}s",True,time_color)
    screen.blit(timer_txt,(WIDTH-timer_txt.get_width()-10 , 10)) 

    if GAME_STATE == "PLAYING": 

        elapsed = (pygame.time.get_ticks() - start_timer) / 1000
        time_left = TIME_LIMIT - elapsed

        if time_left <= 0:
            GAME_STATE = "GAME OVER"    

        keys = pygame.key.get_pressed()

        # Speed boost
        speed = PLAYER_SPEED * 2 if keys[pygame.K_LSHIFT]  else PLAYER_SPEED

        if keys[pygame.K_LEFT] or keys[pygame.K_a] : player.x -= speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]: player.x += speed
        if keys[pygame.K_UP] or keys[pygame.K_w]   : player.y -= speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s] : player.y += speed

        # Keep player inside the window
        player.clamp_ip(screen.get_rect())

        # Collision check
        if player.colliderect(target):
            SCORE += 1
            current_target_size -= 5
            current_target_size = max(current_target_size,15)
            target = new_target(current_target_size)
            if SCORE >= WIN_SCORE:
                GAME_STATE = "WIN"

# ===========================================================================

    screen.fill(BLACK)

# ============================== Day 3 ======================================    

    if GAME_STATE == "PLAYING":
        pygame.draw.rect(screen,RED,target)
        pygame.draw.rect(screen,GREEN,player)

        # display score
        score_text = font.render(f"SCORE : {SCORE}/{WIN_SCORE}",True,WHITE)
        screen.blit(score_text,(10,10)) 

        # Sinple Guide arrow for hint
        hint = font.render(f"Collect the red squares !",True,WHITE)
        screen.blit(hint,(10,HEIGHT-35))

    elif GAME_STATE == "WIN":
        win_text = font.render(f"YOU WIN !",True,RED)
        sub_txt = small_font.render(f"YOU COLLECED {SCORE} TARGETS",True,GREEN)
        quit_txt = small_font.render(f"PRESS 'Q' TO QUIT GAME",True,WHITE)
        restart = small_font.render(f"PRESS 'R' TO PLAY AGAIN",True,WHITE)
        timer = small_font.render(f"Time : {elapsed:.1f} seconds",True,WHITE)
    
        screen.blit(win_text, (WIDTH//2 - win_text.get_width()//2 , 120))
        screen.blit(sub_txt,  (WIDTH//2 - sub_txt.get_width()//2  , 200))
        screen.blit(restart,  (WIDTH//2 - restart.get_width()//2  , 250))
        screen.blit(quit_txt, (WIDTH//2 - restart.get_width()//2  , 300))
        screen.blit(timer,    (WIDTH//2 - restart.get_width()//2  , 160))

    elif GAME_STATE == "GAME OVER":
        over_txt = font.render(f"GAME OVER !",True,RED)
        slow_txt = small_font.render(f"TOO SLOW..!",True,WHITE)
        restart = small_font.render(f"PRESS 'R' TO PLAY AGAIN",True,WHITE)
        quit_txt = small_font.render(f"PRESS 'Q' TO QUIT GAME",True,WHITE)

        screen.blit(over_txt  ,(WIDTH//2 - over_txt.get_width()//2 , 100))
        screen.blit(slow_txt  ,(WIDTH//2 - over_txt.get_width()//2 , 150))
        screen.blit(restart   ,(WIDTH//2 - over_txt.get_width()//2 , 200))
        screen.blit(quit_txt  ,(WIDTH//2 - over_txt.get_width()//2 , 250))
        
# ===========================================================================

    pygame.display.flip()
    clock.tick(FPS)