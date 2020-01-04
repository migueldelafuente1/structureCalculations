# -*- coding: utf-8 -*-
"""
Created on Fri Jan  3 17:14:10 2020

@author: Miguel
"""
import numpy as np
from abc import abstractmethod
class Tree:
    
    """
    This classes define the weight distributions and the gravity and forces
    acting over a simplified pine. 
    
    Inclination and pulling point are considered to evaluate pulley systems inputs.
    
    @inclination: maximum vertical inclination, degrees
    @height: in meters. An stimation could be given by the diameter.
    @diameter: diameter at the ground. in centimeters
    @perimeter: (optional) base circumference in cm.
    
    """
    def __init__(self, inclination= 0. ,diameter= None
                     , height= None, perimeter= None):
        
        self.inclination = 0.
        
        if not diameter:
            if not perimeter:
                raise Exception("Perimeter or diameter are required")
            self.perimeter = perimeter
            self.diameter  = perimeter / np.pi 
        else:
            self.diameter  = diameter
            self.perimeter = np.pi * diameter
        
        self.height = height
        
        print (f"incl:{self.inclination} diam: {self.diameter} perimeter: {self.perimeter} height: {self.height}")
        self.setDensityProfile()
   
    @property
    def height(self):
        return self.__height
    
    @height.setter
    def height(self, height):
        if height:
            self.__height = float(height)
        else:
            self.__height = self.setHeigthProfile()
        
        
    
    @abstractmethod
    def setHeigthProfile(self):
        raise Exception("Heigth profile has to be set in the child classes")
        
    @abstractmethod
    def setDensityProfile(self):
        raise Exception("Density profile has to be set in the child classes")
    

class Pine(Tree):
    def __int__(self, inclination= 0. ,diameter= None
                    , height= None, perimeter= None):
        super().__init__(inclination, diameter, height, perimeter)
    
    def setDensityProfile(self):
        print("Fill me, density as function of height and diameter. regression")
            
t = Pine(diameter = 42., height=10)

        
