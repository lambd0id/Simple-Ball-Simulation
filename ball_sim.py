import pygame
import math
import numpy as np
from time import sleep

pygame.init()
width = 500
height = 500
win = pygame.display.set_mode((width,height),1)
pygame.display.set_caption('Ball Sim', 'Ball Sim')

class particle(object):
    def __init__(self,radius,density,color,position):
        self.radius = radius #constant
        self.density = density #constant
        self.mass = math.pi * (self.radius**2) * self.density
        self.color = np.array(color) #n=3 tuple
        self.pos = np.array(position) #n=2 list
        self.vel = np.array([0,0])    #n=2 list
        self.rel_mov = np.array([0,0]) #n=2 list
        self.held = False

    def draw(self,window):
        pygame.draw.circle(window,self.color,self.pos,self.radius)

    def is_held(self,mouse):
        self.held = (mouse[0]-self.pos[0])**2 + (mouse[1]-self.pos[1])**2 < self.radius**2
        
    def mouse_drag(self,mouse):
        if not self.held:
            return
        
        self.pos[0] = mouse[0]
        self.pos[1] = mouse[1]

    def gravity(self,grav):
        if self.held:
            return
        
        self.vel[1] += grav
    
    def move(self):
        self.pos += self.vel
    
    def boundaries(self,damp):
        if self.pos[0]+self.radius > width:
            self.pos[0] = width-self.radius
            self.vel[0] *= -damp

        elif self.pos[0]-self.radius < 0:
            self.pos[0] = self.radius
            self.vel[0] *= -damp

        if self.pos[1]+self.radius > height:
            self.pos[1] = height-self.radius
            self.vel[1] *= -damp

        elif self.pos[1]-self.radius < 0:
            self.pos[1] = self.radius
            self.vel[1] *= -damp

    def force_steady_state(self):
            if abs(self.vel[1]) <= 1 and self.pos[1] > height-self.radius-10:
                self.vel[1] = 0
                self.pos[1] = height-self.radius
            if abs(self.vel[0]) <= 1 and self.pos[1] == height-self.radius:
                self.vel[0] = 0

    def mouse_fling(self):
        self.vel[0] = int((self.rel_mov[0] * vel_scale) / self.mass)
        self.vel[1] = int((self.rel_mov[1] * vel_scale) / self.mass)
        self.rel_mov = (0,0)
        
    def update(self,mouse,grav,damp,win):
        self.mouse_drag(mouse)
        self.gravity(grav)
        self.boundaries(damp)
        self.force_steady_state()
        self.move()
        self.draw(win)

def collide(a,b):
    collision = a.pos-b.pos
    distance = np.linalg.norm(collision)
    if distance == 0:
        collision = np.array([1,0])
        distance = 1;
    
    collision = collision/distance
    aci = np.dot(a.vel,collision)
    bci = np.dot(b.vel,collision)
    
    acf = ((aci*(a.mass-b.mass))+(2*b.mass*bci))/(a.mass+b.mass)
    bcf = ((bci*(b.mass-a.mass))+(2*a.mass*aci))/(a.mass+b.mass)

    avf = (acf - aci) * collision
    bvf = (bcf - bci) * collision

    a.vel[0] += int(avf[0])
    a.vel[1] += int(avf[1])
    b.vel[0] += int(bvf[0])
    b.vel[1] += int(bvf[1])
    

def check_collision(allballs):
    cnt = 0
    for i in allballs:
        for j in allballs[cnt+1:len(allballs)]:
            if i.radius + j.radius >= np.linalg.norm(i.pos-j.pos):                
                collide(i,j)
        cnt+=1


#constants
grav = 1
damp = 0.5
run = True
vel_scale = 1000
mouse_down = False
ctr = 0

test = particle(20,10,(0,255,0),[width/2, height/2])
test2 = particle(20,10,(0,0,255),[0, 0])
#test3 = particle(30,10,(255,0,0),[400, 300])
#test4 = particle(30,10,(255,255,0),[200, 200])
allballs = [test,test2]

print("Simple Ball Sim")
print("-Pick up a ball using the mouse button")
print("-Drag it around and release to throw the ball")
print("-Watch it bounce around and collide with other balls")


while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            break
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_down = True
            for ball in allballs:
                ball.is_held(mouse)
        elif event.type == pygame.MOUSEBUTTONUP:
            mouse_down = False
            for ball in allballs:
                if ball.held:
                    ball.rel_mov = pygame.mouse.get_rel()
                    ball.held = False
                    ball.mouse_fling()
    
    if mouse_down:
        if ctr < 60:
            ctr+=1
        else:
            for ball in allballs:
                if ball.held:
                    ball.rel_mov = pygame.mouse.get_rel()
            ctr=0
    mouse = pygame.mouse.get_pos()

    check_collision(allballs)
    
    win.fill((0,0,0))
    for ball in allballs:
        ball.update(mouse,grav,damp,win)
    pygame.display.update()
    sleep(1/60)

pygame.quit()
            
    
    
