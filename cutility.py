# -*- coding: utf-8 -*-

'''
contain useful tools for concrete structure design
'''

import sympy
from sympy.core import numbers as spn
import math

__author__ = 'D. Wenzhuo'


def getApls(m, fc, b, h, alp1=1.0):
    '''

    :param m: kN*m
    :param alp1: 1.0
    :param fc: concrete design strength : N/mm^2
    :param b: beam's width : mm
    :param h: beam's height - as : mm
    :return: Alpha_s
    '''
    return m*1000000/(alp1*fc*b*h*h)


def getXi(alps):
    '''

    :param alps: Alpha_s
    :return: Xi
    '''
    x = 1-2*alps
    return 1 - sympy.sqrt(x)

def getGamma(alps):
    '''

    :param alps: Alpha_s
    :return: gamma_s
    '''

    x = 1-2*alps
    return (1 + sympy.sqrt(x))/2


def getAs2(gm, M, fy, h):
    '''

    :param gm: γ gamma
    :param M: moment
    :param fy: stell strength
    :param h: height - as
    :return: As
    '''
    return M*1000000/(gm*fy*h)


def getAs1(xi, b, h, fc, fy, alps=1.0):
    '''

    :param xi: Xi
    :param b: beam's width: mm
    :param h: beam's height - as: mm
    :param fc: concrete design strength : N/mm^2
    :param fy: steel design strength : N/mm^2
    :param alps: Alpha_s 1.0
    :return: As
    '''
    return xi*b*h*alps*fc/fy

def yieldLine(lx, ly, p, mx1=None, mx2=None, my1=None,my2=None, beta=2.0):
    '''

    :param lx:
    :param ly:
    :param p:
    :param mx1:
    :param mx2:
    :param my1:
    :param my2:
    :param beta:
    :return: yield line method
    '''
    n = ly/lx
    alp = 1/(n*n)

    x = sympy.Symbol('x')

    if mx1 == None:
        mx1 = beta*ly*x
    if mx2 == None:
        mx2 = beta*ly*x
    if my1 == None:
        my1 = beta*alp*lx*x
    if my2 == None:
        my2 = beta*alp*lx*x

    f = 2*(ly*x + alp*lx*x) + mx1 + mx2 + my1 + my2 - p*lx*lx*(3*ly-lx)/12

    res = sympy.solve(f, x)
    m = res[0]

    if isinstance(mx1, (type(sympy.Float(1)), int)):
        mx1 = mx1/ly
    else:
        mx1 = beta * m

    if isinstance(mx2, (type(sympy.Float(1)), int)):
        mx2 = mx2/ly
    else:
        mx2 = beta * m

    if isinstance(my1, (type(sympy.Float(1)), int)):
        my1 = my1/lx
    else:
        my1 = beta * m

    if isinstance(my2, (type(sympy.Float(1)), int)):
        my2 = my2/lx
    else:
        my2 = beta * m


    return [alp, m, alp*m, mx1, mx2, my1, my2]
    



def efSpan(lc, type, b, h, a=240):
    '''
    return the effective span 
    lc : Distance of center line of support
    type: 
        0 - 两端支承在梁上
        1 - 一端墙一端梁
        2 - 两端支承在墙上
        0 1 2 弹性
        3 4 5 对应 0 1 2 塑性
    a : 在墙上支承长度
    b : 在支座上支承的长度

    if h = 0 indicate that is a beam
    else that is a slab
    '''
    if type == 0:
        return lc
    elif type == 1:
        ln = lc - 120 - b/2
        if h == 0:
            return min(ln + b/2 + a/2, 1.025*ln + b/2)
        else:
            return min(ln + b/2 + a/2, ln + b/2 + h/2)
    elif type == 2:
        ln = lc - 240
        if h == 0:
            return min(ln+a, 1.05*ln)
        else:
            return min(ln+a, ln + h)
    elif type == 3:
        return lc-b
    elif type == 4:
        ln = lc - 120 - b/2
        if h == 0:
            return min(ln + a/2, 1.025*ln)
        else:
            return min(ln + a/2, ln + h/2)
    elif type == 5:
        ln = lc - 240
        if h == 0:
            return min(ln + a, 1.05*ln)
        else:
            return min(ln+a, ln+h)

if __name__ == '__main__':
    lx = 4.8
    ly = 5.8
    p = 10.89
    a = yieldLine(lx, ly, p, 43.85, 0)
    print(a)