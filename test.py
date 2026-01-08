import pygame as pg
import math
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

def calculate_tape_point(mouse_displacement, point) -> tuple:
    
    displacement = mouse_displacement
    tapeLenght = math.hypot(*displacement)

    print(f"tapeLenght: {tapeLenght}")

    theta = math.asin(displacement[1] / tapeLenght)
    alpha = math.pi/2 - theta

    print(f"Theta: {theta} | Alpha: {alpha}")
    # print(f"Theta + Alpha = {theta + alpha} | pi/2: {math.pi/2}")

    dis_y = math.sin(alpha) * tapeWidth/2
    dis_x= math.cos(alpha) * tapeWidth/2
    
    if displacement[0] > 0:

        dis_x = -dis_x  # idk why but it fixes everything

    print(f"Displacement Y: {dis_y} , X: {dis_x}")

    new_y1 = int(point[1] + dis_y)
    new_x1 = int(point[0] + dis_x)

    new_y2 = int(point[1] - dis_y)
    new_x2 = int(point[0] - dis_x)

    return ((new_x1 , new_y1),(new_x2 , new_y2))
     

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
            
            init_click = mouse

        if event.type == pg.MOUSEBUTTONUP:

            if "unfinishedTapePoint" not in globals():

                initTapePoints = None
                init_click = None

            else:

                patches.append(unfinishedTapePoint)
                initTapePoints = None
                init_click = None

                hole_points_covered = hole_cover_check()

                print(f"covered:{sorted(hole_points_covered)}\nhole:{sorted(hole)}")

                if sorted(hole_points_covered) == sorted(hole):
                    print("PIPE FIXED!")
                    running = False


    if "init_click" in globals() and init_click != None:
        
        # print(f"{init_click[0]} - {mouse[0]} , {init_click[1]} - {mouse[1]} | init_x - cur_x , init_y - cur_y")
        mouse_displacement = ((mouse[0] - init_click[0]) , (mouse[1] - init_click[1]))
        print(f"mouse_displacement = {mouse_displacement}")

# OUTPUT

    screen.blit(background,(0,0))
    
    if "init_click" in globals() and init_click != None and mouse_displacement != (0,0) : # drawing unfinished tape
        
        initTapeSide = calculate_tape_point(mouse_displacement,init_click)
        curentTapeSide = calculate_tape_point(mouse_displacement , mouse)
        curentTapeSide = (curentTapeSide[1] , curentTapeSide[0])
        
        unfinishedTapePoint = initTapeSide + curentTapeSide
        
        print(f"unfinishedTapePoint: {unfinishedTapePoint}")
        pg.draw.polygon(screen,"gray",unfinishedTapePoint)
    
    blit_patches() 

    # blit_hole()

    pg.display.flip()

