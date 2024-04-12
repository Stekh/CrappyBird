import pygame as pg
import random

pg.init()

SCREEN_WIDTH = 500
SCREEN_HEIGHT = 700
GRAVITY = 0.25


class Bird:
    def __init__(self):
        self.pos = [80, 400]
        self.vel = 0
        self.size = (30, 20)
        self.alive = True

    def update(self):
        self.vel += GRAVITY
        self.pos[1] += self.vel

        if self.pos[1] >= 650 - self.size[1]:
            self.pos[1] = 650 - self.size[1]
            self.alive = False
        elif self.pos[1] <= 0:
            self.pos[1] = 0

    def fly(self):
        self.vel = -25 * GRAVITY


class Pipe:
    def __init__(self, pos):
        self.slot_height = 150
        self.slot_pos = 50 + random.random() * (650 - self.slot_height * 2)
        self.pos = pos
        self.width = 80
        self.vel = 1.2
        self.passed = False

    def update(self):
        self.pos -= self.vel

        if self.pos <= 0 - self.width:
            self.pos = SCREEN_WIDTH
            self.slot_pos = 50 + random.random() * 450
            self.passed = False

    def crash(self, bird):
        if (bird.pos[0] + bird.size[0] >= self.pos and bird.pos[0] < self.pos + self.width and
           (bird.pos[1] < self.slot_pos or bird.pos[1] + bird.size[1] > self.slot_pos + self.slot_height)):
            bird.alive = False

    def scored(self, bird):
        if not self.passed:
            if bird.pos[0] > self.pos + self.width:
                self.passed = True
                return 1
        return 0


screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pg.display.set_caption("Crappy Bird")
clock = pg.time.Clock()
player = Bird()
score = 0
font = pg.font.Font(None, 80)
pipes = [Pipe(SCREEN_WIDTH), Pipe(SCREEN_WIDTH * 1.6)]

run = True
while run:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                if not player.alive:
                    player.__init__()
                    pipes = [Pipe(SCREEN_WIDTH), Pipe(SCREEN_WIDTH * 1.6)]
                    score = 0
                player.fly()

    pg.draw.rect(screen, (0, 150, 205), pg.Rect((0, 0, 500, 650)))
    pg.draw.rect(screen, (165, 42, 42), pg.Rect((0, 650, 500, 50)))

    for pipe in pipes:
        if player.alive:
            pipe.update()
        pipe.crash(player)
        score += pipe.scored(player)
        pg.draw.rect(screen, (5, 255, 50), pg.Rect((pipe.pos, 0, pipe.width, pipe.slot_pos)))
        pg.draw.rect(screen, (5, 255, 50), pg.Rect((pipe.pos, pipe.slot_pos + pipe.slot_height,
                     pipe.width, 651 - (pipe.slot_pos + pipe.slot_height))))

    player.update()
    pg.draw.rect(screen, (255, 255, 0), pg.Rect((player.pos[0], player.pos[1], player.size[0], player.size[1])))

    text = font.render(str(score), True, "black", None, 1000)
    text_block = text.get_rect()
    text_block.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 6)
    screen.blit(text, text_block)

    if not player.alive:
        restart_screen = pg.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        restart_screen.set_alpha(150)
        restart_screen.fill("white")
        screen.blit(restart_screen, (0, 0))
        restart = font.render("Press space to try again", True, "black", None, 400)
        restart_block = restart.get_rect()
        restart_block.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        screen.blit(restart, restart_block)

    pg.display.flip()
    clock.tick(60)

pg.quit()
