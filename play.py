import pygame
import neat
import time
import os
import random
from bird import Bird
from pipe import Pipe
from base import Base

pygame.font.init()

WIN_WIDTH = 500
WIN_HEIGHT = 800

BG_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bg.png")))
STAT_FONT = pygame.font.SysFont("Comicsans", 70)


def draw_window(win, bird, pipes, base, score, lost, last_update):
    win.blit(BG_IMG, (0, 0))

    for pipe in pipes:
        pipe.draw(win)

    base.draw(win)

    bird.draw(win)

    if lost:
        lose_text = STAT_FONT.render("GAME OVER!!!!!!", 1, (255, 255, 255))
        win.blit(lose_text, (50, 250))


    if not last_update:
        text = STAT_FONT.render("Your Score is: " + str(score), 1, (255, 255, 255))
        win.blit(text, (WIN_WIDTH - 10 - text.get_width(), 10))
        pygame.display.update()

    if lost:
        return True
    else:
        return False


def main():
    bird = Bird(230, 250)
    base = Base(730)
    pipes = [Pipe(600)]
    lost = False
    last_update = False

    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    clock = pygame.time.Clock()

    score = int(0)

    runDMC = True
    while runDMC:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                runDMC = False
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird.jump()

        add_pipe = False
        rem = []
        for pipe in pipes:

            if pipe.collide(bird):
                lost = True

            if not pipe.passed and pipe.x < bird.x:
                pipe.passed = True
                add_pipe = True

            if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                rem.append(pipe)

            pipe.move()

        if add_pipe:
            score += 1

            pipes.append(Pipe(700))

        for r in rem:
            pipes.remove(r)

        if bird.y + bird.img.get_height() >= 730 or bird.y < 0:
            lost = True

        bird.move()
        base.move()
        last_update = draw_window(win, bird, pipes, base, score, lost, last_update)


if __name__ == "__main__":
    main()
