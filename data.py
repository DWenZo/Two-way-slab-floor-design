# -*- coding: utf-8 -*-

' data storage module '

__author__ = 'D. Wenzhuo'

_sc = 1000.0

# size L1 * L2 unit: mm
L1 = 20700.0 # y
L2 = 31500.0 # x

# load unit:kN/m^2
qk = 22.0
gk = 0.0
# unit kN/m^2
q = 0.0
g = 0.0
p = 0.0

# slab size: lx ly unit: m
lx = 4500.0
ly = 6900.0
h = 160

# beam size
l1_b = 400.0 # y
l1_h = 800.0
l2_b = 250.0 # x
l2_h = 500.0

# gama kN/m^3
g_concrete = 25
g_mortar = 20
g_plaster = 17

# calculation


gk = g_concrete * h/_sc + g_mortar*20/_sc + g_plaster*20/_sc

q = 1.5 * qk
g = 1.3 * gk
p = g + q

if __name__ == '__main__':
    print(q)
    print(g)