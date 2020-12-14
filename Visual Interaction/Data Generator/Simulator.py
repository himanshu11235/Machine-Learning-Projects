#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
from Box2D import *
import math
import random
import pygame
from pygame.locals import (QUIT, KEYDOWN, K_ESCAPE)

# --- constants ---
# Box2D deals with meters, but we want to display pixels,
# so define a conversion factor:
PPM = 20.0  # pixels per meter
TARGET_FPS = 60
TIME_STEP = 1.0 / TARGET_FPS
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480



# --- pygame setup ---
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
pygame.display.set_caption('Simple pygame example')
clock = pygame.time.Clock()


colors = {
    Box2D.b2.staticBody: (255, 255, 255, 255),
    Box2D.b2.dynamicBody: (127, 127, 127, 255),
}

colours  = [(255, 255, 255, 255), (255, 0, 0, 255), (0, 255, 0, 255), (127, 127, 127, 255)]

def my_draw_circle(circle, body, fixture):
    position = body.transform * circle.pos * PPM
    position = (position[0], SCREEN_HEIGHT - position[1])
    pygame.draw.circle(screen, colours[i-5], [int(
        x) for x in position], int(circle.radius * PPM))
    # Note: Python 3.x will enforce that pygame get the integers it requests,
    #       and it will not convert from float.

def my_draw_polygon(box, body, fixture):
    position1 = body.transform * box.vertices[0] * PPM
    position1 = (position1[0], SCREEN_HEIGHT - position1[1])
    position2 = body.transform * box.vertices[1] * PPM
    position2 = (position2[0], SCREEN_HEIGHT - position2[1])
    position3 = body.transform * box.vertices[2] * PPM
    position3 = (position3[0], SCREEN_HEIGHT - position3[1])
    position4 = body.transform * box.vertices[3] * PPM
    position4 = (position4[0], SCREEN_HEIGHT - position4[1])
    
    pygame.draw.polygon(screen,colors[body.type] , [(int(position1[0]),int(position1[1]) ), (int(position2[0]), int(position2[1])), (int(position3[0]),int(position3[1])),(int(position4[0]),int(position4[1])) ])
    #
    # Note: Python 3.x will enforce that pygame get the integers it requests,
    #       and it will not convert from float.

    
    
Box2D.b2.circleShape.draw = my_draw_circle
Box2D.b2.polygonShape.draw = my_draw_polygon



def check_overlap(centre1, centre2, radius1, radius2):
    dist = math.sqrt((centre1[0]-centre2[0])**2 + (centre1[1] - centre2[1])**2)
    if dist > radius1+radius2 + 10:
        return 0
    else :
        return 1
    

for k in range(1, 2):
    gap = (30, 20)
    world = b2World(gravity=(0,0), doSleep = False)
    r = 1.5
    radius =  [r]*4
    density = [1]*4
    restitution = [1]*4
    position = []
    
    
    # --- constants ---
    # Box2D deals with meters, but we want to display pixels,
    # so define a conversion factor:
    PPM = 20.0  # pixels per meter
    TARGET_FPS = 60
    TIME_STEP = 1.0 / TARGET_FPS
    SCREEN_WIDTH, SCREEN_HEIGHT = 1000, 480



    # --- pygame setup ---
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
    pygame.display.set_caption('Simple pygame example')
    clock = pygame.time.Clock()

    
    sep = math.ceil(r)
    
    

    groundBody1 = world.CreateStaticBody(position=(gap[0]/2 + 2, 1))
    fix1 = groundBody1.CreateFixture(shape = b2PolygonShape(box=(gap[0]/2,1)), restitution =1, categoryBits=0x0010, maskBits= 0xFFFF)
    
    groundBody2 = world.CreateStaticBody(position=(gap[0]/2 + 2,  gap[1]+3))
    fix2 = groundBody2.CreateFixture(shape = b2PolygonShape(box=(gap[0]/2,1)), restitution =1, categoryBits=0x0020, maskBits= 0xFFFF)
    
    groundBody3 = world.CreateStaticBody(position=(1,(4+gap[1])/2))
    fix3 = groundBody3.CreateFixture(shape = b2PolygonShape(box=(1,(4+gap[1])/2)) , restitution =1, categoryBits=0x0040, maskBits= 0xFFFF)

    groundBody4 = world.CreateStaticBody(position=(gap[0] + 3,(4+gap[1])/2))
    fix4 = groundBody4.CreateFixture(shape = b2PolygonShape(box=(1,(4+gap[1])/2)), restitution =1, categoryBits=0x0080, maskBits= 0xFFFF)

    body1 = world.CreateBody(type =  b2_dynamicBody, position = position[0], angle = 0.0, linearDamping=0.0, angularDamping = 0.01, bullet = True, )
    myShape = b2CircleShape(radius=radius[0])
    myFixture = body1.CreateFixture(shape=myShape, density=density[0], friction=0.0, restitution = restitution[0], categoryBits=0x0001, maskBits=0x0010 |0x0020|0x0040|0x0080)

    body2 = world.CreateBody(type =  b2_dynamicBody, position = position[1], angle = 0.0, linearDamping=0.0, angularDamping = 0.01, bullet = True, )
    myShape2 = b2CircleShape(radius=radius[1])
    myFixture = body2.CreateFixture(shape=myShape2, density=density[1], friction=0.0, restitution = restitution[1],categoryBits=0x0002, maskBits=0x0010 |0x0020|0x0040|0x0080|0x0008| 0x0004)

    body3 = world.CreateBody(type =  b2_dynamicBody, position = position[2], angle = 0.0, linearDamping=0.0, angularDamping = 0.01, bullet = True, )
    myShape3 = b2CircleShape(radius=radius[2])
    myFixture = body3.CreateFixture(shape=myShape3, density=density[2], friction=0.0, restitution = restitution[2], categoryBits=0x0004, maskBits=0x0010 |0x0020|0x0040|0x0080| 0x0002|0x0008)

    body4 = world.CreateBody(type =  b2_dynamicBody, position = position[3], angle = 0.0, linearDamping=0.0, angularDamping = 0.01, bullet = True, )
    myShape4 = b2CircleShape(radius=radius[3])
    myFixture = body4.CreateFixture(shape=myShape4, density=density[3], friction=0.0, restitution = restitution[3],categoryBits=0x0008, maskBits=0x0010 |0x0020|0x0040|0x0080|0x0004| 0x0002)

        
    n_sec = 30
    B = np.zeros((n_sec*60,16))
    frame_per_sec = 60
    timeStep = 1.0 / frame_per_sec
    vel_iters, pos_iters = 6, 4

    body1.linearVelocity = (0,0)
    body2.linearVelocity = (0, 0)
    body3.linearVelocity = (0, 0)
    body4.linearVelocity = (0,0)
    ######################################
    array = np.load("path of the np array you wanna simulate")
    #########################################
    for l in range(n_sec*frame_per_sec):
        '''r12 = ((body2.position[0]-body1.position[0])/math.sqrt((body1.position[0]-body2.position[0])**2 + (body1.position[1]-body2.position[1])**2), (body2.position[1]-body1.position[1])/math.sqrt((body1.position[0]-body2.position[0])**2 + (body1.position[1]-body2.position[1])**2))
        if (A[0][6] == 1):
            f12 = A[1][0]/((body1.position[0]-body2.position[0])**2 + (body1.position[1]-body2.position[1])**2)
        else:
            f12 = A[1][0]*math.sqrt((body1.position[0]-body2.position[0])**2 + (body1.position[1]-body2.position[1])**2)
        r13 = ((body3.position[0]-body1.position[0])/math.sqrt((body1.position[0]-body3.position[0])**2 + (body1.position[1]-body3.position[1])**2), (body3.position[1]-body1.position[1])/math.sqrt((body1.position[0]-body3.position[0])**2 + (body1.position[1]-body3.position[1])**2))
        if (A[0][7] == 1):
            f13 = A[1][1]/((body1.position[0]-body3.position[0])**2 + (body1.position[1]-body3.position[1])**2)
        else:
            f13 = A[1][1]*math.sqrt((body1.position[0]-body3.position[0])**2 + (body1.position[1]-body3.position[1])**2)
        r14 = ((body4.position[0]-body1.position[0])/math.sqrt((body1.position[0]-body4.position[0])**2 + (body1.position[1]-body4.position[1])**2), (body4.position[1]-body1.position[1])/math.sqrt((body1.position[0]-body4.position[0])**2 + (body1.position[1]-body4.position[1])**2))
        if (A[0][8] == 1):
            f14 = A[1][2]/((body1.position[0]-body4.position[0])**2 + (body1.position[1]-body4.position[1])**2)
        else:
            f14 = A[1][2]*math.sqrt((body1.position[0]-body4.position[0])**2 + (body1.position[1]-body4.position[1])**2)
        r23 = ((body3.position[0]-body2.position[0])/math.sqrt((body2.position[0]-body3.position[0])**2 + (body2.position[1]-body3.position[1])**2), (body3.position[1]-body2.position[1])/math.sqrt((body2.position[0]-body3.position[0])**2 + (body2.position[1]-body3.position[1])**2))
        if (A[0][9] == 1):
            f23 = A[1][3]/((body2.position[0]-body3.position[0])**2 + (body2.position[1]-body3.position[1])**2)
        else:
            f23 = A[1][3]*math.sqrt((body2.position[0]-body3.position[0])**2 + (body2.position[1]-body3.position[1])**2)
        r24 = ((body4.position[0]-body2.position[0])/math.sqrt((body2.position[0]-body4.position[0])**2 + (body2.position[1]-body4.position[1])**2), (body4.position[1]-body2.position[1])/math.sqrt((body2.position[0]-body4.position[0])**2 + (body2.position[1]-body4.position[1])**2))
        if (A[0][10] == 1):
            f24 = A[1][4]/((body2.position[0]-body4.position[0])**2 + (body2.position[1]-body4.position[1])**2)
        else:
            f24 = A[1][4]*math.sqrt((body2.position[0]-body4.position[0])**2 + (body2.position[1]-body4.position[1])**2)
        r34 = ((body4.position[0]-body3.position[0])/math.sqrt((body3.position[0]-body4.position[0])**2 + (body3.position[1]-body4.position[1])**2), (body4.position[1]-body3.position[1])/math.sqrt((body3.position[0]-body4.position[0])**2 + (body3.position[1]-body4.position[1])**2))
        if (A[0][11] == 1):
            f34 = A[1][5]/((body3.position[0]-body4.position[0])**2 + (body3.position[1]-body4.position[1])**2)
        else:
            f34 = A[1][5]*math.sqrt((body3.position[0]-body4.position[0])**2 + (body3.position[1]-body4.position[1])**2)
        
        body1.ApplyForce(force=(f12*r12[0]+f13*r13[0]+f14*r14[0],f12*r12[1]+f13*r13[1]+f14*r14[1]), point=(body1.position[0],body1.position[1]), wake = True)
        body2.ApplyForce(force=(-f12*r12[0]+f23*r23[0] + f24*r24[0],-f12*r12[1]+f23*r23[1] + f24*r24[1]), point=(body2.position[0],body2.position[1]), wake = True)
        body3.ApplyForce(force=(-f13*r13[0]-f23*r23[0] + f34*r34[0],-f13*r13[1]-f23*r23[1] + f34*r34[1]), point=(body3.position[0],body3.position[1]), wake = True)
        body4.ApplyForce(force=(-f14*r14[0]-f24*r24[0] - f34*r34[0],-f14*r14[1]-f24*r24[1] - f34*r34[1]), point=(body4.position[0],body4.position[1]), wake = True)
        '''
        ########################################
        body1.pos[0] = array[l,0]
        body1.pos[1] = array[l, 1]
        body2.pos[0] = array[l, 2]
        body2.pos[1] = array[l, 3]
        body3.pos[0] = array[l, 4]
        body3.pos[1] = array[l, 5]
        body4.pos[0] = array[l, 6]
        body4.pos[1] = array[l, 7]
        ##################################################
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                # The user closed the window or pressed escape
                running = False


        screen.fill((0, 0, 0, 0))
        # Draw the world
        i=0
        for body in world.bodies:
            # print(position)
            i+=1
            for fixture in body.fixtures:
                fixture.shape.draw(body, fixture)
        
        world.Step(timeStep, vel_iters, pos_iters)
        world.ClearForces()
        pygame.display.flip()
        clock.tick(TARGET_FPS)
    
    
    pygame.quit()
    print('Done!')
      
