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
        
        self.inclination = inclination
        
        if not diameter:
            if not perimeter:
                raise Exception("Perimeter or diameter are required")
            self.perimeter = perimeter
            self.diameter  = perimeter / np.pi 
        else:
            self.diameter  = diameter
            self.perimeter = np.pi * diameter
        
        self.height = height
        
        print (f"inclination: {self.inclination}º\ndiameter: {self.diameter} cm",
               f"\nperimeter: {self.perimeter} cm\nheight: {self.height} m")
   
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
    
class PineException(Exception):
    pass
class Pine(Tree):
    """
    Class Docs.      [Pine] --> [Tree]
    
    * Description of the pine model arguments:
        
           vvvvvvvvv---------------------------
         vvvvvvvvvvvvv                       ^ 
        vvvvvvvvvvvvvvv <-- _topCentroid_z   |- top_height  
          vvvvvvvvvvv________________________v
              ||         ^            >( )< top_diameter 
              ||
              ||         ·
              ||         |- height
             |  |        ·
             |  |<----- centroidHeight
             |  |<----- _trunkCentroid_z 
             |  |
            |    |
         ___|    |_______V__          >(   )< diameter
         
    The density profile is the combination of a truncated cone for the trunk 
    and a point like mass for the upper part, that sumarize the centroid of an
    homogeneous bunch of leaves and branches.
    
    The density considered for the wood could be normal or lower if the pine 
    is dead and partialy rotten.
    
    Args:
    =========================================================
    * :inclination:  [deg] Angle between the trunk and the vertical
    * :diameter:     [cm]  Diameter at the base
    * :top_diameter: [cm]  Diameter of the trunk before the begining of the branches
    * :height:       [m]   Height of the trunk before the begining of the branches
    * :top_height:   [m]   Height of the top part of the pine.
    * :pineStatus:   [NORMAL or ROTTEN]. Defines the expected density.
    
    =========================================================
    """
    
    class PineStatus:
        ROTTEN = 'rotten'
        NORMAL = 'normal'
         
    def __init__(self, inclination= 0. ,diameter= None
                    , height= None, perimeter= None
                    , top_height= None, top_diameter=None
                    , pineStatus=PineStatus.NORMAL):
        print(self.__doc__)
        print('SETTING UP PINE ...\n')
        #print("Height goes from the ground to the begining of the branches")
        super().__init__(inclination, diameter, height, perimeter)
        
        """ Definitions of the upper part parameters if they are fixed, 
        otherwise, they are set by estimations"""
        self.topHeight = top_height
        self.topDiameter = top_diameter
        self.density = pineStatus
        
        self.setDensityProfile()
    
    
    """ TODO: Find the correct regresions for the following properties."""
    
    @property
    def density(self):
        return self.__density
    @density.setter
    def density(self, pineStatus):
        """ Density defined in [kg / cm3] in terms of the pine status"""
        if pineStatus is self.PineStatus.NORMAL:
            self.__density = 0.0009 
        elif pineStatus is self.PineStatus.ROTTEN:
            self.__density = 0.0007
        else:
            raise PineException("pineStatus can only be NORMAL or ROTTEN:", 
                                "got [{}]".format(pineStatus))
    
    @property
    def topHeight(self):
        return self.__topHeight
    @topHeight.setter
    def topHeight(self, top_height):
        if top_height:
            if (top_height > self.height/3) or (top_height < self.height/6):
                print("WARNING: Very extrange pine definition",
                      "top height is > 0.33 trunk heigt or < trunk height / 6")
            self.__topHeight = top_height
        else:
            self.__topHeight = self.height / 4
    
    @property
    def topDiameter(self):
        return self.__topDiameter
    @topDiameter.setter
    def topDiameter(self, top_diameter):
        if top_diameter:
            if top_diameter > self.diameter:
                raise PineException("A pine cannot be more widder in the top [{} cm]"
                                    .fotmat(top_diameter), " than in the base[{} cm]."
                                    .format(self.diameter))
                
            elif (top_diameter > 0.9 * self._trunkDiameter()):
                print("WARNING: Extrange pine definition, too cilindrical profile.",
                      "top diameter is more than 90 % bigger than the base estimation")
            elif (top_diameter < 0.5 * self._trunkDiameter()):
                print("WARNING: Extrange pine definition, too conical profile",
                      "top diameter is 50 % lower than from the base estimation")
            
            self.__topDiameter = top_diameter
        else:
            self.__topDiameter = self._trunkDiameter(h=self.height)
    
    
    def _trunkDiameter(self, h=7):
        # rough approximation:
        # (30 cm - 20 cm) / 7m = 10 cm / 7 m = 1.4285 cm / m
        return self.diameter - 1.4285 * h
    
    def _pineSystemMasses(self, trunk_mass, top_mass):
        self.trunk_mass = trunk_mass
        self.top_mass = top_mass
        self.totalMass = trunk_mass + top_mass
    
    def setDensityProfile(self):
        """ 
        Definition of the mass distribution from the description.
        Inclination will be taken into account after.
        
        * Trunk is treated as a truncated cone.
        * The centroid of the branches will be sum into a point like mass.
        
        The centroid of the sistem will be the average sum of the two.
        + density is in kg/cm3
        + height in meters
        + diameters in cm
        """
        t_volume = (self.topDiameter**2 + 
                     self.topDiameter*self.diameter +
                     self.diameter**2) / 4
        self._trunkCentroid_z = (.25 * (self.height * 100)* 
                                  (3 * (self.topDiameter**2) +  
                                  2 * self.topDiameter * self.diameter + 
                                  self.diameter**2)) /(4 * t_volume)
        
        self._trunkCentroid_z = self._trunkCentroid_z / 100           ## in [m]
        trunk_mass = self.density * t_volume * np.pi * (100*self.height) / 3
        
        # the top part has the density profile of a cone:
        self._topCentroid_z   = self.topHeight / 4
        # this estimation come from comparing the volume of wood from the 
        # branches compared with the trunks. 
        #    $$pi*topH*(diam/2)**2 / 3 = 2.5'parts' * 1.5*pi*(top_diam/2)**2 $$
        top_mass = self.density * (294.52 * self.topDiameter**2)
        
        self._pineSystemMasses(trunk_mass, top_mass)
        
        self.centroidHeight = ((trunk_mass * self._trunkCentroid_z + 
                                top_mass * (self._topCentroid_z + self.height))
                               / self.totalMass)
        
        self._applyInclination()
    
    def _applyInclination(self):
        _alpha = np.deg2rad(self.inclination)
        self.centroidHeight = self.centroidHeight * np.cos(_alpha)
        self.centroidLenght = self.centroidHeight * np.sin(_alpha) * 100
        
        if abs(self.centroidLenght) > (self.diameter / 2):
            print("\n*WARNING !!\n",
                    "Centroid projection outside the tree basis.\n", 
                  f"centroidLenght: [{self.centroidLenght} cm] \n radius: [{.5*self.diameter} cm]",
                  "\n---------------------------------")
            self.centroidProjectionInsideBase = False
        else:
            self.centroidProjectionInsideBase = True
        
        
        
        
        
            
t = Pine(diameter = 30., height=7, top_diameter= 20., top_height= 2., 
         inclination= 3. )
print("\n\nPINE RESULT DESCRIPTION:\n========================")
print('top_diameter\t=',t.topDiameter)
print('top_heigth\t=',t.topHeight)
print('----------')
print('top mass\t=', t.top_mass)
print('trunk mass\t=',t.trunk_mass)
print('total\t\t=', t.totalMass)
print('----------')
print('centroid_top\t=',t._topCentroid_z)
print('centroid_trunk\t=',t._trunkCentroid_z)
print()
print('centroid', t.centroidHeight)

        
