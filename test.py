import pygame as pg

pg.init()

clock = pg.time.Clock()
screen = pg.display.set_mode((500,500))


background = pg.transform.scale(pg.image.load("game pics/stina.pmg"),(500,500))

running = True
while running:
    clock.tick(30)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
    
    


    pg.display.flip()
