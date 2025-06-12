import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

# Game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Game clock
clock = pygame.time.Clock()
FPS = 60

# Bird properties
BIRD_X = 50
BIRD_SIZE = 30
bird_y = SCREEN_HEIGHT // 2
bird_vel = 0
GRAVITY = 0.5
FLAP_STRENGTH = -9

# Pipe properties
PIPE_WIDTH = 60
PIPE_GAP = 150
pipe_speed = 3
pipes = []

# Score
score = 0
font = pygame.font.SysFont(None, 36)

# Ground level
GROUND_HEIGHT = 50

def spawn_pipe():
    gap_y = random.randint(100, SCREEN_HEIGHT - 100 - PIPE_GAP)
    top_rect = pygame.Rect(SCREEN_WIDTH, 0, PIPE_WIDTH, gap_y)
    bottom_rect = pygame.Rect(SCREEN_WIDTH, gap_y + PIPE_GAP, PIPE_WIDTH, SCREEN_HEIGHT - gap_y - PIPE_GAP - GROUND_HEIGHT)
    pipes.append((top_rect, bottom_rect))

# Spawn the first pipe
timer = 0
spawn_pipe()

running = True
while running:
    clock.tick(FPS)
    timer += 1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird_vel = FLAP_STRENGTH

    # Bird movement
    bird_vel += GRAVITY
    bird_y += bird_vel
    bird_rect = pygame.Rect(BIRD_X, int(bird_y), BIRD_SIZE, BIRD_SIZE)

    # Spawn new pipes periodically
    if timer % 90 == 0:
        spawn_pipe()

    # Move pipes and check for collisions
    for top, bottom in pipes:
        top.x -= pipe_speed
        bottom.x -= pipe_speed
        # Collision with bird
        if bird_rect.colliderect(top) or bird_rect.colliderect(bottom):
            running = False
    # Remove off-screen pipes and update score
    pipes = [p for p in pipes if p[0].right > 0]
    for top, bottom in pipes:
        if top.right < BIRD_X and not getattr(top, 'scored', False):
            score += 1
            top.scored = True

    # Collision with ground
    if bird_y + BIRD_SIZE > SCREEN_HEIGHT - GROUND_HEIGHT:
        running = False

    # Drawing
    screen.fill((135, 206, 235))  # Sky blue background

    # Draw pipes
    for top, bottom in pipes:
        pygame.draw.rect(screen, (34, 139, 34), top)      # Top pipe
        pygame.draw.rect(screen, (34, 139, 34), bottom)   # Bottom pipe

    # Draw ground
    ground_rect = pygame.Rect(0, SCREEN_HEIGHT - GROUND_HEIGHT, SCREEN_WIDTH, GROUND_HEIGHT)
    pygame.draw.rect(screen, (222, 184, 135), ground_rect)

    # Draw bird
    pygame.draw.rect(screen, (255, 255, 0), bird_rect)  # Yellow bird

    # Draw score
    score_surf = font.render(str(score), True, (255, 255, 255))
    screen.blit(score_surf, (SCREEN_WIDTH // 2 - score_surf.get_width() // 2, 20))

    pygame.display.flip()

# Game over screen
screen.fill((0, 0, 0))
msg = font.render(f"Game Over! Score: {score}", True, (255, 255, 255))
rect = msg.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
screen.blit(msg, rect)
pygame.display.flip()

# Wait for a key press or quit event
waiting = True
while waiting:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            waiting = False
        if event.type == pygame.KEYDOWN:
            waiting = False

pygame.quit()
sys.exit()
