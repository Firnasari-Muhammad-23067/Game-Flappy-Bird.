import pygame
import random
import sys

pygame.init()

# ================== SETTING ==================
WIDTH, HEIGHT = 400, 600
FPS = 60

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")
clock = pygame.time.Clock()

# ================== IMAGE ==================
bg_img = pygame.transform.scale(pygame.image.load("backround.jpg"), (WIDTH, HEIGHT))
bird_img = pygame.transform.scale(pygame.image.load("bird.png"), (50, 40))
pipe_img = pygame.transform.scale(pygame.image.load("pipe.png"), (70, 450))
star_img = pygame.transform.scale(pygame.image.load("star.png"), (30, 30))

# ================== BACKGROUND ==================
class Background:
    def __init__(self):
        self.x1 = 0
        self.x2 = WIDTH
        self.speed = 1

    def update(self):
        self.x1 -= self.speed
        self.x2 -= self.speed

        if self.x1 <= -WIDTH:
            self.x1 = WIDTH
        if self.x2 <= -WIDTH:
            self.x2 = WIDTH

    def draw(self):
        screen.blit(bg_img, (self.x1, 0))
        screen.blit(bg_img, (self.x2, 0))

# ================== BIRD ==================
class Bird:
    def __init__(self):
        self.x = 80
        self.y = HEIGHT // 2
        self.vel = 0
        self.gravity = 0.4
        self.jump = -8
        self.rect = bird_img.get_rect(center=(self.x, self.y))

    def flap(self):
        self.vel = self.jump

    def update(self):
        self.vel += self.gravity
        self.y += self.vel
        self.rect.center = (self.x, self.y)

    def draw(self):
        screen.blit(bird_img, self.rect)

    def dead(self):
        return self.y < 0 or self.y > HEIGHT - 50

# ================== PIPE ==================
class Pipe:
    def __init__(self, x):
        self.x = x
        self.gap = 220
        self.top_h = random.randint(120, HEIGHT - self.gap - 150)
        self.bottom_y = self.top_h + self.gap
        self.passed = False

        self.top_img = pygame.transform.flip(
            pygame.transform.scale(pipe_img, (70, self.top_h)), False, True
        )
        self.bottom_img = pygame.transform.scale(
            pipe_img, (70, HEIGHT - self.bottom_y)
        )

        self.top_rect = self.top_img.get_rect(topleft=(self.x, 0))
        self.bottom_rect = self.bottom_img.get_rect(topleft=(self.x, self.bottom_y))

    def update(self, speed):
        self.x -= speed
        self.top_rect.x = self.x
        self.bottom_rect.x = self.x

    def draw(self):
        screen.blit(self.top_img, self.top_rect)
        screen.blit(self.bottom_img, self.bottom_rect)

    def collide(self, bird):
        return bird.rect.colliderect(self.top_rect) or bird.rect.colliderect(self.bottom_rect)

    def offscreen(self):
        return self.x < -80

# ================== STAR ==================
class Star:
    def __init__(self, x):
        self.x = x
        self.y = random.randint(100, HEIGHT - 200)
        self.rect = star_img.get_rect(center=(self.x, self.y))
        self.taken = False

    def update(self, speed):
        self.x -= speed
        self.rect.center = (self.x, self.y)

    def draw(self):
        screen.blit(star_img, self.rect)

    def collide(self, bird):
        return self.rect.colliderect(bird.rect)

    def offscreen(self):
        return self.x < -50

# ================== TEXT ==================
def draw_text(text, size, x, y):
    font = pygame.font.Font(None, size)
    img = font.render(text, True, (0, 0, 0))
    screen.blit(img, img.get_rect(center=(x, y)))

# ================== MAIN ==================
def main():
    bg = Background()
    player = Bird()
    pipes = [Pipe(WIDTH + 200)]
    stars = []

    score = 0
    star_count = 0      # HITUNG JUMLAH BINTANG
    level = 1
    MAX_LEVEL = 10

    start = False
    game_over = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
                if game_over:
                    main()
                else:
                    start = True
                    player.flap()

        if start and not game_over:
            bg.update()
            player.update()

            if player.dead():
                game_over = True

            # ================= PIPE =================
            for p in pipes:
                p.update(2.5 + level * 0.3)

                if p.collide(player):
                    game_over = True

                if not p.passed and p.x < player.x:
                    p.passed = True
                    score += 1

            pipes = [p for p in pipes if not p.offscreen()]
            if pipes[-1].x < WIDTH - 250:
                pipes.append(Pipe(WIDTH))

            # ================= STAR =================
            if random.randint(1, 180) == 1:
                stars.append(Star(WIDTH + 50))

            for s in stars:
                s.update(2.5 + level * 0.2)

                if s.collide(player):
                    score += 5
                    star_count += 1
                    s.taken = True

                    # 5 BINTANG = NAIK 1 LEVEL
                    level = min((star_count // 5) + 1, MAX_LEVEL)

            stars = [s for s in stars if not s.offscreen() and not s.taken]

        # ================= DRAW =================
        bg.draw()

        for p in pipes:
            p.draw()
        for s in stars:
            s.draw()

        player.draw()

        draw_text(f"Score: {score}", 32, WIDTH // 2, 40)
        draw_text(f"Stars: {star_count}", 24, WIDTH // 2, 70)
        draw_text(f"Level: {level}", 24, WIDTH // 2, 100)

        if not start:
            draw_text("PRESS SPACE / CLICK", 28, WIDTH // 2, HEIGHT // 2)

        if game_over:
            draw_text("GAME OVER", 48, WIDTH // 2, HEIGHT // 2)

        pygame.display.update()
        clock.tick(FPS)

main()
