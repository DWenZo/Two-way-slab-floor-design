# -*- coding: utf-8 -*-

'''
there are some useful functions in this module 

you can also use the functions in console directly
    format : 'function_name' *parameters

containing : 
ln_interPL(x, x0, x1, y0, y1) Lagrange polynomial intepolation

'''

__author__ = ' D. Wenzhuo '

import sys
import math


'''
Interpolation 
'''
# linear interpolation
# Lagrange polynomial interpolation
def ln_interPL(x, x0, x1, y0, y1):
    # x : you require independent variable
    # (x1, y1) and (x0, y0) is already known
    return y0 + (y1-y0)/(x1-x0) * (x-x0)

def tableIPL():
    str = input('plz input m1: x, x0, x1, y0, y1')
    y0 = eval('ln_interPL('+str + ')')
    str = input('plz input m2: x, x0, x1, y0, y1')
    y1 = eval('ln_interPL('+str + ')')
    str = input('plz input n: x, x0, x1, y0, y1')
    return eval('ln_interPL('+str + ')')

# GCD & LCM
def GCD(a, b):
    if (b == 0):
        return a
    return GCD(b, a%b)

def LCM(a, b):
    return a*b/GCD(a, b)

def exit():
    sys.exit()

if __name__ == '__main__':
    while True:
        str = input('math utilty >')
        res = eval(str)
        print('math utilty>', end='')
        print(res)
'''
if __name__ == '__main__':
    str = sys.argv[1] + '('
    para = sys.argv[2: ]
    for o in para:
        str = str + o + ','
    
    execute = str[:-1]+')'
    
    print('Execute : ' + execute + '\n RESULT : ', end = '')

    print(eval(execute))
'''