import pygame as pg

pg.init()

clock = pg.time.Clock()
screen = pg.display.set_mode((500,500))



tapeWidth = 50
patches = []

hole = pg.Rect(166,283,80,80)

background = pg.transform.scale(pg.image.load("game pics/pipehole.png"),(500,500))

running = True
while running:
    clock.tick(30)
    
    mouse = pg.mouse.get_pos()

    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
        if event.type == pg.MOUSEBUTTONDOWN:
            print(f"mouse: {mouse}")
            initTapePoints = [(mouse[0] - tapeWidth / 2, mouse[1]),(mouse[0] + tapeWidth / 2 , mouse[1])]
        if event.type == pg.MOUSEBUTTONUP:
            pass
    
    screen.blit(background,(0,0))
    
    if "initTapePoints" in globals(): # drawing unfinished tape
        curentTapePoint = [(mouse[0] + tapeWidth / 2 , mouse[1]),(mouse[0] - tapeWidth / 2, mouse[1])]
        unfinishedTapePoint = initTapePoints + curentTapePoint
        
        print(f"unfinishedTapePoint: {unfinishedTapePoint}")
        
        if curentTapePoint != initTapePoints:
            pg.draw.polygon(screen,"gray",unfinishedTapePoint)
    


    pg.display.flip()
