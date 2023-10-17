from assets import Black, White
import pygame as pg

pg.init()
WIDTH = 1000
HEIGHT = 800
window = pg.display.set_mode([WIDTH, HEIGHT])
font = pg.font.Font("timesnewroman.ttf", 20)
big_font = pg.font.Font("timesnewroman.ttf", 50)
timer = pg.time.Clock()
fps = 60

run = True
while run:
    timer.tick(fps)
    window.fill("gray")

    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False

    pg.display.flip()
pg.quit()
