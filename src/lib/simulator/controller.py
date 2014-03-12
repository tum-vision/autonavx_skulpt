'''
Created on 07.02.2014

@author: tatsch
'''

import math
import numpy as np

class Controller():
    '''
    Implements a PIDController
    '''
    #Controller gains, tuned by hand and intuition (4,3,5.5)
    Kd = 10000 #TODO: gains are orders of magnitude too high!
    Kp = 8000 #3
    Ki = 0 #5.5
    dt = 0.1
    
    def __init__(self, drone):
        self.drone=drone
        self.errorIntegral=np.array([[0], [0], [0]])
        
    def calculate_control_command(self,thetaDesired,thetadotDesired,thetadoubledotDesired):

        error=self.Kp*(thetaDesired-self.drone.theta)+self.Kd*(thetadotDesired-self.drone.thetadot)+self.Ki*self.errorIntegral
        self.errorIntegral=self.errorIntegral+self.dt*error
        
        e_phi=-error.item(0)
        e_theta=-error.item(1)
        e_psi=-error.item(2)        

        I_xx=self.drone.I.item((0, 0))
        I_yy=self.drone.I.item((1, 1))
        I_zz=self.drone.I.item((2, 2))
    
        qtt=(self.drone.m*self.drone.g)/(4*self.drone.k*math.cos(self.drone.theta.item(1))*math.cos(self.drone.theta.item(0)))
        gamma1=qtt-(2*self.drone.b*e_phi*I_xx+e_psi*I_zz*self.drone.k*self.drone.L)/4*self.drone.b*self.drone.k*self.drone.L
        gamma2=qtt+e_psi*I_zz/4*self.drone.b-e_theta*I_yy/2*self.drone.k*self.drone.L
        gamma3=qtt-(-2*self.drone.b*e_phi*I_xx+e_psi*I_zz*self.drone.k*self.drone.L)/4*self.drone.b*self.drone.k*self.drone.L
        gamma4=qtt+e_psi*I_zz/4*self.drone.b+e_theta*I_yy/2*self.drone.k*self.drone.L
        
        return [gamma1,gamma2,gamma3,gamma4],e_phi,e_theta,e_psi