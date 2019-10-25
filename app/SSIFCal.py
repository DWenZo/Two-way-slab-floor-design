# -*- coding: utf-8 -*-

'single slab inner force calculation module'

__author__ = 'D. Wenzhuo'

# 
import math
import cutility as cutil

# main func

class SSIF(object):
    def __init__(self, lx, ly, h, q, g, E, poi=0.2):
        # poi: Poisson's ratio 
        # E : elasticity modulus 
        # q : live load
        # g : dead load
        # h : slab TH

        self.lx = lx
        self.ly = ly
        self.h = h
        self.q = q
        self.g = g
        self.E = E
        self.poi = poi
    
        self.Bc = self.cal_Bc()

    # some coefficients
    def cal_Bc(self):
        return (self.E*self.h**2)/(12*(1-self.poi**2))

    # elastic method
    def getM_E(self, coe=0, p = 0):
        '''
        return moment
        '''

        return coe*p*min(self.lx, self.ly)**2
    
    def getNiu_E(self, coe=0):
        '''
        return deflection
        '''
        return coe*(self.g+self.q)*min(self.lx, self.ly)**4/self.Bc

    # plastic method
    def getM_P(self):
        pass
    
    def getNiu_P():
        pass

if __name__ == '__main__':
    a = SSIF(1, 2, 3, 5, 5, 1 )
    a.getM_E(1)