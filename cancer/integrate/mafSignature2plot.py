#!/usr/bin/env python
# Kai Yu
# github.com/readline
# mafSignature2plot.py
# 150410

from __future__ import division
import os,sys,math
from mpl_toolkits.mplot3d import Axes3D
import matplotlib
matplotlib.use('Agg')
import os,sys,matplotlib,pylab
import matplotlib.pyplot as plt
import numpy as np

def font(size):
    return matplotlib.font_manager.FontProperties(size=size,\
        fname='/Share/BP/yukai/src/font/ARIAL.TTF')
def fontConsola(size):
    return matplotlib.font_manager.FontProperties(size=size,\
        fname='/Share/BP/yukai/src/font/consola.ttf')

def getMatrix(sigPath):
    infile = open(sigPath,'r')
    countn = infile.readline().rstrip().split('=')[1]
    mutList, tmpList = [],[]
    sumdic = {'TA':0,'TC':0,'TG':0,'CA':0,'CG':0,'CT':0}
    while 1:
        line = infile.readline().rstrip()
        if not line: break
        c = line.split('\t')
        mutList.append(c[0])
        tmpList.append(float(c[1]))
        bmut = c[0].split('>')[0][1] + c[0].split('>')[1][1]
        sumdic[bmut] += float(c[1])
    sumList = []
    for bmut in ['TA','TC','TG','CA','CG','CT']:
        sumList.append(sumdic[bmut]) 
    infile.close()
    return mutList, tmpList, sumList, countn

def getC(c):
    tmpdic = []
    for n in range(6):
        for m in range(16):
            tmpdic.append(c[n])
    return tmpdic

def main():
    try:
        sigPath = sys.argv[1]
    except:
        print sys.argv[0] + ' [input signature path]'
        sys.exit()
    mutList, mat, sumList,countn = getMatrix(sigPath)

    ### Start plot
    c = ['#FFFF99','#CCCCFF','#FFCC99','#CCFFCC','#CCFFFF','#FF9999']
    col = getC(c)
    fig = plt.figure(figsize = (20,10))
    topy = int((max(mat)//5+1)*5)

    ax1 = fig.add_axes([0.08,0.15,0.83,0.7])
    ax2 = fig.add_axes([0.1,0.46,0.19,0.38])

    ax1.set_xlim([0,96])
    ax1.set_ylim([0,topy])

    ax1.bar(range(96),mat,width=1,linewidth=0.5,color=col,alpha=1)
    ax1.vlines([16,32,48,64,80],0,topy,linestyle='--',linewidth=1,color='black',alpha=0.7)
    ax1.hlines(range(0,topy+1,5),0,96,linestyle='--',linewidth=1,color='black',alpha=0.7)

    ax3 = ax1.twiny()
    ax3.set_xlim([0,96])
    ax3.set_ylim([0,topy])
    ax3.set_xticks(range(8,96,16))
    ax3.set_xticklabels(['T > A','T > C','T > G','C > A','C > G','C > T'],fontproperties=font(30))
    plt.setp(ax3.get_xticklines(), visible=False)

    mutList1 = []
    for n in mutList:
        mutList1.append(n[:3])
    mutList0 = []
    for n in range(96):
        mutList0.append(n+0.7)
    ax1.set_xticks(mutList0)
    plt.setp(ax1.get_xticklines(), visible=False)
    ax1.set_xticklabels(mutList1, fontproperties=fontConsola(16),rotation='vertical')

    ax1.set_yticks(range(0,topy+1,5))
    ax1.set_yticklabels(range(0,topy+1,5),fontproperties=font(24))
    ax1.set_ylabel('Normalized rate / Mb',fontproperties=font(30))

    #   Pie plot
    ax2.set_xticks([])
    ax2.set_yticks([])
    pielabel = ['T>A','T>C','T>G','C>A','C>G','C>T']
    explode = [0.32,0.29,0.26,0.23,0.2,0]
    pie1 = ax2.pie(sumList,labels=pielabel, explode=explode,colors=c,shadow=True,startangle=270)
    for i in pie1[1]:
        # print i
        i.set_fontproperties(font(24))
        # i.set_backgroundcolor('white')
    ax1.text(32,topy*0.8,'%s\nn = %s'%(sigPath.split('/')[-1][:-10],countn),fontproperties=font(32),backgroundcolor='white')

    plt.savefig(sigPath+'.sigplot.png')
    plt.savefig(sigPath+'.sigplot.pdf')

if __name__ == '__main__':
    main()



