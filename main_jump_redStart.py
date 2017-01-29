import pygame, sys
from pygame.locals import *
from random import randint
import time
import ctypes


def get_pair(moveNum):
	pair_ini = [0,1,2,3,4]
	pair_new = [0,3,4,1,2]
	idx = pair_ini.index(moveNum)
	return pair_new[idx]


def randomise_dir_length(dir_low,dir_high,num,len_low, len_high):
	dir_arr = []
	len_arr = []
	N_prev = 2
	dir_arr.append(N_prev)
	len_arr.append(2)
	for i in range(num):
		N = randint(dir_low,dir_high)
		
		if N != get_pair(N_prev) and N != N_prev:			
				N_len = randint(len_low,len_high)
				N_prev = N
				dir_arr.append(N)
				len_arr.append(N_len)				
		elif N == 0:
			if N_prev != 0:
				N_len = randint(len_low,len_high)
				dir_arr.append(N)
				len_arr.append(1)
				dir_arr.append(N_prev)
				len_arr.append(N_len) 
				N_prev = N
		
	return dir_arr, len_arr



    
class Rectangle(object):
    
    def __init__(self,x_left,y_up,x_length,y_length):
        self.x_left = x_left
        self.y_up = y_up
        self.x_length = x_length
        self.y_length = y_length

class Circle(object):

    def __init__(self,center_x,center_y,radius):
        self.center_x = center_x
        self.center_y = center_y
        self.radius = radius

class Direction(object):
    UP = 2
    DOWN = 4
    LEFT = 1
    RIGHT = 3
    JUMP = 0
    


        

class Segment(object):


    def __init__(self,x_start,y_start,length,thickness,direction):


        self.curr_direction = direction
        self.x_start = x_start
        self.y_start = y_start
        self.length = length
        self.thickness = thickness

      
        if direction==Direction.UP:        
            self.x_end = x_start
            self.y_end = y_start - length
            self.line = Rectangle(x_start-int(thickness/2),self.y_end,thickness,length)
            self.circle_end = Circle(x_start,self.y_end,int(thickness/2))
            self.circle_begin = Circle(x_start,y_start,int(thickness/2))
            self.end_point = y_start + length - thickness
            

        elif direction==Direction.DOWN:
            self.x_end = x_start
            self.y_end = y_start + length            
            self.line = Rectangle(x_start-int(thickness/2),y_start,thickness,length)
            self.circle_end = Circle(self.x_end,self.y_end,int(thickness/2))
            self.circle_begin = Circle(x_start,y_start,int(thickness/2))


        elif direction==Direction.LEFT:
            self.x_end = x_start - length
            self.y_end = y_start            
            self.line = Rectangle(self.x_end,y_start-int(thickness/2),length,thickness)
            self.circle_end = Circle(self.x_end,self.y_end,int(thickness/2))
            self.circle_begin = Circle(x_start,y_start,int(thickness/2))
            self.end_point = x_start - length - thickness


        elif direction==Direction.RIGHT:
            self.x_end = x_start + length
            self.y_end = y_start 
            self.line = Rectangle(x_start,y_start-int(thickness/2),length,thickness)
            self.circle_end = Circle(self.x_end,self.y_end,int(thickness/2))
            self.circle_begin = Circle(x_start,y_start,int(thickness/2))



        elif direction==Direction.JUMP:

            global prev_direction

            length = 300
            self.length = length
            if prev_direction == Direction.UP:
                self.x_end = x_start
                self.y_end = y_start - length
                
            elif prev_direction == Direction.DOWN:
                self.x_end = x_start
                self.y_end = y_start + length
                
            elif prev_direction == Direction.LEFT:
                self.x_end = x_start - length
                self.y_end = y_start
                        
            elif prev_direction == Direction.RIGHT:
                self.x_end = x_start + length
                self.y_end = y_start

            
        
            self.line = Rectangle(x_start,y_start-int(thickness/2),0,0)
            self.circle_end = Circle(self.x_end,self.y_end,int(thickness/2))
            self.circle_begin = Circle(x_start,y_start,int(thickness/2))
            direction = prev_direction
            self.curr_direction = Direction.JUMP

        prev_direction = direction


    def draw(self,game_display,X,Y,color):
        game_display.draw.rect(DISPLAYSURF, color, (self.line.x_left+X, self.line.y_up+Y, self.line.x_length , self.line.y_length))
        game_display.draw.circle(DISPLAYSURF, color, (self.circle_end.center_x+X, self.circle_end.center_y+Y), self.circle_end.radius, 0)
        game_display.draw.circle(DISPLAYSURF, color, (self.circle_begin.center_x+X, self.circle_begin.center_y+Y), self.circle_begin.radius, 0)





    def create_partial_segment(self,X,Y):
        direction = self.curr_direction
        thickness = self.thickness
        x_start = self.x_start
        y_start = self.y_start
        length = self.length

        partial = Segment(0,0,0,0,0)
    
        if direction==Direction.UP:
            partial.x_end = self.x_start
            partial.y_end = Y
            partial.line = Rectangle(x_start-int(thickness/2),partial.y_end,thickness,y_start-partial.y_end)
            partial.circle_end = Circle(x_start,Y,int(thickness/2))
            partial.circle_begin = Circle(x_start,y_start,int(thickness/2))
            

        elif direction==Direction.DOWN:
            partial.x_end = x_start
            partial.y_end = Y
            partial.line = Rectangle(x_start-int(thickness/2),y_start,thickness,partial.y_end-y_start)
            partial.circle_end = Circle(partial.x_end,partial.y_end,int(thickness/2))
            partial.circle_begin = Circle(x_start,y_start,int(thickness/2))


        elif direction==Direction.LEFT:
            partial.x_end = X
            partial.y_end = y_start            
            partial.line = Rectangle(partial.x_end,y_start-int(thickness/2),x_start-partial.x_end,thickness)
            partial.circle_end = Circle(partial.x_end,partial.y_end,int(thickness/2))
            partial.circle_begin = Circle(x_start,y_start,int(thickness/2))


        elif direction==Direction.RIGHT:
            partial.x_end = X
            partial.y_end = y_start 
            partial.line = Rectangle(x_start,y_start-int(thickness/2),partial.x_end-x_start,thickness)
            partial.circle_end = Circle(partial.x_end,partial.y_end,int(thickness/2))
            partial.circle_begin = Circle(x_start,y_start,int(thickness/2))



        elif direction==Direction.JUMP:
            partial.x_end = x_start + length
            partial.y_end = y_start 
            partial.line = Rectangle(x_start,y_start-int(thickness/2),0,thickness)
            partial.circle_end = Circle(self.x_end,self.y_end,0)
            partial.circle_begin = Circle(x_start,y_start,int(thickness/2))

        return partial




            
class PATHWAY(object):

    def __init__(self,path_dirs,path_lengths,x_start,y_start,thickness):
        n_dirs = len(path_dirs)
        n_lengths = len(path_lengths)
        n_segs = min(n_dirs,n_lengths)


        self.path = []

        x = x_start
        y = y_start
        for n in range(0,n_segs):
            curr_segment = Segment(x,y,path_lengths[n]*100,thickness,path_dirs[n])
            x = curr_segment.x_end
            y = curr_segment.y_end
            self.path.append(curr_segment)


    def draw(self,game_display,X,Y,color):

        n_segs = len(self.path)
        for n in range(0,n_segs):
            self.path[n].draw(game_display,X,Y,color)

    def draw_range(self,game_display,X,Y,color,min_segment,max_segment):

        n_segs = len(self.path)
        for n in range(max(0,min_segment),min(n_segs,max_segment)):
            self.path[n].draw(game_display,X,Y,color)


    def draw_partial(self,game_display,X,Y,X_pos,Y_pos,curr_seg,color):

        for n in range(0,curr_seg):
            self.path[n].draw(game_display,X,Y,color)

        partial_seg = self.path[curr_seg].create_partial_segment(X_pos,Y_pos)

        partial_seg.draw(game_display,X,Y,color)

    def draw_partial_range(self,game_display,X,Y,X_pos,Y_pos,min_segment,curr_seg,color):

        for n in range(max(0,min_segment),curr_seg):
            self.path[n].draw(game_display,X,Y,color)

        partial_seg = self.path[curr_seg].create_partial_segment(X_pos,Y_pos)
        

        partial_seg.draw(game_display,X,Y,color)

        if(max(0,min_segment)==0):
            circle_begin = self.path[0].circle_begin
            game_display.draw.circle(DISPLAYSURF, RED, (circle_begin.center_x+X, circle_begin.center_y+Y), circle_begin.radius, 0)

            
        



pygame.init()

BLUE =  (150, 255, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
#RED = (155,20,20)
RED = (245,151,69) #orage actually

#DARK_BLUE =  (40, 140, 140)
DARK_BLUE =  (7,99,13) #dark green actually


DISPLAYSURF = pygame.display.set_mode((800, 600))
bg_image = pygame.image.load('grassLand.jpg')
DISPLAYSURF.blit(bg_image,(0,0))


pygame.key.set_repeat (500, 30)





#path_directions = [Direction.UP, Direction.LEFT,Direction.UP,Direction.RIGHT,Direction.RIGHT,Direction.DOWN]

#path_lengths = [7,7,7,7,7,7]

global prev_direction
prev_direction = 1
path_directions,path_lengths = randomise_dir_length(0,4,8,6,9)
print(path_directions)
print(path_lengths)




x_start = 400
y_start = 300
thickness = 200
curr_path = PATHWAY(path_directions,path_lengths,x_start,y_start,thickness)

obj_image = pygame.image.load('Football.png')
newSize = 200
obj_image = pygame.transform.scale(obj_image,(newSize,newSize))

speed = 10

curr_segment = 0
n_segment = len(curr_path.path)

X = x_start
Y = y_start

game_finished = 0

pygame.display.set_caption('Hello World!')
while True: # main game loop
    for event in pygame.event.get():

        DISPLAYSURF.blit(bg_image, (0,0))

        #pygame.draw.rect(DISPLAYSURF, WHITE, (A.line.x_left+X, A.line.y_up+Y, A.line.x_length , A.line.y_length))
        #pygame.draw.circle(DISPLAYSURF, WHITE, (A.circle_end.center_x+X, A.circle_end.center_y+Y), A.circle_end.radius, 0)
        #pygame.draw.rect(DISPLAYSURF, WHITE, (200+X, -50+Y, 300, 100))
        #A.draw(pygame,X,Y,WHITE)
        #B.draw(pygame,X,Y,BLACK)
        curr_path.draw_range(pygame,-(X-x_start),-(Y-y_start),WHITE,curr_segment-2,curr_segment+3)
        #DISPLAYSURF.blit(obj_image,(x_start-int(thickness/2),y_start-200))
        if curr_segment < n_segment:
            curr_path.draw_partial_range(pygame,-(X-x_start),-(Y-y_start),X,Y,curr_segment-2,curr_segment,DARK_BLUE)
        DISPLAYSURF.blit(obj_image, (x_start-int(200/2),y_start-int(200/2)))

        
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN and game_finished == 0:
            curr_segment_direction = curr_path.path[curr_segment].curr_direction


            if event.key == pygame.K_LEFT  and curr_segment_direction == Direction.LEFT:
                X -= speed
                if X<=curr_path.path[curr_segment].x_end:
                    X = curr_path.path[curr_segment].x_end
                    curr_segment+=1
                    if curr_segment >= n_segment:
                        curr_segment -=1
                        game_finished = 1
                    break

         
            elif event.key == pygame.K_RIGHT  and curr_segment_direction == Direction.RIGHT:
                X += speed
                if X>=curr_path.path[curr_segment].x_end:
                    X = curr_path.path[curr_segment].x_end
                    curr_segment+=1
                    if curr_segment >= n_segment:
                        curr_segment -=1
                        game_finished = 1
                    break

            elif event.key == pygame.K_UP  and curr_segment_direction == Direction.UP:
                Y -= speed
                if Y<=curr_path.path[curr_segment].y_end:
                    Y = curr_path.path[curr_segment].y_end 
                    curr_segment+=1
                    if curr_segment >= n_segment:
                        curr_segment -=1                        
                        game_finished = 1
                    break
   

            elif event.key == pygame.K_DOWN  and curr_segment_direction == Direction.DOWN:
                Y += speed
                if Y>=curr_path.path[curr_segment].y_end:
                    Y = curr_path.path[curr_segment].y_end 
                    curr_segment+=1
                    if curr_segment >= n_segment:
                        curr_segment -=1
                        game_finished = 1
                    break
            elif event.key == pygame.K_1  and curr_segment_direction == Direction.JUMP:
                Y = curr_path.path[curr_segment].y_end
                X = curr_path.path[curr_segment].x_end 

                curr_segment+=1
                if curr_segment >= n_segment:
                    curr_segment -=1
                    game_finished = 1
                break
   
   
               
    pygame.display.update()

    if game_finished:
        ctypes.windll.user32.MessageBoxW(0, "Well done", "Message", 1)
        pygame.quit()
        sys.exit()

    
