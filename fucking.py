import pygame as pg
import random
import math
from time import sleep
pg.init()
tales = 40
screen=pg.display.set_mode((tales*40,tales*25))
clock = pg.time.Clock()

pg.display.set_caption("Suchina")

Chickibamboni=pg.image.load("game pics/CHIKIBAMBONI(O.M.).png")

# Simple Object needs to be able to move and have only
# necessary parameters as coordinates and rect.

class GameObject():
	def __init__(self,x,y,w,h,speed,image_route,index = None,layer = 0):
		if image_route != None:

			self.image = pg.transform.scale(pg.image.load(image_route),(w,h))
			self.rect= self.image.get_rect()
			self.rect.x=x
			self.rect.y=y

		else:

			self.image = None
			self.rect = pg.Rect(x,y,w,h)
			self.rect.x = x
			self.rect.y = y


		self.image_route = image_route
		self.w=w
		self.h=h
		self.speed=speed
		self.index = index
		self.layer = layer

	def reload(self,image_route,x,y,w=tales,h=tales,speed=0):
		self.image_route = image_route
		self.image = pg.transform.scale(pg.image.load(image_route),(w,h))
		self.rect= self.image.get_rect()
		self.rect.x=x
		self.rect.y=y
		self.w=w
		self.h=h
		self.speed=speed

	def reset(self):
		screen.blit(self.image , (self.rect.x, self.rect.y))

	def reload_image(self):
		self.image = pg.transform.scale(pg.image.load(self.image_route),(self.w,self.h))

	# Target and move to target copied from player class to make non player objects able to move.

	def set_target(self,goingx,goingy, check_collisions = False):

		new_x = self.rect.x + goingx * tales
		new_y = self.rect.y + goingy * tales

		new_rect = pg.Rect(new_x, new_y,40,40)

		if not check_collisions:
			self.target = (new_x, new_y)
			return

		outside_top = new_y < 0
		outside_bottom = new_y >= screen.get_height()
		outside_right = new_x >= screen.get_width()
		outside_left = new_x < 0

		outside_screen = [outside_top , outside_bottom , outside_left , outside_right]

		# print(f"player outside screen = {outside_screen}")

		canceled = False # Making this global inside this def

		if any(o == True  for o in outside_screen):  # Gorgeous
			exitIndex = outside_screen.index(True)
			if self.allowed_exits[exitIndex]:
				travel("Rover",['Are you sure that you want to leave?'])
				return
			else:
				canceled = True



		collide_intobj2 = any(new_rect.colliderect(obj.rect) for obj in intObj if obj.int_mode == 2)
		collide_intobj3 = any(new_rect.colliderect(obj.rect) for obj in intObj if obj.int_mode == 3)
		collide_smalint2 = any(new_rect.colliderect(smint.rect) for smint in smallInt if smint.int_mode == 2)
		collide_smalint3 = any(new_rect.colliderect(smint.rect) for smint in smallInt if smint.int_mode == 3)
		collide_walls = any(new_rect.colliderect(w.rect) for w in walls )

		if not collide_walls and not collide_intobj2 and not collide_intobj3 and not collide_smalint2 and not collide_smalint3 and not canceled:
			self.target = (new_x, new_y)

	def move_to_target(self):
			final_x, final_y = self.target
			if final_x < self.rect.x:
				self.rect.x -= self.speed
				if self.rect.x <= final_x:
					self.rect.x = final_x
					self.target = None # Обнуляем цель после движения
			if final_x > self.rect.x:
				self.rect.x += self.speed
				if self.rect.x >= final_x:
					self.rect.x = final_x
					self.target = None # Обнуляем цель после движения
			if final_y < self.rect.y:
				self.rect.y -= self.speed
				if self.rect.y <= final_y:
					self.rect.y = final_y
					self.target = None # Обнуляем цель после движения
			if final_y > self.rect.y:
				self.rect.y += self.speed
				if self.rect.y >= final_y:
					self.rect.y = final_y
					self.target = None # Обнуляем цель после движения

# region functions

def check():
	if pg.key.get_pressed()[pg.K_c]:
		check = player.rect
		print (f"check: {check} ")

def string_divide(lst,s_lenght): #divide long text in several strings | made for interaction function
	for i in lst:
		text = i
	segments = [text[i:i+s_lenght] for i in range(0,len(text),s_lenght)] #nahui + zalupa + pizda + gandon + eblan

	return segments
def print_text(surface,text,font,size,x,y, colour = "white"):
	fontt = pg.font.SysFont(font,size)
	text = fontt.render(text, True, colour)

	surface.blit(text, (x,y))

def dialog_menu(dialogue, line_lenght,name,question):

	w =screen.get_width()
	h =screen.get_height()
	page = 0
	page_text = dialogue[page]
	fontName = pg.font.SysFont("Comic Sans", 55)
	fontTalk = pg.font.SysFont("Comic Sans", 55)
	#print(f"[DEBUG] name = {name} | type = {type(name)}")
	name_out = fontName.render(name, True ,"white")
	last = 0

	# Relative sizes and positions
	dialog_x = w * 0.0625
	dialog_y = h * 0.65
	dialog_width = w * 0.875
	dialog_height = h * 0.343


	# Name box (left side of dialog)
	name_box_x = dialog_x
	name_box_y = h * 0.575
	name_box_width = w * 0.25
	name_box_height = h * 0.075


	interaction = True

	while interaction:

		for event in pg.event.get():    # чекаем на евент закрытия игры. <3
			if event.type == pg.QUIT:
				pg.quit()               # Была ошибка что цикл не запускался потому что не было евентов. решение: не вставлять весь код в евенты


		now = pg.time.get_ticks() #Current time

		# Creating dialog surface and making it transparent
		dialog_surface = pg.Surface((w,h),pg.SRCALPHA)
		dialog_surface.fill((0,0,0,0))

		# Dialogue Box
		pg.draw.rect(dialog_surface, (15, 23, 42), [dialog_x, dialog_y, dialog_width, dialog_height])
		# Name Box
		pg.draw.rect(dialog_surface, ("gray"), [name_box_x, name_box_y, name_box_width, name_box_height])

		#Divide dialogue in several segments
		page_text = dialogue[page]
		strings = []

		i = 0
		while i < len(page_text): # text splitting section
			end = min(i + line_lenght, len(page_text))

			# Try to break on word boundary
			while end < len(page_text) and page_text[end - 1] not in (" ", ".") and end > i:
				end -= 1

			if end == i:  # Couldn't find a space, just hard split
				end = min(i + line_lenght, len(page_text))

			strings.append(page_text[i:end].strip())
			i = end


		line1=fontTalk.render(strings[0], True, "white") # What is person saying
		if len(strings)>1:
			line2=fontTalk.render(strings[1], True, "white")
		if len(strings)>2:
			line3=fontTalk.render(strings[2], True, "white")
		if len(strings)>3:
			line4=fontTalk.render(strings[3], True, "white")
		if len(strings)>4:
			line5=fontTalk.render(strings[4], True, "white")

		dialog_surface.blit(name_out, (name_box_x, name_box_y))
		dialog_surface.blit(line1, (dialog_x, dialog_y))
		if len(strings)>1:
			dialog_surface.blit(line2, (dialog_x, dialog_y+50))
		if len(strings)>2:
			dialog_surface.blit(line3, (dialog_x, dialog_y+100))
		if len(strings)>3:
			dialog_surface.blit(line4, (dialog_x, dialog_y+150))
		if len(strings)>4:
			dialog_surface.blit(line5, (dialog_x, dialog_y+200))

		if now - last >=250:

			#print("last =",last)
			if pg.key.get_pressed()[pg.K_f]:
				#screen.blit(dialogue[i+1], (w/2 - 700, h/2 + 150))
				if page < len(dialogue) - 1:
					#print("dialogue =", len(dialogue))
					page+=1

					last = pg.time.get_ticks()

				else:
					interaction = False

			if page == len(dialogue) - 1:
				if question == True:

					print_text(dialog_surface,"Y = yes, N = No","Comic Sans",40,w*0.39375, h*0.9)

					if pg.key.get_pressed()[pg.K_y]:


						return True

					if pg.key.get_pressed()[pg.K_n]:


						return False


		screen.blit(dialog_surface,(0,0))
		pg.display.flip()

def dot_distance(d1: tuple[int, int],d2: tuple[int, int]):
	distance = round(((d1[0] - d2[0])**2 + (d1[1] - d2[1])**2) ** 0.5)

	return distance

def triangle_area(tr1,tr2,tr3):

	trig_area = abs(tr1[0] * (tr2[1]-tr3[1]) +
					tr2[0] * (tr3[1]-tr1[1]) +
					tr3[0] * (tr1[1]-tr2[1])) / 2

	return trig_area

def point_in_triangle(tr1,tr2,tr3,point):

	# Main triangle area
	s = triangle_area(tr1,tr2,tr3)

	# Point triangles area
	s1 = triangle_area(tr1,tr2,point)
	s2 = triangle_area(tr1,point,tr3)
	s3 = triangle_area(point,tr2,tr3)

	# Check

	return abs((s1+s2+s3) - s) <0.01

def point_in_circle(point_x,point_y,center_x,center_y,radius):

	distance_square = (point_x-center_x)**2 + (point_y-center_y)**2

	return distance_square <= radius**2

# endregion Homeless functions

# region CLASSES

class Player(GameObject):
	def __init__(self, x, y, w, h, speed, image,):
		super().__init__(x, y, w, h, speed, image)

		self.direction = 0
		self.image = pg.transform.rotate(pg.transform.scale(pg.image.load(image),(tales,tales)), self.direction)
		self.target = None
		self.allowed_exits = [True,True,True,True]
		self.current_level = None
		self.last_level = None

	def in_front(self,obj_rect):

		if self.direction == 0: # E
			dir_rect = pg.Rect(self.rect.x+tales, self.rect.y,tales,tales)
		if self.direction == 90: # N
			dir_rect = pg.Rect(self.rect.x, self.rect.y - tales,tales,tales)
		if self.direction == 180: # W
			dir_rect = pg.Rect(self.rect.x-tales, self.rect.y,tales,tales)
		if self.direction == 270: # S
			dir_rect = pg.Rect(self.rect.x, self.rect.y + tales,tales,tales)

		if dir_rect.colliderect(obj_rect):
			return True
		else:
			return False

	def set_direction(self,dir_final: int) -> None:
		# in_dir + y = dir_final
		# y = dir_final - in_dir
		if self.direction != dir_final:
			# print(f"Wanted dir_final = {dir_final}")

			dir_change = dir_final - self.direction

			# print(f"in_dir + dir_change = dir_final: {self.direction} + {dir_change} = {dir_final}")

			self.direction = self.direction + dir_change


			self.image = pg.transform.rotate(self.image,dir_change)

			# print(f"Player dir: {self.direction}")

	def set_target(self,goingx,goingy):

		new_x = self.rect.x + goingx * tales
		new_y = self.rect.y + goingy * tales

		new_rect = pg.Rect(new_x, new_y,40,40)


		outside_top = new_y < 0
		outside_bottom = new_y >= screen.get_height()
		outside_right = new_x >= screen.get_width()
		outside_left = new_x < 0

		outside_screen = [outside_top , outside_bottom , outside_left , outside_right]

		# print(f"player outside screen = {outside_screen}")

		canceled = False # Making this global inside this def

		if any(o == True  for o in outside_screen):  # Gorgeous
			exitIndex = outside_screen.index(True)
			if self.allowed_exits[exitIndex]:
				travel("Rover",['Are you sure that you want to leave?'])
				return
			else:
				canceled = True



		collide_intobj2 = any(new_rect.colliderect(obj.rect) for obj in intObj if obj.int_mode == 2)
		collide_intobj3 = any(new_rect.colliderect(obj.rect) for obj in intObj if obj.int_mode == 3)
		collide_smalint2 = any(new_rect.colliderect(smint.rect) for smint in smallInt if smint.int_mode == 2)
		collide_smalint3 = any(new_rect.colliderect(smint.rect) for smint in smallInt if smint.int_mode == 3)
		collide_walls = any(new_rect.colliderect(w.rect) for w in walls )

		if not collide_walls and not collide_intobj2 and not collide_intobj3 and not collide_smalint2 and not collide_smalint3 and not canceled:
			self.target = (new_x, new_y)

	def move_to_target(self):
			final_x, final_y = self.target
			if final_x < self.rect.x:
				self.rect.x -= self.speed
				if self.rect.x <= final_x:
					self.rect.x = final_x
					self.target = None # Обнуляем цель после движения
			if final_x > self.rect.x:
				self.rect.x += self.speed
				if self.rect.x >= final_x:
					self.rect.x = final_x
					self.target = None # Обнуляем цель после движения
			if final_y < self.rect.y:
				self.rect.y -= self.speed
				if self.rect.y <= final_y:
					self.rect.y = final_y
					self.target = None # Обнуляем цель после движения
			if final_y > self.rect.y:
				self.rect.y += self.speed
				if self.rect.y >= final_y:
					self.rect.y = final_y
					self.target = None # Обнуляем цель после движения

	def controls(self):
		#
		global last, now


		# print(f"target: {self.target}")
		# print(f"player rect: {self.rect}")

		if self.target == None: # Проверяем что нету цели <3
			if pg.key.get_pressed()[pg.K_a]:
				self.set_direction(180)
				self.set_target(-1,0)
			elif pg.key.get_pressed()[pg.K_d]:
				self.set_direction(0)
				self.set_target(1, 0)
			elif pg.key.get_pressed()[pg.K_w]:
				self.set_direction(90)
				self.set_target(0, -1)
			elif pg.key.get_pressed()[pg.K_s]:
				self.set_direction(270)
				self.set_target(0, 1)



		if self.target:
			self.move_to_target()

	def teleport(self):
		mouse = pg.mouse.get_pos()
		for event in pg.event.get():
			if event == pg.MOUSEBUTTONDOWN:   # checking if mouse was pressed down
				x_tile = mouse[0] // tales        #Making coordinates able to move player on them correctly
				y_tile = mouse[1] // tales

				self.rect.x = x_tile     #Moving player
				self.rect.y = y_tile


class InteractionObj(GameObject):
	def __init__(self,name,dialogue, x, y, w, h, speed, image_route,line_lenght,int_mode,question,index = None):
		super().__init__(x, y, w, h, speed, image_route)
		self.fontName = pg.font.SysFont("Comic Sans", 55)
		self.fontTalk = pg.font.SysFont("Comic Sans", 55)
		self.name = name
		self.name_out=self.fontName.render(name, True, "white")
		self.int_mode =int(int_mode)
		self.dialogue=dialogue
		self.line_lenght=line_lenght
		self.question = question
		self.answer = None
		self.index = index
		self.times_activated = 0
		self.talked = 0



	def interaction(self):
		global last , string_divide, now, last

		if pg.key.get_pressed() [pg.K_e]:
			if now - last >= 100:
				for i in intObj:
					if i.int_mode == 1:
						if i.rect.colliderect(player.rect):
							print("INTERACTION!!!")
							if i.question == True:
								i.answer = dialog_menu(i.dialogue,i.line_lenght,i.name,i.question)
								print("Answer =", i.answer,f"[{i.index}]")

								if i.answer == True:
									i.times_activated += 1
									print (f"Times activated = {i.times_activated}")

							else:
								dialog_menu(i.dialogue,i.line_lenght,i.name,i.question)
								i.talked += 1


					if i.int_mode == 2:
						left = i.rect.x-tales <= player.rect.x < i.rect.x and i.rect.y == player.rect.y
						right = i.rect.x<player.rect.x <= i.rect.x + tales and i.rect.y == player.rect.y
						top = i.rect.y - tales <= player.rect.y <= i.rect.y and i.rect.x == player.rect.x
						bottom = i.rect.y <= player.rect.y <= i.rect.y + tales and i.rect.x == player.rect.x

						#print(f'''
	#left = {left}
	#right = {right}
	#top = {top}
	#bottom = {bottom}
	#''')

						if left or right or top or bottom:

							print("INTERACTION!!!")

							if i.question == True:
								i.answer = dialog_menu(i.dialogue,i.line_lenght,i.name,i.question)
								print("Answer =", i.answer, f"[{i.index}]")

								if i.answer == True:
									i.times_activated += 1
									print (f"Times activated = {i.times_activated}")

							else:
								dialog_menu(i.dialogue,i.line_lenght,i.name,i.question)
								i.talked += 1

					if i.int_mode == 3:
						if player.in_front(i.rect):

							print("INTERACTION!!!")

							if i.question == True:
								i.answer = dialog_menu(i.dialogue,i.line_lenght,i.name,i.question)
								print("Answer =", i.answer, f"[{i.index}]")

								if i.answer == True:
									i.times_activated += 1
									print (f"Times activated = {i.times_activated}")

							else:
								dialog_menu(i.dialogue,i.line_lenght,i.name,i.question)
								i.talked += 1

					last = pg.time.get_ticks()


				#if i.int_mode != 1 or i.int_mode != 2:
				#    print("WRONG INT_MODE!!!!!!")
	def using_item(self, item, amount):
		dialog_menu([f"Do you want to use {item} x{amount}?"],40,"Rover",True)

	def change(self,name,dialogue,image_route,line_lenght,int_mode,question,index = None,w = tales, h=tales):
		self.fontName = pg.font.SysFont("Comic Sans", 55)
		self.fontTalk = pg.font.SysFont("Comic Sans", 55)
		self.name = name
		self.name_out=self.fontName.render(name, True, "white")
		self.int_mode =int(int_mode)
		self.dialogue=dialogue
		self.line_lenght=line_lenght
		self.question = question
		self.answer = None
		self.index = index
		self.image_route = image_route
		self.image = pg.transform.scale(pg.image.load(image_route),(w,h))

class SmallInt():
	def __init__(self, int_mode,image_route,imagebig_route,x,y, simple_pic = True ,index = None, w = 800, h = 600, layer = 0 ):
		self.int_mode = int_mode
		self.index = index
		self.w = tales
		self.h = tales
		self.bigw = w
		self.bigh = h
		self.image_route = image_route
		self.image1 = pg.transform.scale(pg.image.load(self.image_route),(self.w,self.h))
		self.imagebig_route = imagebig_route
		self.imagebig = pg.transform.scale(pg.image.load(self.imagebig_route),(self.bigw,self.bigh))
		self.rect = self.image1.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.talked = 0
		self.simple_pic = simple_pic
		self.leftTop = None
		self.layer = layer

	def get_leftTopCords(self) -> tuple[float,float]:

		self.leftTop = (screen.get_width()/2 - 400, screen.get_height()/5)

		return self.leftTop

	def interaction(self):
		if self.int_mode == 1:
			if self.rect.colliderect(player.rect):
				if pg.key.get_pressed()[pg.K_e]:
					if self.simple_pic != True:
						print("SmallInt | Interaction 1")
						return True

		if self.int_mode == 2:
			left = self.rect.x-tales <= player.rect.x < self.rect.x and self.rect.y == player.rect.y
			right = self.rect.x<player.rect.x <= self.rect.x + tales and self.rect.y == player.rect.y
			top = self.rect.y - tales <= player.rect.y <= self.rect.y and self.rect.x == player.rect.x
			bottom = self.rect.y <= player.rect.y <= self.rect.y + tales and self.rect.x == player.rect.x

			# print(f" left = {left} \n right = {right} \n top = {top} \n bottom = {bottom}")


			if left or right or top or bottom:
				if pg.key.get_pressed()[pg.K_e]:
					if self.simple_pic != True:
						print ("SmallInt | Interaction 2")
						return True

		if self.int_mode == 3:
			if player.in_front(self.rect):

				if pg.key.get_pressed()[pg.K_e]:

					if self.simple_pic != True:
						print("SmallInt | Interaction 3")

						self.talked += 1

						return True
					
					else:
						interact = True
						while interact:
							for event in pg.event.get():
								if event.type == pg.QUIT:
									pg.quit
							screen.blit(self.imagebig,self.get_leftTopCords())
							if pg.key.get_pressed()[pg.K_f]:
								interact = False

							pg.display.flip()

	def new_imagebig(self,imagebig_route,w = 800,h = 600):

		self.imagebig_route = imagebig_route
		self.imagebig = pg.transform.scale(pg.image.load(self.imagebig_route),(self.bigw,self.bigh))

		self.bigw = w
		self.bigh = h

	def reset(self):
		screen.blit(self.image1 , (self.rect.x, self.rect.y))

	def reset_image_big(self):
		screen.blit(self.imagebig,self.get_leftTopCords())

class Item():
	def __init__(self, name, image_path, x ,y):
		self.name = name
		self.amount = 0
		self.w = 50
		self.h = 50
		self.image = pg.transform.scale(pg.image.load(image_path), (self.w,self.h))
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y


	def taking_item(self):
		answer = dialog_menu([f"Do you want to take {self.name}?"], 40, "Rover", True)

		if answer == True:
			inventory.increase(self.name)
	def reset(self):
		screen.blit(self.image , (self.rect.x, self.rect.y))

class IntItem(Item):
	def __init__(self, name, image_path, x, y, take_use,int_mode, max_amount, index = None):
		super().__init__(name, image_path, x, y)
		self.take_use = take_use
		self.int_mode = int_mode
		self.max_amount = max_amount
		self.used = 0
		self.w = tales
		self.h = tales
		self.image = pg.transform.scale(pg.image.load(image_path), (self.w,self.h))
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.index = index

	def get_give(self):
		if self.take_use == 1 and self.used != self.max_amount:

			answer = dialog_menu([f"Do you want to take {self.name}?"], 40, "Rover", True)

			if answer == True:
				inventory.increase(self.name)
				self.used += 1
		if self.take_use == 2:
			answer = dialog_menu([f"Do you want to use {self.name}?"], 40, "Rover", True)

			if answer == True:
				inventory.decrease(self.name)
				self.used += 1

class Inventory():
	def __init__(self):
		self.collectables = {
			"shovel" : Item("shovel",  "game pics/shovel_big.png",0,0), 
			"tea" : Item("tea", "game pics/tea.png",0,0),
			"key" : Item("key","game pics/key.png",0,0)
		}

		self.inventory_panel = [None] * 6

	def increase(self, name):
		try:
			self.collectables[name].amount += 1

			self.update_inventory()

			print(self.inventory_panel)
		except KeyError:
			print("increase failure")

	def decrease(self, name):
		try:
			self.collectables[name].amount -= 1

			self.update_inventory()

			print(self.inventory_panel)
		except KeyError:
			print("decrease failure")

	def get_amount(self,name):
		try:

			return self.collectables[name].amount

		except KeyError:
			return -1

	def update_inventory(self):
		# print("items =",self.collectables.items())
		for name, collectable in self.collectables.items():
			print("collectable =", collectable)
			if collectable.amount != 0 and collectable not in self.inventory_panel:
				self.inventory_panel.insert(self.inventory_panel.index(None), collectable)
				self.inventory_panel.remove(None)
			if collectable.amount == 0 and collectable in self.inventory_panel:
				self.inventory_panel.insert(self.inventory_panel.index(collectable), None)
				self.inventory_panel.remove(collectable)
	
	def draw_inventory(self):

		x = y = 60
		side = 80
		draw_step = 100
		inv_screen = pg.Surface(screen.get_size(),pg.SRCALPHA)
		inv_screen.fill((0,0,0,0))

		pg.draw.rect(inv_screen, "dark grey", (x-20, y-20, (side+20)*6 +20, side+40))
		print_text(inv_screen,"Inventory","Comic Sans", 35, (side+20)*6/2-50, y-50)

		for cell in self.inventory_panel:
			pg.draw.rect(inv_screen, (200, 215, 227), (x, y, side, side))

			if cell is not None:
				inv_screen.blit(cell.image, (x+15 , y+15))

				if cell.amount > 1:

					print_text(inv_screen,str(cell.amount), "Comic Sans" , 35 ,x+45 , y+40)

				if cell.amount == 0:

					cell is None

			x += draw_step

		screen.blit(inv_screen,(0,0))

	def inventory_cycle(self):
		global last
		if pg.key.get_pressed()[pg.K_TAB]:
			inventory_show = True
			while inventory_show:
				for ev in pg.event.get():
					if ev.type == pg.QUIT:
						pg.quit()

					inventory.draw_inventory()

					#if pg.key.get_pressed()[pg.K_1]:
					#    sleep(0.1)
					#    inventory.increase("shovel")



					if pg.key.get_pressed()[pg.K_ESCAPE]:
						inventory_show = False


					pg.display.flip()
					clock.tick(30)

inventory = Inventory()

class ScreenCollectable():
	def __init__(self,x,y,w,h,image_route,name):
		
		self.w = w
		self.h = h
		self.image_route = image_route
		self.image = pg.transform.scale(pg.image.load(self.image_route),(self.w, self.h))
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.name = name
		self.active = False
		self.max_collects = 1
		self.times_collected = 0 
		self.reached_max = False

	def reset(self):
		if self.reached_max == False and self.active: 
			screen.blit(screen,self.rect)
			
	def collect_when_clicked(self):
		if not self.active:
			return 
		
		if self.times_collected >= self.max_collects:
			self.reached_max = True
			return self.reached_max

		for event in pg.event.get():
			if event.type == pg.MOUSEBUTTONDOWN:
				
				mouse_pos = pg.mouse.get_pos()

				mouse_in_x = self.rect.x <= mouse_pos[0] <= (self.rect.x + self.w)
				mouse_in_y = self.rect.y <= mouse_pos[1] <= (self.rect.y + self.h)

				mouse_inside = mouse_in_x and mouse_in_y

				if mouse_inside:

					inventory.increase(self.name)
					self.times_collected += 1
					
					return self.reached_max



class Exit_zone():
	def __init__(self,x,y,w,h):

		self.rect = pg.rect.Rect(x,y,w,h)
		self.rect.x = x
		self.rect.y = y
		self.w = w
		self.h = h
		self.active = False

	def leave(self,text):
		return travel("Rover",text)


class Effect(GameObject): # a lot of thinking here | ebanina
	def __init__(self,x,y,w,h,speed, sprites: list, sizes_w = None,sizes_h = None,index = None,layer = 0):
		super().__init__(x,y,w,h,speed,None,index,layer)

		self.init_x = x
		self.init_y = y
		self.image = None
		self.anim_last = 0
		self.anim_turn = 0
		self.anim_loops_done = 0
		self.sprites = ["game pics/"+sprite for sprite in sprites]
		print(f"Effect animation: Sprites: {self.sprites} ")
		self.animation_finished = False

		if sizes_w == None: # creating lists of sizes of sprites

			self.sizes_w = [tales for _ in range(len(sprites))]

		else:
			self.sizes_w =  sizes_w


		if sizes_h == None:

			self.sizes_h = [tales for _ in range(len(sprites))]

		else:
			self.sizes_h = sizes_h

	def animation(self, speed = 1, times_max = 1) -> True:
		global now

		# Initializating variables

		last = self.anim_last
		turn = self.anim_turn
		times_done = self.anim_loops_done
		sprites = self.sprites

		delay = int(500 / speed)

		sizes_w = self.sizes_w
		sizes_h = self.sizes_h

		# print(f"Effect | times done: {times_done} < times max: {times_max}")
		if times_done < times_max:
			# print(f"Effect | Now: {now} - Last: {last} = {now-last} >= Delay: {delay}")
			if now-last >= delay:

				if turn != len(sprites):

					self.set_image_to_center(turn)
					self.anim_turn += 1
					self.anim_last = now

					print(f"Effect | Animation sprite changed ")

				else:
					self.anim_loops_done +=1
					self.anim_turn = 0

					print("Effect | Cycle of animation done")

		else:
			self.image = None   # Might have some errors because image wasnt suppose to be None

			self.animation_finished = True

			print("Effect animation finished")

			return self.animation_finished

	def run_animation (self, speed = 1, times_max = 1):

		if not self.animation_finished:
			self.animation(speed,times_max)

	def set_image_to_center(self,turn):
		if self.sizes_w[turn] == tales and self.sizes_h[turn] == tales:
			self.rect.x = self.init_x
			self.rect.y = self.init_y
			self.image = pg.transform.scale(pg.image.load(self.sprites[turn]),(self.sizes_w[turn],self.sizes_h[turn]))
			return
		else:
			print(f"Effects | intit_x + tales/2 - size_w/2 | {self.init_x} + {tales/2} - {self.sizes_w[turn]/2} | turn = {turn}")
			print(f"Effects | intit_y + tales/2 - size_w/2 | {self.init_y} + {tales/2} - {self.sizes_h[turn]/2} | turn = {turn}")
			self.rect.x = self.init_x + tales/2 - self.sizes_w[turn]/2
			self.rect.y = self.init_y + tales/2 - self.sizes_h[turn]/2
			print(f"Effects | x: {self.rect.x} y: {self.rect.y}")

			self.image = self.image = pg.transform.scale(pg.image.load(self.sprites[turn]),(self.sizes_w[turn],self.sizes_h[turn]))

class Wall(GameObject):
	def __init__(self, x, y, w, h, speed, image, angle = 0):
		super().__init__(x, y, w, h, speed, image)
		self.angle=angle
		self.image=pg.transform.rotate(self.image,self.angle)

# class Map():
#     def __init__(self,image,w,h,map_tales,layout):
#         self.image = pg.transform.scale(pg.image.load(image), (self.w , self.h))
#         self.map_tales = map_tales
#         self.w = w*map_tales
#         self.h = h*map_tales
#         self.layout = layout

# endregion Damn CLASSES

# region maps

karta = [
	'0000000000000000000000000000000000000000',
	'0000000000003000000000000000000000000000',
	'0000000000000000000000000000000000000000',
	'0005000000000000000000000000000000000000',
	'0000000000000000000000000000000000000000',
	'0000000000000000000000000000000000000000',
	'0000000000000000000000000000000000000000',
	'0000000000000000000000000000000000000000',
	'0000000000000000000000000000000000000000',
	'0000000000000000000000000111111111000000',
	'0000000000000000000000000100000001000000',
	'0000000000000000000000000100000001000000',
	'0000000000000000000000000100040001000000',
	'0000000000000000000000000100000001000000',
	'0000000000000000000000000100000001000000',
	'0000000000000000000000000100000001000000',
	'0000000000000000000000000111101111000000',
	'0000000000000000000000000000000000000000',
	'0000000000000000000000000000000000000000',
	'0000000000000000000000000000000000000000',
	'0000000000000000000000000000000000000000',
	'0000000000000000000000000000000000000000',
	'0000000000000000000000000000000000000000',
	'0000000000000000000000000000000000000000',
	'0000000000000000000000000000000000000000',
	'0000000000000000000000000000000000000000',
	]

karta1 = [
	'00000000,zzzzzzzzz999999999zzzzzzzzx0000',
	'00000000v5555555559mm..mmm955555555v0000',
	'00000000v55ud5fy55mmmmmmmi955535355v0000',
	'00000000v5555555559mmmmmmm955525255v0000',
	'00000000v55535355599999999955555555v0000',
	'00000000v55525255555555555555535355v0000',
	'00000000v55555555555fy5ud5555525255v0000',
	'00000000v55535355555555555555555555v0000',
	'00000000v55525255555fy5ud5555535355v0000',
	'00000000v55555555555555555555525255v0000',
	'00000000v555555555555tqb55555555555v0000',
	'00000000v555555555555gwn55555555555v0000',
	'00000000v55555555555555555555555555v0000',
	'00000000v55535355555fy5ud5555555555v0000',
	'00000000v55525255555555555555535355v0000',
	'00000000v55555555555fy5ud5555525255v0000',
	'00000000v55535355555555555555555555v0000',
	'00000000v5552525qb55555555555535p55v0000',
	'00000000v5555555wn5555555tqb5525l55v0000',
	'00000000v5553535555555555gwn5555555v0000',
	'00000000v55525255555555555555fy5ud5v0000',
	'00000000v55555555555555555555555555v0000',
	'00000000czzzzzzz[]zzzzzzzzzzzzzzzzzo0000',
	'0000000000007600000000760000007600000000',
	'0000000000000000000000000000000000000000',
]

chupep = [
	'0000000000000000100000000000000000000000',
	'0000000000000000110000000000000000000000',
	'0000000000000000110000000000000000000000',
	'0000000000000000110000001000000000000000',
	'0000000000000000100000001000000011000000',
	'0000000000000000110000000000000000000100',
	'0000000000000000100000001000000000000000',
	'0000000000000000110000000000000000000000',
	'0000000000000000110000001000001100000000',
	'1100000000000000110000001000000000000000',
	'0111111111111111100000000000000000000000',
	'0000000000000000000000001000000000000000',
	'0010001000100010010010000000000000011000',
	'0000000000000000000000000000000000000000',
	'0000000000000000000000000000000000000000',
	'0000000000000000000000000000000000000000',
	'0000000000000000000000000000000000000000',
	'1111111111111111111111111111111111111111',
	'0000000000000000000000000000000000000000',
	'0000000000000000000000000000000000000000',
	'0000000000000000000000000000000000000000',
	'0000000000000000000000000000000000000000',
	'0000000000000000000000000000000000000000',
	'0000000000000000000000000000000000000000',
	'0000000000000000000000000000000000000000',
	'0000000000000000000000000000000000000000',
	]

appartment = [
	"111111111111",
	"123000000041",
	"e000000000t1",
	"100000005011",
	"111101011011",
	"160001000011",
	"160001011111",
	"10779100b0c1",
	"1000110000c1",
	"188001000a11",
	"111111111111"
]
appartment_1 = [
	"111111111111",
	"123000000041",
	"e000000000t1",
	"100000005011",
	"111101011011",
	"160001000011",
	"160001011111",
	"10779100b0c1",
	"1000110000c1",
	"188001000n11",
	"111111111111"
]

basement_stasa = [
	'1111111111111111111111111',#1
	'1111111111111111111111111',#2
	'1111111111111111111111111',#3
	'11100000000010000c0000111',#4
	'1110000000001000000000111',#5
	'1110000000001000000000111',#6
	'1110000000001000000000111',#7
	'1110000000001000000000111',#8
	'1110000000001000000000000',#9
	'1110000000001000000000000',#10
	'1110000000001000000000111',#11
	'1110000000001000000000111',#12
	'1111111111221000000000111',#13
	'1110000000000000000000111',#14
	'1110000000000000000000111',#15
	'1110000000000000000000111',#16
	'1110000000000000000000111',#17
	'1110000000000000000000111',#18
	'1110000000000000000000111',#19
	'1110000000000000000000111',#20
	'1110000000000000000000111',#21
	'1110000000000000000000111',#22
	'1111111111001111111111111',#23
	'1111111111001111111111111',#24
	'1111111111001111111111111',#25
	]

basement_yura = [
	"1"*20,
	"11111111111678911111",
	"11111101000000000j11",
	"11000000000000000011",
	"10000000000000000011",
	"10000000000000000011",
	"00000000000011110011",
	"00000000000011110011",
	"10000000000011110011",
	"10000000000000000011",
	"11000000000000000111",
	"11100111110000001111",
	"11111111111234511111",
	"11111111111111111111"
]

levels = [karta1,chupep,appartment,appartment_1,basement_stasa,basement_yura]
startLevel = 5
choosenLevel = levels[startLevel]
# print("CL =",startLevel)
effects = []
floor=[]
walls=[]
intObj=[]
item=[]
smallInt = []
screenCollectables = []

map_app = pg.transform.scale(pg.image.load("game pics/appartment_map.png"),(12*tales,11*tales))
map_chupep = pg.transform.scale(pg.image.load("game pics/chupep.png"),screen.get_size())
map_stas_low = pg.transform.scale(pg.image.load("game pics/karta_stasa_low.png"),(45*25,45*25))
map_stas_up = pg.transform.scale(pg.image.load("game pics/karta_stasa_up.png"),(45*25,45*25))
map_yura_low = pg.transform.scale(pg.image.load("game pics/basement_yura_low.png"),(60*20,60*14))
map_yura_up = pg.transform.scale(pg.image.load("game pics/basement_yura_up.png"),(60*20,60*14))

togo_levels = None

# endregion maps

def map(kostil = None, up = None):
	global tales, screen, map_app

	if kostil == None and up == None:
		print ("**| map |**")
		if choosenLevel == karta:
			print ("map | CL = karta")
			for i in range(len(karta)):
				#print("i =", i)
				for g in range(len(karta[i])):
					#print("g =", g)
					if karta[i][g]=="1":
						walls.append(Wall(g*tales,i*tales,tales,tales,0,"game pics/brick_wall.png",0))
					if karta[i][g]=="0":
						floor.append(GameObject(g*tales,i*tales,tales,tales,0,"game pics/трава.png"))
					if karta[i][g]=="3":
						intObj.append(InteractionObj("Rover",["Im useless dog, gav gav gav gav gav gav gav gav", "Dima piska"],g*tales,i*tales,tales,tales,0,"game pics/InteractionObj.png", 25,2,False))
					if karta[i][g]=="4":
						intObj.append(InteractionObj("Rover",["Im inside a house", "it`s not my house","dima pisun"],g*tales,i*tales,tales,tales,0,"game pics/InteractionObj.png", 25,1,True))
					if karta[i][g]=="5":
						intObj.append(InteractionObj("Rover",["fucking"],g*tales,i*tales,tales,tales,0,"game pics/InteractionObj.png",25,3,False))
		if choosenLevel == karta1:
			player.target = None
			player.set_direction(90)
			player.rect.x , player.rect.y =(tales*16,tales*21)

			print ("map | CL = karta1")
			for i in range(len(karta1)):
				#print("i =", i)
				for g in range(len(karta1[i])):
					#print("g =", g)
					if karta1[i][g]=="1":
						walls.append(Wall(g*tales,i*tales,tales,tales,0,"game pics/brick_wall.png",0))
					if karta1[i][g]=="0":
						if random.randint(0,1) == 1:
							floor.append(GameObject(g*tales,i*tales,tales,tales,0,"game pics/трава.png"))
						else:
							floor.append(GameObject(g*tales,i*tales,tales,tales,0,"game pics/trava1.png"))
					if karta1[i][g]=="2":
						walls.append(GameObject(g*tales,i*tales,tales,tales,0,"game pics/mm2.png"))
					if karta1[i][g]=="3":
						walls.append(GameObject(g*tales,i*tales,tales,tales,0,"game pics/mm.png"))
					if karta1[i][g]=="5":
						if random.randint(0,1) == 1:
							floor.append(GameObject(g*tales,i*tales,tales,tales,0,"game pics/tihaTravapng.png"))
						else:
							floor.append(GameObject(g*tales,i*tales,tales,tales,0,"game pics/tihaTrava1.png"))
					if karta1[i][g]=="6":
						walls.append(GameObject(g*tales,i*tales,tales,tales,0,"game pics/pollavkiR.png"))
					if karta1[i][g]=="7":
						walls.append(GameObject(g*tales,i*tales,tales,tales,0,"game pics/pollavkiL.png"))
					if karta1[i][g]=="u":
						walls.append(Wall(g*tales,i*tales,tales,tales,0,"game pics/mm.png",90))
					if karta1[i][g]=="d":
						walls.append(Wall(g*tales,i*tales,tales,tales,0,"game pics/mm2.png",90))
					if karta1[i][g]=="y":
						walls.append(Wall(g*tales,i*tales,tales,tales,0,"game pics/mm.png",-90))
					if karta1[i][g]=="f":
						walls.append(Wall(g*tales,i*tales,tales,tales,0,"game pics/mm2.png",-90))
					if karta1[i][g]=="p":
						mo=InteractionObj("Rover",["Bury a grave?"],g*tales,i*tales,tales,tales,0,"game pics/mo.png",40,3,True)
						intObj.append(mo)
						mo_ind = intObj.index(mo)
						#print(mo_ind)
					if karta1[i][g]=="l":
						mo2=InteractionObj("Rover",["Bury a grave?"],g*tales,i*tales,tales,tales,0,"game pics/mo_down.png",40,3,True)
						intObj.append(mo2)
						mo2_ind = intObj.index(mo2)
						#print(mo2_ind)
					if karta1[i][g]=="9":
						walls.append(GameObject(g*tales,i*tales,tales,tales,0,"game pics/stinka.png"))
					if karta1[i][g]=="i":
						item.append(IntItem("shovel","game pics/Shovel_floor.png",g*tales,i*tales,1,1,1,"shovel"))
					if karta1[i][g]=="9":
						walls.append(GameObject(g*tales,i*tales,tales,tales,0,"game pics/stinka.png"))
					if karta1[i][g]=="m":
						floor.append(GameObject(g*tales,i*tales,tales,tales,0,"game pics/pidloga1.png",))
					if karta1[i][g]=="q":
						walls.append(Wall(g*tales,i*tales,tales,tales,0,"game pics/stil copy.png",90))
					if karta1[i][g]=="w":
						walls.append(Wall(g*tales,i*tales,tales,tales,0,"game pics/stil copy2.png",90))
					if karta1[i][g]=="b":
						walls.append(Wall(g*tales,i*tales,tales,tales,0,"game pics/pollavkiL.png",-90))
					if karta1[i][g]=="n":
						walls.append(Wall(g*tales,i*tales,tales,tales,0,"game pics/pollavkiR.png",-90))
					if karta1[i][g]=="t":
						walls.append(Wall(g*tales,i*tales,tales,tales,0,"game pics/pollavkiR.png",90))
					if karta1[i][g]=="g":
						walls.append(Wall(g*tales,i*tales,tales,tales,0,"game pics/pollavkiL.png",90))
					if karta1[i][g]=="z":
						walls.append(Wall(g*tales,i*tales,tales,tales,0,"game pics/zaborchik.png",0))
					if karta1[i][g]=="o":
						walls.append(Wall(g*tales,i*tales,tales,tales,0,"game pics/angle_zaborchik.png",0))
					if karta1[i][g]=="v":
						walls.append(Wall(g*tales,i*tales,tales,tales,0,"game pics/front_zaborchik.png",0))
					if karta1[i][g]=="x":
						walls.append(Wall(g*tales,i*tales,tales,tales,0,"game pics/up_angle_zaborchik.png",0))
					if karta1[i][g]=="c":
						walls.append(Wall(g*tales,i*tales,tales,tales,0,"game pics/left_angle_zaborchik.png",0))
					if karta1[i][g]==",":
						walls.append(Wall(g*tales,i*tales,tales,tales,0,"game pics/left_up_angle_zaborchik.png",0))
					if karta1[i][g]==".":
						smallInt.append(SmallInt(3,"game pics/grave_on_the_floor.png","game pics/CHIKIBAMBONI(O.M.).png",g*tales,i*tales,True))
					if karta1[i][g]=="[":
						intObj.append(InteractionObj("Rover",["I cant leave yet"],g*tales,i*tales,tales,tales,0,"game pics/zaborl.png",30,3,False,"exit"))
					if karta1[i][g]=="]":
						intObj.append(InteractionObj("Rover",["I cant leave yet"],g*tales,i*tales,tales,tales,0,"game pics/zaborr.png",30,3,False,"exit"))

		if choosenLevel == chupep:
			print ("map | CL = supertest33")

			player.target = None
			player.rect.x , player.rect.y =(tales,tales*14)
			player.allowed_exits = [True,False,False,False]

			screen.blit(map_chupep,(0,0,screen.get_width(),screen.get_height()))
			for i in range(len(chupep)):
				for g in range(len(chupep[i])):
					if chupep[i][g] == "0":
						floor.append(GameObject(g*tales,i*tales,tales,tales,0,"game pics/nothing.png"))
					if chupep[i][g] == "1":
						walls.append(Wall(g*tales,i*tales,tales,tales,0,"game pics/nothing.png",0))
			# else:
			#     print("map | CL not defined")
			#     print("map | CL =",choosenLevel)

		if choosenLevel == appartment:
			# Changing screen parameters for this one

			tales = 80
			screen = pg.display.set_mode((tales*12,tales*11))
			map_app = pg.transform.scale(pg.image.load("game pics/appartment_map.png"),(12*tales,11*tales))

			player.target = None
			# player.rect.x , player.rect.y =(tales, tales*2)
			player.__init__(tales,tales*2,tales,tales,tales/8,"game pics/avatar.png")


			print("map | CL = appartment")
			screen.blit(map_app,(0,0,12*tales,11*tales))
			for i in range(len(appartment)):
				for g in range(len(appartment[i])):
					if appartment[i][g] == "0":
						floor.append(GameObject(g*tales,i*tales,tales,tales,0,"game pics/nothing.png"))
					if appartment[i][g] == "1":
						walls.append(Wall(g*tales,i*tales,tales,tales,0,"game pics/nothing.png",0))
					if appartment[i][g] == "2":
						intObj.append(InteractionObj("Coat rack",["Coat rack"],g*tales,i*tales,tales,tales,0,"game pics/nothing.png",30,3,False))
					if appartment[i][g] == "3":
						intObj.append(InteractionObj("Rover",["Here is my keys","Dont need them now"],g*tales,i*tales,tales,tales,0,"game pics/nothing.png",30,3,False,"keys"))
					if appartment[i][g] == "4":
						intObj.append(InteractionObj("Fridge",["*Fridge sounds*"],g*tales,i*tales,tales,tales,0,"game pics/nothing.png",30,3,False))
					if appartment[i][g] == "5":
						intObj.append(InteractionObj("Rover",["Notebook on kitchen table -_-"],g*tales,i*tales,tales,tales,0,"game pics/nothing.png",30,3,False))
					if appartment[i][g] == "6":
						intObj.append(InteractionObj("Rover",["Sleeping bag.","I sleep here","Go to sleep?"],g*tales,i*tales,tales,tales,0,"game pics/nothing.png",30,1,True,"sleep")) # Do you want to sleep? after those
					if appartment[i][g] == "7":
						intObj.append(InteractionObj("Rover",["Jacket on the floor.","Wasnt wearing it since yesterday"],g*tales,i*tales,tales,tales,0,"game pics/nothing.png",30,1,False))
					if appartment[i][g] == "8":
						intObj.append(InteractionObj("Rover",["Wardrobe.","Not much in there"],g*tales,i*tales,tales,tales,0,"game pics/nothing.png",30,3,False))
					if appartment[i][g] == "9":
						intObj.append(InteractionObj("Rover",["Radio.","..."],g*tales,i*tales,tales,tales,0,"game pics/nothing.png",30,3,False))
					if appartment[i][g] == "a":
						intObj.append(InteractionObj("Rover",["Toilet."],g*tales,i*tales,tales,tales,0,"game pics/nothing.png",30,3,False))
					if appartment[i][g] == "b":
						intObj.append(InteractionObj("Rover",["the sink and mirror (that u cant see)"],g*tales,i*tales,tales,tales,0,"game pics/nothing.png",30,3,False))
					if appartment[i][g] == "c":
						intObj.append(InteractionObj("Rover",["Bath."],g*tales,i*tales,tales,tales,0,"game pics/nothing.png",30,3,False))
					if appartment[i][g] == "t":
						intObj.append(InteractionObj("Rover",["Make tea?"],g*tales,i*tales,tales,tales,0,"game pics/nothing.png",30,3,True, "tea"))
					if appartment[i][g] == "e":
						intObj.append(InteractionObj("Rover",["I dont want to leave yet"],g*tales,i*tales,tales,tales,0,"game pics/nothing.png",30,3,False, "exit"))

		if choosenLevel == appartment_1:
			# Changing screen parameters for this one

			tales = 80
			screen = pg.display.set_mode((tales*12,tales*11))
			map_app = pg.transform.scale(pg.image.load("game pics/appartment_map.png"),(12*tales,11*tales))

			player.target = None



			print("map | CL = appartment_1") # fucking
			screen.blit(map_app,(0,0,12*tales,11*tales))
			for i in range(len(appartment_1)):
				for g in range(len(appartment_1[i])):
					if appartment_1[i][g] == "0":
						floor.append(GameObject(g*tales,i*tales,tales,tales,0,"game pics/nothing.png"))
					if appartment_1[i][g] == "1":
						walls.append(Wall(g*tales,i*tales,tales,tales,0,"game pics/nothing.png",0))
					if appartment_1[i][g] == "2":
						intObj.append(InteractionObj("Coat rack",["Coat rack"],g*tales,i*tales,tales,tales,0,"game pics/nothing.png",30,3,False))
					if appartment_1[i][g] == "3":
						intObj.append(InteractionObj("Rover",["Here is my keys","Dont need them now"],g*tales,i*tales,tales,tales,0,"game pics/nothing.png",30,3,False,"keys"))
					if appartment_1[i][g] == "4":
						intObj.append(InteractionObj("Fridge",["*Fridge sounds*"],g*tales,i*tales,tales,tales,0,"game pics/nothing.png",30,3,False))
					if appartment_1[i][g] == "5":
						intObj.append(InteractionObj("Rover",["Notebook on kitchen table -_-"],g*tales,i*tales,tales,tales,0,"game pics/nothing.png",30,3,False))
					if appartment_1[i][g] == "6":
						intObj.append(InteractionObj("Rover",["Sleeping bag.","I sleep here"],g*tales,i*tales,tales,tales,0,"game pics/nothing.png",30,1,False)) # Do you want to sleep? after those
					if appartment_1[i][g] == "7":
						intObj.append(InteractionObj("Rover",["Jacket on the floor.","Wasnt wearing it since yesterday"],g*tales,i*tales,tales,tales,0,"game pics/nothing.png",30,1,False))
					if appartment_1[i][g] == "8":
						intObj.append(InteractionObj("Rover",["Wardrobe.","Not much in there"],g*tales,i*tales,tales,tales,0,"game pics/nothing.png",30,3,False))
					if appartment_1[i][g] == "9":
						intObj.append(InteractionObj("Rover",["Radio.","..."],g*tales,i*tales,tales,tales,0,"game pics/nothing.png",30,3,False))
					if appartment_1[i][g] == "n":
						intObj.append(InteractionObj("Rover",["Toilet."],g*tales,i*tales,tales,tales,0,"game pics/nothing.png",30,3,False))
					if appartment_1[i][g] == "b":
						intObj.append(InteractionObj("Rover",["....","*no water*","??","damn it, probably something in basement something again",],g*tales,i*tales,tales,tales,0,"game pics/nothing.png",30,3,False,"sink"))
					if appartment_1[i][g] == "c":
						intObj.append(InteractionObj("Rover",["Bath."],g*tales,i*tales,tales,tales,0,"game pics/nothing.png",30,3,False))
					if appartment_1[i][g] == "t":
						intObj.append(InteractionObj("Rover",["Make tea?"],g*tales,i*tales,tales,tales,0,"game pics/nothing.png",30,3,True, "tea"))
					if appartment_1[i][g] == "e":
						intObj.append(InteractionObj("Rover",["Its so early, I dont want to go anywhere"],g*tales,i*tales,tales,tales,0,"game pics/nothing.png",30,3,False, "exit"))

		if choosenLevel == basement_stasa:
			global togo_levels

			tales = 45
			screen = pg.display.set_mode((tales*25,tales*25))
			print(f"screen = {screen.get_size()}")

			if player.last_level == 5:
				player.__init__(tales*24,tales*9,tales,tales,tales/8,"game pics/avatar.png")
				player.set_direction(180)

			else:
				player.__init__(tales*11,tales*24,tales,tales,tales/8,"game pics/avatar.png")
				player.set_direction(90)
			player.allowed_exits = [False,False,False,True]



			togo_levels = None

			print("map | CL = basement stasa")

			screen.blit(map_stas_low,(0,0,tales*25,tales*25))

			for i in range(len(basement_stasa)):
				for g in range(len(basement_stasa[i])):

					if basement_stasa[i][g] == "0":
						floor.append(GameObject(g*tales,i*tales,tales,tales,0,"game pics/nothing.png"))
					if basement_stasa[i][g] == "1":
						walls.append(Wall(g*tales,i*tales,tales,tales,0,"game pics/nothing.png"))
						# print(f"i = {i}, g = {g}")
					if basement_stasa[i][g] == "2":
						intObj.append(InteractionObj("Rover",["Closed..."],g*tales,i*tales,tales,tales,0,"game pics/nothing.png",40,3,False,"dooor"))
					if basement_stasa[i][g] == "c":
						smallInt.append(SmallInt(3,"game pics/nothing.png","game pics/zzzamok.png",tales*g,tales*i,False, "chest"))

		if choosenLevel == basement_yura:


			tales = 60
			screen = pg.display.set_mode((tales*20, tales*14))


			player.__init__(0,tales*7,tales,tales,tales/8,"game pics/avatar.png")
			player.set_direction(0)
			player.allowed_exits = [False,False,True,False]

			print("map | CL = basement yura")

			screen.blit(map_yura_low,(0,0,tales*20,tales*14))

			togo_levels = basement_stasa

			print (f"togo_levels during map = {togo_levels}")

			for i in range(len(basement_yura)):
				for g in range(len(basement_yura[i])):

					if basement_yura[i][g] == "0":
						floor.append(GameObject(g*tales,i*tales,tales,tales,0,"game pics/nothing.png"))
					if basement_yura[i][g] == "1":
						walls.append(Wall(g*tales,i*tales,tales,tales,0,"game pics/nothing.png"))
					if basement_yura[i][g] == "2":
						intObj.append(InteractionObj("Rover",["Pull the lever?"],g*tales,i*tales,tales,tales,0,"game pics/lever_down.png", 40,3,True,"lever1"))
					if basement_yura[i][g] == "3":
						intObj.append(InteractionObj("Rover",["Pull the lever?"],g*tales,i*tales,tales,tales,0,"game pics/lever_down.png", 40,3,True,"lever2"))
					if basement_yura[i][g] == "4":
						intObj.append(InteractionObj("Rover",["Pull the lever?"],g*tales,i*tales,tales,tales,0,"game pics/lever_down.png", 40,3,True,"lever3"))
					if basement_yura[i][g] == "5":
						intObj.append(InteractionObj("Rover",["Pull the lever?"],g*tales,i*tales,tales,tales,0,"game pics/lever_down.png", 40,3,True,"lever4"))
					if basement_yura[i][g] == "6":
						walls.append(GameObject(g*tales,i*tales,tales,tales,0,"game pics/lamp_off.png","lamp1"))
					if basement_yura[i][g] == "7":
						walls.append(GameObject(g*tales,i*tales,tales,tales,0,"game pics/lamp_off.png","lamp2"))
					if basement_yura[i][g] == "8":
						walls.append(GameObject(g*tales,i*tales,tales,tales,0,"game pics/lamp_off.png","lamp3"))
					if basement_yura[i][g] == "9":
						walls.append(GameObject(g*tales,i*tales,tales,tales,0,"game pics/lamp_off.png","lamp4"))
					if basement_yura[i][g] == "j":
						walls.append(GameObject(g*tales,i*tales,tales,tales,0,"game pics/frog.png","frog",1))
						effects.append(Effect(g*tales,i*tales,tales,tales,0,["boom1.png","boom2.png","boom3.png","boom4.png"],sizes_w=[30,40,60,80],sizes_h=[30,40,60,80],index = "exp",layer = 1))

	if kostil != None:
		# Fixes the bug with player model on appartment map

		if choosenLevel == appartment or choosenLevel == appartment_1:

			# print("map | kostil found")
			screen.blit(map_app,(0,0,12*tales,11*tales))

		if choosenLevel == chupep:

			screen.blit(map_chupep,(0,0,screen.get_width(),screen.get_height()))

		if choosenLevel == basement_stasa:

			screen.blit(map_stas_low,(0,0,screen.get_width(),screen.get_height()))

		if choosenLevel == basement_yura:

			screen.blit(map_yura_low,(0,0,screen.get_width(),screen.get_height()))

		for w in walls:
			if w.image_route != "game pics/nothing.png" and w.layer == 0:
				w.reset()
		for obj in intObj:
			if obj.image_route != "game pics/nothing.png" and obj.layer == 0:
				obj.reset()
		for smol in smallInt:
			if smol.image_route != "game pics/nothing.png" and smol.layer == 0:
				smol.reset()
		for effect in effects:
			if effect.image != None and effect.layer == 0:
				effect.reset()
		for f in floor:
			if f.layer == 0:
				f.reset()




	# print(f"level1progress = {level1progress}")

	if up != None:
		if choosenLevel == basement_yura:

			screen.blit(map_yura_up,(0,0,screen.get_width(),screen.get_height()))


		if choosenLevel == basement_stasa:

			screen.blit(map_stas_up,(0,0,45*25,45*25))

		for w in walls:
			if w.image_route != "game pics/nothing.png" and w.layer == 1:
				w.reset()
		for obj in intObj:
			if obj.image_route != "game pics/nothing.png" and obj.layer == 1:
				obj.reset()
		for smol in smallInt:
			if smol.image_route != "game pics/nothing.png" and smol.layer == 1:
				smol.reset()
		for effect in effects:
			if effect.image != None and effect.layer == 1:
				effect.reset()
		for f in floor:
			if f.layer == 1:
				f.reset()

				# KARTI VRUCNUYU PISAT | POTOMUChTO DAUN

player = Player(tales,tales,tales,tales,tales/8,"game pics/avatar.png")
#player = Player(tales,tales,tales,tales,tales,"rover.png")



def travel(name = None,dialogue = None, record=True )->None: #travel on other level
	global last, choosenLevel, startLevel


	if player.target is None: # Checking that the player stands still

		print(f"togo_levels in Travel {togo_levels}")

		if togo_levels != None:

			answer = dialog_menu(dialogue,40,name,True)

			if answer == True:

				print("travel through togo levels")

				togo_index = levels.index(togo_levels)

				print(f"togo index = {togo_index}")

				choosenLevel= levels[togo_index]

				print(f"travel | startLevel = {startLevel}")

				old_startLevel = startLevel # recording the last start level

				startLevel = togo_index

				print(f"travel | new startLevel = {startLevel}")

				floor.clear()
				walls.clear()
				intObj.clear()
				item.clear()
				smallInt.clear()

				print("travel | map lists cleared")

				screen.fill("black")

				if record == True:
					player.current_level = startLevel
					player.last_level = old_startLevel

					print(f"Player current level = {player.current_level}")
					print(f"Player last level = {player.last_level}")


				map()
				return

		if startLevel + 1 < len(levels):


			print("travel func began")
			if dialogue != None and name != None:

				print("ASKING TRAVEL:")

				answer = dialog_menu(dialogue,40,name,True)

				print("travel answ =", answer)

				if answer == True:
					print("travel | startlevel =", startLevel)

					old_startLevel = startLevel
					startLevel += 1

					print("travel | new startlevel =", startLevel)

					choosenLevel = levels[startLevel]

					# print("travel | CL =",choosenLevel)

					floor.clear()
					walls.clear()
					intObj.clear()
					item.clear()
					smallInt.clear()

					print("travel | map lists cleared")

					screen.fill("black")

					if record == True:
						player.current_level = startLevel
						player.last_level = old_startLevel

						print(f"Player current level = {player.current_level}")
						print(f"Player last level = {player.last_level}")

					map()

				# print("travel | map began")
			else:
				print("FORCE TRAVEL:")
				print("travel | startlevel =", startLevel)

				old_startLevel = startLevel
				startLevel += 1

				print("travel | new startlevel =", startLevel)

				choosenLevel = levels[startLevel]

				# print("travel | CL =",choosenLevel)

				floor.clear()
				walls.clear()
				intObj.clear()
				item.clear()
				smallInt.clear()

				print("travel | map lists cleared")

				screen.fill("black")

				if record == True:
					player.current_level = startLevel
					player.last_level = old_startLevel

					print(f"Player current level = {player.current_level}")
					print(f"Player last level = {player.last_level}")

				map()


			if player.rect.y >= screen.get_height():
				player.rect.y -= tales
			if player.rect.y < 0:
				player.rect.y += tales
			if player.rect.x >= screen.get_width():
				player.rect.x -= tales
			if player.rect.x < 0:
				player.rect.x += tales






				pg.display.flip()
				return True
		else:
			# print("travel | ran out of levels")
			if player.rect.y >= screen.get_height():
				player.rect.y -= tales
			if player.rect.y < 0:
				player.rect.y += tales
			if player.rect.x >= screen.get_width():
				player.rect.x -= tales
			if player.rect.x < 0:
				player.rect.x += tales

			return False


class Button():
	def __innit__(self,x,y,w,h,text,color,font,fontSize):
		self.rect.x = x
		self.rect.y = y
		self.w = screen.get_width()
		self.h = screen.get_height()
		self.color= (color)
		self.font=pg.font.SysFont(font,fontSize)
		self.text= font.render(text, True, color)
		pass

def menu():
	global controls_show
	menu_bgr=pg.image.load("game pics/menu.png")
	controls_pic = pg.image.load("game pics/Controls.png")
	font=pg.font.SysFont('Comic Sans', 55)
	color_text=(255,255,255)
	t_quit = font.render('Quit', True , color_text)
	t_start = font.render('Start', True , color_text)
	t_controls = font.render('Controls', True, color_text)
	t_quit.get_rect()
	w=screen.get_width()
	h=screen.get_height()

	menuShow=True
	while menuShow:
		for event in pg.event.get():
			if event.type == pg.QUIT:
				pg.quit()

		screen.blit(menu_bgr, (0,0))
		# screen.fill((62,123,39))
		mouse=pg.mouse.get_pos()
		# Check where mouse was presseed
		if event.type == pg.MOUSEBUTTONDOWN:
			if w*0.16 - 70 <= mouse[0] <= w*0.16 + 30 and h/2 + 150 <= mouse[1] <= h/2 + 190:
				pg.quit()
			if w*0.16 - 75 <= mouse[0] <= w*0.16 +75 and h/2 -50 <= mouse[1] <= h/2 + 10:
				menuShow= False
			if w*0.16 - 110 <= mouse[0] <= w*0.16 +115 and h/2 +50 <= mouse[1] <= h/2 + 110:
				controls_show = True

			# Making Controls thing able to close
			while controls_show:
				for event in pg.event.get():
					mouse=pg.mouse.get_pos()

					if event.type == pg.QUIT:
						pg.quit()
					if event.type == pg.MOUSEBUTTONDOWN:
						if w*0.3 + 560 <= mouse[0] <= w*0.3 + 579 and h*0.3 + 2 <= mouse[1] <= h*0.3 + 22:
							controls_show = False

				screen.blit(controls_pic,(w*0.3,h*0.3))

				pg.display.flip()
				clock.tick(30)

		# Check where mouse is pointing, if mouse on button or not
		if w*0.16 - 70 <= mouse[0] <= w*0.16 + 60 and h/2 + 150 <= mouse[1] <= h/2 + 210:
			pg.draw.rect(screen, (133,169,71), [w*0.16 - 70,h/2 + 150,130,60])

		else:
			pg.draw.rect(screen,(18,53,36), [w*0.16 - 70,h/2 + 150,130,60])

		if w*0.16 - 75 <= mouse[0] <= w*0.16 +75 and h/2 -50 <= mouse[1] <= h/2 + 10:
			pg.draw.rect(screen, (133, 169, 71), [w*0.16 - 75, h/2 - 50, 150,60])

		else:
			pg.draw.rect(screen, (18,53,36), [w*0.16 - 75, h/2 - 50, 150,60])

		if w*0.16 - 110 <= mouse[0] <= w*0.16 +115 and h/2 +50 <= mouse[1] <= h/2 + 110:
			pg.draw.rect(screen, (133, 169, 71), [w*0.16 - 110, h/2 + 50, 225,60])

		else:
			pg.draw.rect(screen, (18,53,36), [w*0.16 - 110, h/2 + 50, 225,60])

		screen.blit(t_quit, (w*0.16 - 65, h/2 + 140))
		screen.blit(t_start, (w*0.16 - 70, h/2 - 60))
		screen.blit(t_controls,(w*0.16 - 105, h/2 + 40))

		pg.display.flip()
		clock.tick(30)

def hint_menu(dialogue,w = screen.get_width(),h = screen.get_height(),x=0,y=0,line_lenght = 20):
	alpha_surface = pg.Surface((w, h),pg.SRCALPHA)  #Making surface that able to be transparent
	alpha_surface.fill((0,0,0,128)) #Setting transparency


		#Copying code from Dialog menu to make a proper looking text

	page = 0
	page_text = dialogue[page]
	strings = []

	for i in range(0,len(page_text),line_lenght):

		if i != 0:
			i = end


		# print("hint_menu | pagetext =",len(page_text))
		# print("hint_menu | i and line_lenght =",i,",",line_lenght)

		if i+line_lenght < len(page_text):
			end = i+line_lenght
		else:
			temp = len(page_text) - i
			# print("hint_menu | temp =",temp)
			end = i + temp

		# print("hint_menu | end =",end)
		# print("hint_menu | page_text[end] =",page_text[end-1])

		decrease = 0
		while page_text[end-1] != " " and page_text[end-1] != ".":
			end -= 1
			decrease += 1
			# print("hint_menu | end decreased by",decrease)


		strings.append(page_text[i:end])

		# print("hint_menu | strings =", strings)

	fontTalk = pg.font.SysFont("Comic Sans", 32)

	line1=fontTalk.render(strings[0], True, "white") # What is person saying
	if len(strings)>1:
		line2=fontTalk.render(strings[1], True, "white")
	if len(strings)>2:
		line3=fontTalk.render(strings[2], True, "white")
	if len(strings)>3:
		line4=fontTalk.render(strings[3], True, "white")
	if len(strings)>4:
		line5=fontTalk.render(strings[4], True, "white")
	if len(strings)>5:
		line6=fontTalk.render(strings[5], True, "white")

	alpha_surface.blit(line1, (0, 0 ))
	if len(strings)>1:
		alpha_surface.blit(line2, (0, 35))
	if len(strings)>2:
		alpha_surface.blit(line3, (0, 70))
	if len(strings)>3:
		alpha_surface.blit(line4, (0, 105))
	if len(strings)>4:
		alpha_surface.blit(line5, (0, 140))
	if len(strings)>5:
		alpha_surface.blit(line6, (0, 175))
	screen.blit(alpha_surface,(x,y)) #Drawing the surface | VERY IMPORTANT TO THIS BE AT THE END OF ALL CHANGES IN SURFACE
	# print("hint_menu | Done")

def fps_show():
	fps = round(clock.get_fps(),1)
	fps_lenght = 150
	print_text(screen,f"FPS: {fps}", "Comic Sans",24,screen.get_width() - fps_lenght,0)

# initializing something for map_blit():

lastlevel = None   # We already have player.last_level but this thing here to initialize things at the start of each level.


def map_blit(floor_only = None):
	global level1progress , happened , lastlevel


	if choosenLevel != lastlevel:

		lastlevel = choosenLevel

		if choosenLevel == basement_yura:
			global lever1_action, lever2_action, lever3_action, lever4_action
			global lamp1_on,lamp2_on,lamp3_on,lamp4_on, puzzle_won

			puzzle_won = None
			lever1_action = None
			lever2_action = None
			lever3_action = None
			lever4_action = None

			lamp1_on,lamp2_on,lamp3_on,lamp4_on = None,None,None,None


	if floor_only != None:
		for i in floor:
			i.reset()
			print("map blit | floor reseted")
	else:
		for obj in intObj:
			# not reseting objects after field level because map() does it now (same for walls and smallInt)
			if startLevel < 3:
				obj.reset()

			obj.interaction()
			if choosenLevel == karta1:

				if obj.image_route == "game pics/mo.png" or obj.image_route == "game pics/mo_down.png":

					if obj.answer:

						if inventory.get_amount("shovel") <1:
							print("Shovel amount:",inventory.get_amount("shovel"), inventory.get_amount("shovel") < 1)
							obj.answer = False
							break

						if obj.image_route == "game pics/mo.png":         # MAYBE CHANGE IT TO A SHORTER FUNCTION LATER | We are changing gravve texture when answer after interaction is positive

							walls.append(Wall(obj.rect.x, obj.rect.y, obj.w, obj.h, obj.speed, "game pics/mm.png", 0))
							intObj.remove(obj)

							level1progress += 1

						if obj.image_route == "game pics/mo_down.png":     # MAYBE CHANGE IT TO A SHORTER FUNCTION LATER | We are changing gravve texture when answer after interaction is positive

							obj.image_route = "game pics/mm2.png"
							walls.append(Wall(obj.rect.x, obj.rect.y, obj.w, obj.h, obj.speed, obj.image_route, 0))
							intObj.remove(obj)

							level1progress += 1


				if obj.index == "exit":
					if level1progress == 3:
						obj.__init__("Rover",["Should I leave?"],obj.rect.x,obj.rect.y,obj.w,obj.h,obj.speed,obj.image_route,obj.line_lenght,obj.int_mode,True,"active_exit")
				if obj.index == "active_exit":
					if obj.answer == True:
						level1progress = 0

						travel() # kalitka

			if choosenLevel == appartment:

				if obj.index == "tea": # checking for int obj with index tea

					if obj.times_activated > 10:
						walls.append(Wall(obj.rect.x, obj.rect.y, obj.w, obj.h, obj.speed, "game pics/nothing.png", 0))
						intObj.remove(obj)

					if obj.answer == True: # looking if answer is yes
						inventory.increase("tea") # Giving tea
						print("tea =", inventory.get_amount("tea"))


					# Changing text after several tea

						if 5 >obj.times_activated >= 1:
							obj.change(obj.name,["More tea?"],obj.image_route,obj.line_lenght,obj.int_mode,obj.question, index = obj.index)

						elif 10 >obj.times_activated >= 5:
							obj.change(obj.name,["More tea???"],obj.image_route,obj.line_lenght,obj.int_mode,obj.question, index = obj.index)

						elif obj.times_activated == 10:
							obj.change(obj.name,["Last tea?"],obj.image_route,obj.line_lenght,obj.int_mode,obj.question, index = obj.index)

						obj.answer = False

				if obj.index == "sleep": # checking my sleeping bag

					if obj.answer == True: # checking that player went to sleep
						travel()

			if choosenLevel == appartment_1:
				if obj.index == "tea": # checking for int obj with index tea

					if obj.times_activated > 10:
						walls.append(Wall(obj.rect.x, obj.rect.y, obj.w, obj.h, obj.speed, "game pics/nothing.png", 0))
						intObj.remove(obj)

					if obj.answer == True: # looking if answer is yes
						inventory.increase("tea") # Giving tea
						print("tea =", inventory.get_amount("tea"))

					# Changing text after several tea

						if 5 >obj.times_activated >= 1:
							obj.change(obj.name,["More tea?"],obj.image_route,obj.line_lenght,obj.int_mode,obj.question, index = obj.index)

						elif 10 >obj.times_activated >= 5:
							obj.change(obj.name,["More tea???"],obj.image_route,obj.line_lenght,obj.int_mode,obj.question, index = obj.index)

						elif obj.times_activated == 10:
							obj.change(obj.name,["Last tea?"],obj.image_route,obj.line_lenght,obj.int_mode,obj.question, index = obj.index)

						obj.answer = False

				if obj.index == "sink":
					if obj.talked >= 1:
						level1progress +=1
						obj.__init__("Rover",["I should go check basement"], obj.rect.x, obj.rect.y, obj.w, obj.h, obj.speed, obj.image_route,obj.line_lenght,obj.int_mode,obj.question,index = None)

				if level1progress == 1:

					if obj.index == "exit":

						obj.__init__("Rover",["Go to the basement?"], obj.rect.x, obj.rect.y, obj.w, obj.h, obj.speed, obj.image_route,obj.line_lenght,obj.int_mode,True,obj.index)
						level1progress += 1

				if level1progress == 2:

					if obj.index == "exit":

						if obj.answer == True:
							if player.target == None:
								print(f"traveling and reseting levelprogress")

								travel()
								level1progress = 0
								happened = False

			if choosenLevel == basement_yura:


				if obj.index == "lever1":

						if obj.answer:

							lever1_action = True

							if obj.image_route == "game pics/lever_down.png":

								obj.image_route = "game pics/lever_up.png"
								obj.reload_image()
								print(f"lever 1 action = {lever1_action}")


							else:

								obj.image_route = "game pics/lever_down.png"
								obj.reload_image()

							obj.answer = False

				if obj.index == "lever2":

						if obj.answer:

							lever2_action = True

							if obj.image_route == "game pics/lever_down.png":

								obj.image_route = "game pics/lever_up.png"
								obj.reload_image()
								print(f"lever 2 action = {lever2_action}")



							else:

								obj.image_route = "game pics/lever_down.png"
								obj.reload_image()

							obj.answer = False

				if obj.index == "lever3":

						if obj.answer:

							lever3_action = True

							if obj.image_route == "game pics/lever_down.png":

								obj.image_route = "game pics/lever_up.png"
								obj.reload_image()
								print(f"lever 3 action = {lever4_action}")



							else:

								obj.image_route = "game pics/lever_down.png"
								obj.reload_image()

							obj.answer = False

				if obj.index == "lever4":

					if obj.answer:

						lever4_action = True

						if obj.image_route == "game pics/lever_down.png":

							obj.image_route = "game pics/lever_up.png"
							obj.reload_image()
							print(f"lever 4 action = {lever4_action}")


						else:

							obj.image_route = "game pics/lever_down.png"
							obj.reload_image()

						obj.answer = False





			if len(intObj) == 0:
				#print("inv =", inventory.get_amount("shovel"))

				if inventory.get_amount("shovel") != 0:
					inventory.decrease("shovel")
		for ef in effects:

			if choosenLevel == basement_yura:

				if ef.animation_finished:

					floor.append(GameObject(tales*17,tales*2,tales,tales,tales/4,"game pics/zapiska.png","zapiska",1))
					effects.remove(ef)

				if puzzle_won:
					ef.run_animation(speed = 4)

		for i in floor:
			if startLevel < 3:
				i.reset()
			# if choosenLevel == basement_yura:
				# if i.index == "zapiska":



					# Moving code

					# if i.rect.x == 1020 and i.rect.y == 120:
					#     i.set_target(-4,1)

					# if i.target != None:
					#     i.move_to_target()
					#     print ("moving zapiska")

		for w in walls:
			if startLevel < 3:
				w.reset()

			if choosenLevel == basement_yura:



				if w.index == "lamp1":

					if lever1_action:

						if w.image_route != "game pics/lamp.png":

							w.image_route = "game pics/lamp.png"
							w.reload_image()
							lamp1_on = True


						else:

							w.image_route = "game pics/lamp_off.png"
							w.reload_image()

						print("lamp1 | image changed")

					# print(f"l2 = {lever2_action} l3 = {lever3_action} l4 = {lever4_action}")

					if lever2_action:

						if w.image_route != "game pics/lamp.png":

							w.image_route = "game pics/lamp.png"
							w.reload_image()
							lamp1_on = True

						else:

							w.image_route = "game pics/lamp_off.png"
							w.reload_image()



						print("lamp1 | image changed")


					if lever3_action:

						if w.image_route != "game pics/lamp.png":

							w.image_route = "game pics/lamp.png"
							w.reload_image()
							lamp1_on = True

						else:

							w.image_route = "game pics/lamp_off.png"
							w.reload_image()



						print("lamp1 | image changed")

					if lever4_action:

						if w.image_route != "game pics/lamp.png":

							w.image_route = "game pics/lamp.png"
							w.reload_image()
							lamp1_on = True

						else:

							w.image_route = "game pics/lamp_off.png"
							w.reload_image()



						print("lamp1 | image changed")

				if w.index == "lamp2":

					if lever1_action:

						if w.image_route != "game pics/lamp.png":

							w.image_route = "game pics/lamp.png"
							w.reload_image()
							lamp2_on = True


						else:

							w.image_route = "game pics/lamp_off.png"
							w.reload_image()

						print("lamp2 | image changed")


					if lever2_action:

						if w.image_route != "game pics/lamp.png":

							w.image_route = "game pics/lamp.png"
							w.reload_image()
							lamp2_on = True

						else:

							w.image_route = "game pics/lamp_off.png"
							w.reload_image()

						print("lamp2 | image changed")

				if w.index == "lamp3":

					if lever4_action:

						if w.image_route != "game pics/lamp.png":

							w.image_route = "game pics/lamp.png"
							w.reload_image()

							lamp3_on = True

						else:

							w.image_route = "game pics/lamp_off.png"
							w.reload_image()



						print("lamp3 | image changed")

				if w.index == "lamp4":

					if lever2_action:

						if w.image_route != "game pics/lamp.png":

							w.image_route = "game pics/lamp.png"
							w.reload_image()
							lamp4_on = True

						else:

							w.image_route = "game pics/lamp_off.png"
							w.reload_image()



						print("lamp4 | image changed")

					if lever3_action:

						if w.image_route != "game pics/lamp.png":

							w.image_route = "game pics/lamp.png"
							w.reload_image()
							lamp4_on = True

						else:

							w.image_route = "game pics/lamp_off.png"
							w.reload_image()


						print("lamp4 | image changed")

					lever1_action,lever2_action,lever3_action,lever4_action = False,False,False,False



				puzzle_won = lamp1_on and lamp2_on and lamp3_on and lamp4_on
				# print(f"l1 {lamp1_on}, l2 {lamp2_on}, l3 {lamp3_on}, l4 {lamp4_on} \npz {puzzle_won}")

				if puzzle_won:

					if w.index == "frog":

						w.image_route, w.index = "game pics/nothing.png", None   # If not change index cycle eats all FPS

		for smol in smallInt:
			if startLevel < 3:
				smol.reset()

			if choosenLevel == karta1:
				interact=smol.interaction()
				#print ("smol | interact =",interact)

				while interact:
					for event in pg.event.get():
						if event.type == pg.QUIT:
							pg.quit
					screen.blit(smol.imagebig,(screen.get_width()/2 - 400, screen.get_height()/5))
					if pg.key.get_pressed()[pg.K_f]:
						interact = False

					pg.display.flip()

			if choosenLevel == basement_stasa:

				if smol.index == "chest":

					interact = smol.interaction()

					num1 = 0
					num2 = 0
					num3 = 0

					while interact:

						smol.get_leftTopCords()

						screen.blit(smol.imagebig,(smol.leftTop[0], smol.leftTop[1])) # bliting the lock

						print_text(screen,str(num1), "Comic Sans", 80, 320,600,"black")
						print_text(screen,str(num2), "Comic Sans", 80, 480,600,"black")
						print_text(screen,str(num3), "Comic Sans", 80, 640,600,"black")

						for event in pg.event.get(): # Cycles man
							if event.type == pg.QUIT:
								pg.quit



							if event.type == pg.MOUSEBUTTONDOWN:
								mouse = pg.mouse.get_pos()
								print("Mouse Pos:",mouse)

								# TRIkUTNICHKI

								tr1_u = ((294, 581),(353, 538),(414, 582))
								tr1_d = ((294, 737),(352, 781),(413, 739))
								tr2_u = ((453, 582),(513, 538),(574, 581))
								tr2_d = ((454, 737),(513, 781),(574, 736))
								tr3_u = ((613, 582),(673, 539),(733, 582))
								tr3_d = ((613, 737),(673, 782),(733, 737))

								# Button Circle

								button = (810,666)
								radius = 53

								# Check which triangle was clicked

								if point_in_triangle(tr1_u[0],tr1_u[1],tr1_u[2],mouse):
									print("Up Left Triangle Clicked!!!!!!!!!")
									# Add Num 1
									if num1 != 9:
										num1+=1
									else:
										num1 = 0

										# print(f"Num 1 = {num1}")

								if point_in_triangle(tr1_d[0],tr1_d[1],tr1_d[2],mouse):
									print("Bottom Left Triangle Clicked!!!!!!!!!")
									# Subtract Num 1
									if num1 != 0:
										num1-=1
									else:
										num1 = 9

										# print(f"Num 1 = {num1}")

								if point_in_triangle(tr2_u[0],tr2_u[1],tr2_u[2],mouse):
									print("Up Middle Triangle Clicked!!!!!!!!!")
									# Add Num 2
									if num2 != 9:
										num2+=1
									else:
										num2 = 0

									# print(f"Num 2 = {num2}")

								if point_in_triangle(tr2_d[0],tr2_d[1],tr2_d[2],mouse):
									print("Bottom Middle Triangle Clicked!!!!!!!!!")
									# Subtract Num 2
									if num2 != 0:
										num2-=1
									else:
										num2 = 9

									# print(f"Num 2 = {num2}")

								if point_in_triangle(tr3_u[0],tr3_u[1],tr3_u[2],mouse):
									print("Up Right Triangle Clicked!!!!!!!!!")
									# Add Num 3
									if num3 != 9:
										num3+=1
									else:
										num3 = 0

									# print(f"Num 3 = {num3}")

								if point_in_triangle(tr3_d[0],tr3_d[1],tr3_d[2],mouse):
									print("Bottom Right Triangle Clicked!!!!!!!!!")
									# Subtract Num 3
									if num3 != 0:
										num3-=1
									else:
										num3 = 9
									# print(f"Num 3 = {num3}")

								if point_in_circle(mouse[0],mouse[1],button[0],button[1],radius):
									print("point in circle")

									correct_password = num1 == 5 and num2 == 1 and num3 == 2

									if correct_password:

										print("RIGHT PASSWORD!!!!!!!!")

										smol.new_imagebig("game pics/empty_chest.png")
										smol.index = "open_chest"

										# adding key in chest that picks up when you click on it
										x,y = smol.get_leftTopCords()
										screenCollectables.append(ScreenCollectable(x+(smol.w/2) - 50, y + (smol.h/2) + 50, 100, 100, "game pics/key.png","key"))

										interact = False

						if pg.key.get_pressed()[pg.K_f]:
							interact = False

						pg.display.flip()

				if smol.index == "open_chest":
					interact = smol.interaction()

					while interact:
						for collectable in screenCollectables:
							collectable.active = True						
						
						smol.reset_image_big()


						for event in pg.event.get(): # Cycles man
							if event.type == pg.QUIT:
								pg.quit		
					
						pg.display.flip()
					
		for collectable in screenCollectables:
			if collectable.active:
				collectable.reset()
				collectable.collect_when_clicked()

			if collectable.reached_max:
				screenCollectables.remove(collectable)


		for thing in item:
			thing.reset()
			if thing.int_mode == 1:
				if player.rect.colliderect(thing.rect):
					if pg.key.get_pressed()[pg.K_e]:
						thing.get_give()
			if thing.int_mode == 2:
				left = thing.rect.x-tales <= player.rect.x < thing.rect.x and thing.rect.y == player.rect.y
				right = thing.rect.x<player.rect.x <= thing.rect.x + tales and thing.rect.y == player.rect.y
				top = thing.rect.y - tales <= player.rect.y <= thing.rect.y and thing.rect.x == player.rect.x
				bottom = thing.rect.y <= player.rect.y <= thing.rect.y + tales and thing.rect.x == player.rect.x

				if left or right or top or bottom:
					if pg.key.get_pressed()[pg.K_e]:
						thing.get_give()

			if thing.index == "shovel":
				if thing.used == thing.max_amount:
					floor.append(GameObject(thing.rect.x,thing.rect.y,thing.w,thing.h,0,"game pics/pidloga1.png"))
					item.remove(thing)


		map("reset")

#global varients
last = 0
level1progress = 0
happened = False
controls_show = False

exitzone = Exit_zone(tales*16,tales*21,tales*2,tales)

menu()
map()
running=True
while running:
	for event in pg.event.get():
		#print(event)
		if event.type == pg.QUIT:
			running = False
		#if event.type == pg.USEREVENT:
			#player.controls()

	mouse = pg.mouse.get_pos()
	now = pg.time.get_ticks() #Current time number
	#print("now =", now)
	#screen.blit(Chickibamboni, (0,0))



	map_blit()


	# Fixing things after tale changed:

	# print(f"player.w = {player.w}")

	# if player.w != tales:
	#     player.reload("game pics/avatar.png",player.rect.x,player.rect.y,w=tales,h=tales,speed = tales/8)
#         print(f'''player.w = {player.w}
# player.h = {player.h}''')


	player.reset()

	map(up = True)

	player.controls()
	# player.teleport()
	inventory.inventory_cycle()
	fps_show()
	check()




	if choosenLevel == karta1:   # SCRIPT FOR LEVEL1





		if level1progress == 0:
			hint_menu(["I need to bury a grave, shovel should be somewhere on graveyard."],w=screen.get_width()/5,h=screen.get_height()/3,x=0,y=screen.get_height()/6)
		if inventory.get_amount("shovel") >= 1 and happened == False:    # Pomoemu eto HALTURA | da pohui
			level1progress += 1
			happened = True

		if 3 > level1progress >=1:
			hint_menu(["Now when I have a shovel I can bury that grave."],w=screen.get_width()/5,h=screen.get_height()/3,x=0,y=screen.get_height()/6)
			# happened = False

		if level1progress == 3:
			hint_menu(["Now I need to get out of here."],w=screen.get_width()/5,h=screen.get_height()/3,x=0,y=screen.get_height()/6)


	if choosenLevel == appartment_1:

		if level1progress == 0:
			hint_menu(["I need to brush my teeth."],tales*8,tales,tales*2,0,40)

		if level1progress >= 1:
			hint_menu(["I should go check basement."],tales*8,tales,tales*2,0,40)





	# if choosenLevel == appartment:
	#     if exitzone.rect.colliderect:


#Put the game before this line

	pg.display.flip()
	clock.tick(30)
pg.quit()
