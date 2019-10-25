# -*- coding: utf-8 -*-

' test '

from mathutility import *
import data
import pandas as pd
import json


if __name__ == '__main__':
    with open('data.json', 'r') as reader:
        a = json.load(reader)
    print(a)
    d = {'fy':435, 'h0x':65, 'h0y':75}
    with open('data.json', 'w') as writer:
        json.dump(d,writer)
    

    '''
    dxb1 = [1, 2, 3, 4, 5, 6, 7, 8]
    dxb2 = [1, 2, 3, 4, 5, 6, 7, 8]
    dxb3 = [1, 2, 3, 4, 5, 6, 7, 8]
    dxb4 = [1, 2, 3, 4, 5, 6, 7, 8]

    df = pd.DataFrame(['lx/ly', 'ly/lx', 'mx', 'my', 'mxu', 'myu', 'mxb','myb'], columns=['block'])
    df['XB1'] = pd.Series(dxb1)
    df['XB2'] = pd.Series(dxb2)
    df['XB3'] = pd.Series(dxb3)
    df['XB4'] = pd.Series(dxb4)

    df.to_excel('1.xlsx')
    '''