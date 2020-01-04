# -*- coding: utf-8 -*-
"""
Created on Wed Jan  1 20:11:21 2020

@author: Miguel
"""
import numpy as np

"""  Class to construct pulley systems """

class Vector:
    def __init__(self, F_x, F_y):
        self.Fx = F_x
        self.Fy = F_y
        self.module = None
        self.unitary = None
     
    @property
    def module(self):
        self.module  = np.sqrt(self.Fx**2 + self.Fy**2)
        return self.module
    
    def unitary(self):
        if (self.module > 1e-9):
            if not unitary:
                self.unitary = Vector(self.Fx/self.module, self.Fy/self.module, unitary=True)
            else:
                self.unitary = 'is already unitary' 
        else:
            self.unitary = None
        
class PositionAndLoad:
    def __init__(self, x, y, load = None, fixed = True):
        self.x = x
        self.y = y
        self.load = load
        self.fixed = fixed
    
    def setLoad(self, load):
        self.load = load
        
    def distance(self, another_position):
        return np.sqrt((self.x - another_position.x)**2 + 
                       (self.y - another_position.y)**2)

class Pulley:
    
    """ class docs:
        r1, r2: boundary of the rope
        r_pulley: possition of the pulley.
        
        This vectors contain the possition and optionally the load vector for 
        each point
        """
    radius = 0
    
    def __init__(self, r1, r_pulley, r2):
        
        for _input in (r1, r_pulley, r2):
            if not isinstance(_input, PositionAndLoad):
                raise Exception("Input of a pulley must be instance of 'PositionAndLoad'")
        self.r1 = r1
        self.r2 = r2
        self.r_pulley = r_pulley
        
        self.rope_length = r1.distance(r_pulley) + r2.distance(r_pulley) + np.pi*self.radius
        
        ## make the forces of the system static
        if r1.load is None and r2.load is None:
            if 
            
            
            
            