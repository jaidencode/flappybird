import pygame
import random
import sys
import numpy as np
import sounddevice as sd

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
GRAVITY = 0.35
FLAP_STRENGTH = -9

# Pipe properties
PIPE_WIDTH = 60
PIPE_GAP = 150
PIPE_SPEED = 3

# Ground level
GROUND_HEIGHT = 50

# Sounddevice parameters
SAMPLE_RATE = 44100

def play_tone(freq, duration, amp=0.5):
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration), endpoint=False)
    wave = amp * np.sin(2 * np.pi * freq * t)
    sd.play(wave, SAMPLE_RATE, blocking=False)

def play_flap_sound():
    play_tone(600, 0.05)

def play_hit_sound():
    play_tone(200, 0.2)

font = pygame.font.SysFont(None, 36)


def spawn_pipe(pipes):
    gap_y = random.randint(100, SCREEN_HEIGHT - 100 - PIPE_GAP)
    top_rect = pygame.Rect(SCREEN_WIDTH, 0, PIPE_WIDTH, gap_y)
    bottom_rect = pygame.Rect(
        SCREEN_WIDTH,
        gap_y + PIPE_GAP,
        PIPE_WIDTH,
        SCREEN_HEIGHT - gap_y - PIPE_GAP - GROUND_HEIGHT,
    )
    pipes.append((top_rect, bottom_rect))


def show_start_screen():
    screen.fill((0, 0, 0))
    msg = font.render("Press SPACE to start", True, (255, 255, 255))
    rect = msg.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    screen.blit(msg, rect)
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                return True
        clock.tick(FPS)


def game_over_screen(score):
    screen.fill((0, 0, 0))
    msg = font.render(f"Game Over! Score: {score}", True, (255, 255, 255))
    rect = msg.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 20))
    screen.blit(msg, rect)

    restart = font.render("Press SPACE to play again", True, (255, 255, 255))
    r_rect = restart.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20))
    screen.blit(restart, r_rect)
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                return True
        clock.tick(FPS)


def run_game():
    bird_y = SCREEN_HEIGHT // 2
    bird_vel = 0
    pipes = []
    score = 0
    timer = 0
    spawn_pipe(pipes)

    running = True
    while running:
        clock.tick(FPS)
        timer += 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                bird_vel = FLAP_STRENGTH
                play_flap_sound()

        bird_vel += GRAVITY
        bird_y += bird_vel
        bird_rect = pygame.Rect(BIRD_X, int(bird_y), BIRD_SIZE, BIRD_SIZE)

        if timer % 90 == 0:
            spawn_pipe(pipes)

        for top, bottom in pipes:
            top.x -= PIPE_SPEED
            bottom.x -= PIPE_SPEED
            if bird_rect.colliderect(top) or bird_rect.colliderect(bottom):
                play_hit_sound()
                running = False
        pipes = [p for p in pipes if p[0].right > 0]
        for top, bottom in pipes:
            if top.right < BIRD_X and not getattr(top, "scored", False):
                score += 1
                top.scored = True

        if bird_y + BIRD_SIZE > SCREEN_HEIGHT - GROUND_HEIGHT:
            play_hit_sound()
            running = False

        screen.fill((135, 206, 235))

        for top, bottom in pipes:
            pygame.draw.rect(screen, (34, 139, 34), top)
            pygame.draw.rect(screen, (34, 139, 34), bottom)

        ground_rect = pygame.Rect(
            0, SCREEN_HEIGHT - GROUND_HEIGHT, SCREEN_WIDTH, GROUND_HEIGHT
        )
        pygame.draw.rect(screen, (222, 184, 135), ground_rect)

        pygame.draw.rect(screen, (255, 255, 0), bird_rect)

        score_surf = font.render(str(score), True, (255, 255, 255))
        screen.blit(score_surf, (SCREEN_WIDTH // 2 - score_surf.get_width() // 2, 20))

        pygame.display.flip()

    return score


def main():
    if not show_start_screen():
        pygame.quit()
        sys.exit()

    while True:
        score = run_game()
        if not game_over_screen(score):
            break

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
