# -*- coding: utf-8 -*-

' main module to run the calculation '

__author__ = 'D. Wenzhuo'

# official module
import os
import sys
import pandas as pd
import numpy as np
import json
import sympy
import datetime

# mine module
import data
import CSIFCal
import cutility as cutil
import mathutility as mutil

_sc = 1000.0

def readData():
    with open('data.json', 'r') as reader:
        dt = json.load(reader)
    return dt

def save(dt):
    with open('data.json', 'w') as writer:
        json.dump(dt, writer)

def elastic():
    # 计算跨度
    # XB1 中部 unit: m
    b1lx = cutil.efSpan(data.lx, 0, data.l1_b, data.h)/_sc
    b1ly = cutil.efSpan(data.ly, 0, data.l2_b, data.h)/_sc

    # XB2 角部
    b2lx = cutil.efSpan(data.lx, 1, data.l1_b, data.h)/_sc
    b2ly = cutil.efSpan(data.ly, 1, data.l2_b, data.h)/_sc

    # XB3 左右
    b3lx = cutil.efSpan(data.lx, 1, data.l1_b, data.h)/_sc
    b3ly = cutil.efSpan(data.ly, 0, data.l2_b, data.h)/_sc

    # XB4 上下
    b4lx = cutil.efSpan(data.lx, 0, data.l1_b, data.h)/_sc
    b4ly = cutil.efSpan(data.ly, 1, data.l2_b, data.h)/_sc

    # 跨中正弯矩
    gAdj = data.g + data.q/2
    qAdj = data.q/2
    p = data.p
    # XB1
    print('dl: 4 fix  +  ll: 4 simply support')
    XB1 = CSIFCal.CSIF(data.L1, data.L2, b1lx, b1ly, data.h, qAdj, gAdj, p)
    dxb1 = XB1.excute()
    print('XB1 completed \n \n ')
    
    # XB2
    print('dl: 2 fix, 2 ss  + ll: 4 simply support')
    XB2 = CSIFCal.CSIF(data.L1, data.L2, b2lx, b2ly, data.h, qAdj, gAdj, p)
    dxb2 = XB2.excute()
    print('XB2 completed \n \n ')

    # XB3
    print('dl: 3 fix, 1 ss  + ll: 4 simply support')
    print('XB3 的x y 与 表格相反 请注意正确查询 mx查my my查mx')
    XB3 = CSIFCal.CSIF(data.L1, data.L2, b3lx, b3ly, data.h, qAdj, gAdj, p)
    dxb3 = XB3.excute()
    print('XB3 completed \n \n ')

    # XB4
    print('dl: 3 fix, 1 ss  + ll: 4 simply support')
    XB4 = CSIFCal.CSIF(data.L1, data.L2, b4lx, b4ly, data.h, qAdj, gAdj, p)
    dxb4 = XB4.excute()
    print('XB4 completed \n \n ')

    dxb1.insert(0,b1lx/b1ly)
    dxb1.insert(0,b1ly/b1lx)

    dxb2.insert(0,b2lx/b2ly)
    dxb2.insert(0,b2ly/b2lx)

    dxb3.insert(0,b3lx/b3ly)
    dxb3.insert(0,b3ly/b3lx)

    dxb4.insert(0,b4lx/b4ly)
    dxb4.insert(0,b4ly/b4lx)

    idx = ['lx/ly', 'ly/lx', 'mx', 'my', 'mxu', 'myu', 'mxb','myb']
    '''
    df = pd.DataFrame(['lx/ly', 'ly/lx', 'mx', 'my', 'mxu', 'myu', 'mxb','myb'], columns=['block'])
    df['XB1'] = pd.Series(dxb1)
    df['XB2'] = pd.Series(dxb2)
    df['XB3'] = pd.Series(dxb3)
    df['XB4'] = pd.Series(dxb4)
    '''
    df = pd.DataFrame({'XB1':dxb1,'XB2':dxb2,'XB3':dxb3,'XB4':dxb4}, idx)
    # As = pd.DataFrame({'XB1':dxb1[2:],'XB2':dxb2[2:],'XB3':dxb3[2:],'XB4':dxb4[2:]}, idx[2:])
    # support 
    df['XB1XB3'] = (df['XB1'] + df['XB3'])/2
    df['XB1XB4'] = (df['XB1'] + df['XB4'])/2
    df['XB2XB3'] = (df['XB2'] + df['XB3'])/2
    df['XB2XB4'] = (df['XB2'] + df['XB4'])/2

    df.iloc[:6,4:] = None
    As = df.copy()

    with open('data.json', 'r') as reader:
        dt = json.load(reader)

    As.iloc[4] = As.iloc[4].apply(lambda x:x*1000000/(0.95*dt['fy']*dt['h0x']))
    As.iloc[5] = As.iloc[5].apply(lambda x:x*1000000/(0.95*dt['fy']*dt['h0y']))
    As.iloc[6] = As.iloc[6].apply(lambda x:x*1000000/(0.95*dt['fy']*dt['h0x']))
    As.iloc[7] = As.iloc[7].apply(lambda x:x*1000000/(0.95*dt['fy']*dt['h0y']))
    As['XB1'] = As['XB1'].apply(lambda x:0.8*x)

    As = As.iloc[4:]
    As = As.apply(lambda x:abs(x))
    with pd.ExcelWriter('elastic.xlsx') as writer:
        df.to_excel(writer, sheet_name='InnerForce')
        As.to_excel(writer, sheet_name='As')


def plastic():
    # 计算跨度
    # XB1 中部 unit: m
    b1lx = cutil.efSpan(data.lx, 3, data.l1_b, data.h)/_sc
    b1ly = cutil.efSpan(data.ly, 3, data.l2_b, data.h)/_sc

    # XB2 角部
    b2lx = cutil.efSpan(data.lx, 4, data.l1_b, data.h)/_sc
    b2ly = cutil.efSpan(data.ly, 4, data.l2_b, data.h)/_sc

    # XB3 左右
    b3lx = cutil.efSpan(data.lx, 4, data.l1_b, data.h)/_sc
    b3ly = cutil.efSpan(data.ly, 3, data.l2_b, data.h)/_sc

    # XB4 上下
    b4lx = cutil.efSpan(data.lx, 3, data.l1_b, data.h)/_sc
    b4ly = cutil.efSpan(data.ly, 4, data.l2_b, data.h)/_sc

    dt = readData()

    # XB1
    p = data.p
    b1 = cutil.yieldLine(b1lx, b1ly, 0.8*p)

    # XB3
    b3 = cutil.yieldLine(b3lx, b3ly, p, b3ly*b1[3], 0)

    # XB4
    b4 = cutil.yieldLine(b4lx, b4ly, p, my1=b4lx*b1[5], my2=0)

    # XB2
    b2 = cutil.yieldLine(b2lx, b2ly, p, b2ly*b4[3], 0, b2lx*b3[5], 0)
    
    idx = ['alpha', 'mx', 'my', 'mx1', 'mx2', 'my1', 'my2']
    df1 = pd.DataFrame({'XB1':b1,'XB2':b2,'XB3':b3,'XB4':b4}, idx, dtype='float')
    df2 = pd.DataFrame({'XB1':b1[1:],'XB2':b2[1:],'XB3':b3[1:],'XB4':b4[1:]}, idx[1:], dtype='float')
    
    df2 = df2.apply(lambda x:x*1000000/(0.95*dt['fy']*dt['h0x']))

    with pd.ExcelWriter('plastic.xlsx') as writer:
        df1.to_excel(writer, sheet_name='InnerForce')
        df2.to_excel(writer, sheet_name='As')

    save(dt)


def beam():
    # live load
    q = data.q * data.lx/1000 # 梯形荷载：此值为 几何梯形的 h
    # dead load
    gb = data.g * data.lx/1000 # 板传来 梯形荷载 : 
    g = 1.3 * ((data.l1_h-data.h)*data.l1_b*data.g_concrete/1000000+(data.l1_h-data.h)/1000*0.02*2*data.g_plaster)
    # 自重 均布

    # 
    a = data.lx/2000
    l = cutil.efSpan(data.ly, 1, 400, 0)  # 两个相等 都是6300
    # l = cutil.efSpan(data.ly, 2, 400, 0)
    l = l/1000  # unit to m
    alp = a/l
    # equivalent
    qe = q*(1-2*alp**2+alp**3)
    gbe = gb*(1-2*alp**2+alp**3)

    print('q gb qe gbe g')
    print(q)
    print(gb)
    print(qe)
    print(gbe)
    print(g)

    sheer_a = []
    sheer_bl = []
    sheer_br = []
    a = data.lx/2000
    # 系数 3跨
    # 1-1-1
    # 1-1-0
    # 1-0-1
    # 0-1-0
    # A1B2C1D
    spMb = [-0.100, -0.117, -0.05, -0.05]
    spMc = [-0.100, -0.033, -0.05, -0.05]

    # SUPPORT maximum bending moment
    # 恒荷载满布
    # live load 1-1-0

    Mb110 = (spMb[0] * (gbe+g) + spMb[1]*qe) * l*l
    V = Mb110/l + (g * l + (gb + q) * (l - 2 * a) + (gb + q) * a) / 2

    sheer_a.append(V)
    sheer_bl.append(-Mb110/l + (g * l + (gb + q) * (l - 2 * a) + (gb + q) * a) / 2)
    sheer_br.append((g * l + (gb + q) * (l - 2 * a) + (gb + q) * a) / 2)

    # SPAN maximum bending moment
    # 恒荷载满布
    # live load 1-0-1

    Ma = 0
    Mb = (spMb[0] * (gbe+g) + spMb[2]*qe) * l*l
    x = sympy.Symbol('x')

    V = Mb/l + (g * l + (gb + q) * (l - 2 * a) + (gb + q) * a) / 2

    sheer_a.append(V)
    sheer_bl.append(-Mb/l + (g * l + (gb + q) * (l - 2 * a) + (gb + q) * a) / 2)
    sheer_br.append((g * l + gb * (l - 2 * a) + gb * a) / 2)

    f = V - ((x - a) * (gb + q) + g * x + (gb + q) * a / 2)
    res = sympy.solve(f, x)
    x0 = res[0]
    M1 = g*x0*x0/2 + (gb+q)*a*a*2/3 + (gb+q)*(x0-a)*(a+(x0-a)/2)

    # live load 0-1-0
    # 对称
    Mb = (spMb[0] * (gbe+g) + spMb[3]*qe) * l*l
    V = (g * l + (gb + q) * (l - 2 * a) + (gb + q) * a) / 2

    sheer_a.append(-Mb / l + (g * l + gb * (l - 2 * a) + gb * a) / 2)
    sheer_bl.append(-Mb / l + (g * l + gb * (l - 2 * a) + gb * a) / 2)
    sheer_br.append((g * l + (gb+q) * (l - 2 * a) + (gb+q) * a) / 2)

    f = V - ((x - a) * (gb + q) + g * x + (gb + q) * a / 2)
    res = sympy.solve(f, x)
    x0 = res[0] # mm
    M2 = g*x0*x0/2 + (gb+q)*a*a*2/3 + (gb+q)*(x0-a)*(a+(x0-a)/2)


    # calculate As
    dt = readData()
    dt['bf'] = l*1000/3
    M = [Mb110, M1, M2]
    b = [dt['b'], dt['bf'], dt['bf']]
    alps = []
    Xi = []
    gms = []
    As = []

    for i, value in enumerate(M):

        a = cutil.getApls(value, dt['fc'], b[i], dt['h0'])
        # print('i:%d M:%f fc:%f b:%f h:%f as:%f' % (i, value, dt['fc'], b[i], dt['h0'], a))
        alps.append(abs(a))
        Xi.append(cutil.getXi(a))
        gms.append(cutil.getGamma(a))
        As.append(cutil.getAs2(gms[i], value, dt['fy'], dt['h0']))

    idx = ['M', 'As']
    df1 = pd.DataFrame([q, gb, qe, gbe, g], ['q', 'gb', 'qe', 'gbe', 'g'])
    df2 = pd.DataFrame(columns=['Mb max', 'M1 max', 'M2 max'])
    df2.loc['M'] = M
    df2.loc['alpha s'] =alps
    df2.loc['Xi'] = Xi
    df2.loc['gms'] = gms
    df2.loc['As'] = As

    # sheer cal
    # 1-1-0
    # 1-0-1
    # 0-1-0
    sheer_max = [max(sheer_a), max(sheer_bl), max(sheer_br)]
    sheer = pd.DataFrame({'Va': sheer_a, 'Vb L': sheer_bl, 'Vb R': sheer_br}, ['1-1-0', '1-0-1', '0-1-0'])
    sheer_Asv = pd.DataFrame(columns=['Va', 'Vb L', 'Vb R'])
    sheer_Asv.loc['V(kN)'] = sheer_max

    bfbh = 0.25*1.0*dt['fc']*dt['b']*dt['h0']/1000
    fbh = 0.7*dt['ft']*dt['b']*dt['h0']/1000
    asvs = [(i-fbh)*1000/(dt['fy']*dt['h0']) for i in sheer_max]

    sheer_Asv.loc['0.25*beta*fcbh0'] = [bfbh, bfbh, bfbh]
    sheer_Asv.loc['0.7ftbh0'] = [fbh, fbh, fbh]
    sheer_Asv.loc['Asv / s'] = asvs

    save(dt)

    with pd.ExcelWriter('beam.xlsx') as writer:
        df1.to_excel(writer, sheet_name='data')
        df2.to_excel(writer, sheet_name='moment')
        sheer.to_excel(writer, sheet_name='sheer')
        sheer_Asv.to_excel(writer, sheet_name='Asv')


if __name__ == '__main__':
    # calculation of loads
    # already complete in data.py module
    start = datetime.datetime.now()
    #elastic()

    #plastic()
    beam()
    end = datetime.datetime.now()
    print(end-start)

