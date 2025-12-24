import pygame as pg
from game_funcs import point_in_triangle, triangle_area
pg.init()

clock = pg.time.Clock()
screen = pg.display.set_mode((500,500))



tapeWidth = 50
patches = [] #list for final tape polygon points

def blit_patches():
    for patch in patches: 
        pg.draw.polygon(screen,"gray",patch)

def hole_cover_check() -> list: 
    points_covered = []

    for patch in patches: # patch: [(x0,y0),(x1,y1),(x2,y2),(x3,y3)]

        trig1 = (patch[0],patch[1],patch[3])
        trig2 = (patch[1],patch[2],patch[3])

        for h_point in hole:
            
            if point_in_triangle(trig1[0],trig1[1],trig1[2],h_point) or point_in_triangle(trig2[0],trig2[1],trig2[2],h_point):
                
                if h_point not in points_covered:
                    points_covered.append(h_point)

                print(f"{points_covered} Covered")
    
    return points_covered
                


def blit_hole():
    for point in hole:
        pg.draw.circle(screen,"red",point,5)


# hole = pg.Rect(166,283,80,80)
hole = [(166,283),(246,283),(246,203),(190,203),(208,246)]
hole_points_covered = []

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
            patches.append(unfinishedTapePoint)
            initTapePoints = None

            hole_points_covered = hole_cover_check()

            print(f"covered:{sorted(hole_points_covered)}\nhole:{sorted(hole)}")

            if sorted(hole_points_covered) == sorted(hole):
                print("PIPE FIXED!")
                running = False


    screen.blit(background,(0,0))
    
    if "initTapePoints" in globals() and initTapePoints != None: # drawing unfinished tape
        curentTapePoint = [(mouse[0] + tapeWidth / 2 , mouse[1]),(mouse[0] - tapeWidth / 2, mouse[1])]
        unfinishedTapePoint = initTapePoints + curentTapePoint
        
        print(f"unfinishedTapePoint: {unfinishedTapePoint}")
        pg.draw.polygon(screen,"gray",unfinishedTapePoint)
    
    blit_patches() 
        
    blit_hole()

    pg.display.flip()



# TODO: 
# 1. tapes edges shold not be always horizontal they should be at angle to look at cursor when creating.
# 2. When hole is covered minigame is completed