# -*- coding: utf-8 -*-


'continuous slab inner force calculation module'

__author__ = 'D. Wenzhuo'

import SSIFCal
import mathutility as mt

class CSIF(SSIFCal.SSIF):
    def __init__(self, L1, L2, lx, ly, h, q, g, p, E=1, poi=0.2):
        # poi: Poisson's ratio 
        # E : elasticity modulus 
        # q : live load
        # g : dead load
        # h : slab TH
        super().__init__(lx, ly, h, q, g, E, poi);
        self.L1 = L1
        self.L2 = L2
        self.p = p

        #self.Bc = cal_Bc()

    def excute(self):
        xyr = self.lx/self.ly
        yxr = self.ly/self.lx
        print('lx/ly = %f' % xyr)
        print('ly/lx = %f' % yxr)
        print('plz search the coefficient table and input : ')
        print('mx - ')
        com = input('plz input dead load coe \'x0 x1 y0 y1\':')
        ar = com.split()
        ar = [float(x) for x in ar]
        coe1 = mt.ln_interPL(min(xyr, yxr), ar[0], ar[1], ar[2], ar[3])

        com = input('plz input live load coe \'x0 x1 y0 y1\':')
        ar = com.split()
        ar = [float(x) for x in ar]
        coe2 = mt.ln_interPL(min(xyr, yxr), ar[0], ar[1], ar[2], ar[3])
        mx = self.getM_E(coe1, self.g) + self.getM_E(coe2, self.q)


        print('my - ')
        com = input('plz input dead load coe \'x0 x1 y0 y1\':')
        ar = com.split()
        ar = [float(x) for x in ar]
        coe1 = mt.ln_interPL(min(xyr, yxr), ar[0], ar[1], ar[2], ar[3])

        com = input('plz input live load coe \'x0 x1 y0 y1\':')
        ar = com.split()
        ar = [float(x) for x in ar]
        coe2 = mt.ln_interPL(min(xyr, yxr), ar[0], ar[1], ar[2], ar[3])
        my = self.getM_E(coe1, self.g) + self.getM_E(coe2, self.q)
        
        print(' mx\' ')
        com = input('plz input live load coe \'x0 x1 y0 y1\':')
        ar = com.split()
        ar = [float(x) for x in ar]
        coe = mt.ln_interPL(min(xyr, yxr), ar[0], ar[1], ar[2], ar[3])
        mxb = self.getM_E(coe, self.p)

        print(' my\' ')
        com = input('plz input live load coe \'x0 x1 y0 y1\':')
        ar = com.split()
        ar = [float(x) for x in ar]
        coe = mt.ln_interPL(min(xyr, yxr), ar[0], ar[1], ar[2], ar[3])
        myb = self.getM_E(coe, self.p)
        
        return [mx, my, mx+self.poi*my, my+self.poi*mx, mxb, myb]

    def log(self):
        print('Bc=%f; poisson\'s ratio =%f; elasticity = %f' % (self.Bc, self.poi, self.E))


if __name__ == '__main__':
    a = CSIF(2, 4, 1, 2, 100, 10, 20, 50)
    a.log()