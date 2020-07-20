#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 19 15:08:59 2020

@author: kartik
"""

import pygame
from pygame.locals import *
import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import * 
from OpenGL.GLUT import *

import pyquaternion as pyq

verticies = (
(0,  0.052, 0.012),
(0,  0.052,  0),
(0,  0, 0.012),
(0,  0,  0),
(0.072, 0.052, 0.012),
(0.072, 0, 0.012),
(0.072, 0.052,  0),
(0.072, 0,  0)
)

# edges = (
# (0,4),
# (2,3),
# (5,7),
# (0,1),
# (0,2),
# (3,7),
# (1,3),
# (1,6),
# (2,5),
# (4,6),
# (6,7),
# (4,5)
# )

faces = (
    (0,4,6,1),
    (2,5,4,0),
    (0,2,3,1),
    (4,6,7,5),
    (2,3,7,5),
    (3,7,6,1))

def draw_cube_faces():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glBegin(GL_QUADS)
    
    color = [(0.0,1.0,0.0),
             (1.0,0.0,0.0),
             (0.0,0.0,1.0),
             (1.0,1.0,0.0),
             (1.0,0.0,1.0),
             (0.0,1.0,1.0)]
    
    for i,points in enumerate(faces):
        glColor3fv(color[i])
        glVertex3fv(verticies[points[0]])
        glVertex3fv(verticies[points[1]])
        glVertex3fv(verticies[points[2]])
        glVertex3fv(verticies[points[3]])
            
    glEnd()
     
    glEnable(GL_DEPTH_TEST);
# // Accept fragment if it closer to the camera than the former one
    glDepthFunc(GL_LESS);
    pygame.display.flip()

def setup_camera(factor = 8):
    
    display = (int(5184/factor),int(3456/factor))
    pygame.display.set_mode(display,DOUBLEBUF|OPENGL)
    
    fx = 2.355450338814530e+04/factor
    fy = 2.542322134763687e+04/factor
    cx = 3.017825080465273e+03/factor #not used here
    cy = 3.245362443401546e+03/factor #not used here
    
    fov_y = 2*np.arctan(display[1]/(2*fy)) * (180/np.pi) * 1
    # fov_x = 2*np.arctan(display[0]/(2*fx)) * (180/np.pi) * 1

#NOTE : OPENGL STORES MATRICES IN COLUMN MAJOR ORDER! SO NEED TO TRANSPOSE THEM
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    ##(field of view(in degrees), aspect ratio,z_near(near clipping plane), z_far(far clipping plane))
    gluPerspective(fov_y, display[0]/display[1], 0.001, 1000.0)
    model1 = glGetDoublev(GL_PROJECTION_MATRIX)
    print(model1)


def initialise_extrinsic_matrix():
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    
    glTranslate(-0.02,-0.014,-0.5)
    # glRotatef(degrees, x,y,z)
    glRotatef(130,1,0,0)
    glRotatef(70,0,0,-1)

    #this gives the total projection matrix ie  extrinsic * instrinsic matrix
    #that is why gluPerspective is called afterwards to be able to extract the final rotation+translation matrix
    model1 = glGetDoublev(GL_MODELVIEW_MATRIX)
    print(model1.transpose()) #reminder:openGL matrices are in column major order
    # print("Rotation Quaternion :",pyq.Quaternion(matrix = model1[:3,:3].transpose()))
 
def keyPressed(*args):
    print(args[0])
    # if args[0] == '\x1b':
    #     sys.exit()

def react_to_event(event,t_axis,r_axis):
    if event.type == 2:
        
        dist = 0.01
        r_axis1,r_axis2,r_axis3 = r_axis
        t_axis1,t_axis2,t_axis3 = t_axis
        t_axis1,t_axis2,t_axis3 = t_axis1*dist,t_axis2*dist,t_axis3 *dist
        if event.unicode == '\x1b':
            pygame.quit()
        
        elif event.key == 273:
            glTranslatef(t_axis1,t_axis2,t_axis3)
        elif event.key == 274:
            glTranslatef(-t_axis1,-t_axis2,-t_axis3)
       
        elif event.key == 275:
            glRotatef(1,r_axis1,r_axis2,r_axis3)
        elif event.key == 276:
            glRotatef(-1,r_axis1,r_axis2,r_axis3)
        
        #1,2,3 -- choose rotation axis
        elif event.key in [49,257]:
            r_axis[0] = 1
            r_axis[1] = 0
            r_axis[2] = 0
            print("Moving x axis")
        elif event.key in [50,258]:
            r_axis[0] = 0
            r_axis[1] = 1
            r_axis[2] = 0
            print("Moving y axis")
        elif event.key in [51,259]:
            r_axis[0] = 0
            r_axis[1] = 0
            r_axis[2] = 1
            print("Moving z axis")
            
            
        #4,5,6 -- choose translation axis
        elif event.key in [52,260]:
            t_axis[0] = 1
            t_axis[1] = 0
            t_axis[2] = 0
            print("Rotating x axis")
        elif event.key in [53,261]:
            t_axis[0] = 0
            t_axis[1] = 1
            t_axis[2] = 0
            print("Rotating y axis")
        elif event.key in [54,262]:
            t_axis[0] = 0
            t_axis[1] = 0
            t_axis[2] = 1
            print("Rotating z axis")
            
        elif event.key == 115:
            print("Extrinsic Matrix")
            model1 = glGetDoublev(GL_MODELVIEW_MATRIX)
            print(model1.transpose()) #reminder:openGL matrices are in column major order
    
        else:
            print(event.key)
        
    
def main():
    pygame.init()
    
    setup_camera()    
    initialise_extrinsic_matrix()    
    
    # glutKeyboardFunc(keyPressed)
    # glutMainLoop()
    z = 0
    pygame.time.wait(10)       
    r_axis = [1,0,0]
    t_axis = [1,0,0]
    while True:
        for event in pygame.event.get():
            react_to_event(event,r_axis,t_axis)
       
        # glRotatef(2,0,1,0)
#        glTranslate(-0.01, 0,0)
        # z = z-0.0005
        # print(z)
        # glMatrixMode(GL_MODELVIEW)
        # glLoadIdentity()

        # gluLookAt(0.5,0.01,0.5, #camera position
        #       0.038,0.026,0.012,        #where to look 
        #       0,0,1) 
        draw_cube_faces()
        
        pygame.time.wait(50)  
        # print(glGetDoublev(GL_MODELVIEW_MATRIX).transpose())

if __name__ == '__main__':        
    main()
        
