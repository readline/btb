#!/usr/bin/env python
# armSigPlot.py
# version 1.0
# Kai Yu
# github.com/readline
# 150420
##############################################
from __future__ import division
import os,sys,math
import matplotlib
matplotlib.use('Agg')
import os,sys,matplotlib,pylab
import matplotlib.pyplot as plt

def font(size):
    return matplotlib.font_manager.FontProperties(size=size,fname='/Share/BP/yukai/src/font/ARIAL.TTF')

def importSigFile(armSigPath):
    infile = open(armSigPath,'r')
    idList, ampList, delList = [],[],[]
    while 1:
        line = infile.readline()
        if not line: break
        if line[0] == '#' or line[:3] == 'Arm':continue
        c = line.rstrip().split('\t')
        idList.append(c[0])
        ampList.append(float(c[4]))
        delList.append(float(c[7]))
    return idList,ampList,delList

def main():
    try:
        armSigPath = sys.argv[1]
        prefix = sys.argv[2]
    except IndexError:
        sys.exit(sys.argv[0] + ' [gistic arm sig path] [output prefix]')

    idList,ampList,delList = importSigFile(armSigPath)

    colorlist = ['#CC3333','#336699']

    fig = plt.figure(figsize = (10,16))
    ax1 = fig.add_axes([0.15,0.1,0.7,0.8])
    ax2 = ax1.twiny()
    ax1.xaxis.set_ticks_position('bottom')
    ax2.xaxis.set_ticks_position('top')
    ax1.yaxis.set_ticks_position('left')
    ax2.yaxis.set_ticks_position('right')

    # xmax = int(max([-math.log(x,10) for x in ampList]+[-math.log(x,10) for x in delList]))+1
    # amin,dmin = 1,1
    # for n in ampList:
    #     if n < amin and n > 0:
    #         amin = n
    # for n in delList:
    #     if n < dmin and n > 0:
    #         dmin = n

    xmax = 0
    for n in range(len(ampList)):
        if ampList[n] == 0 or delList[n] == 0:
            continue
        else:
            if -math.log(ampList[n],10)-math.log(delList[n],10) > xmax:
                xmax = -math.log(ampList[n],10)-math.log(delList[n],10)
    xmax = int(xmax)+1
    alist,dlist = [],[]
    for n in range(len(ampList)):
        if ampList[n] == 0:
            alist.append(xmax)
            dlist.append(0)
        elif delList[n] == 0:
            alist.append(0)
            dlist.append(xmax)
        else:
            alist.append(-math.log(ampList[n],10))
            dlist.append(-math.log(delList[n],10))





    ax1.barh(range(len(idList)),alist,color=colorlist[0],edgecolor=colorlist[0],height=1,align='center')
    ax2.barh(range(len(idList)),dlist,color=colorlist[1],edgecolor=colorlist[1],height=1,align='center')

    ax2.invert_xaxis()
    
    ax1.invert_yaxis()
    # ax2.invert_yaxis()

    ax1.set_xlim([0,xmax])
    ax2.set_xlim([xmax,0])
    ax1.set_ylim([len(idList)-0.5,-0.5])


    ax1.set_yticks(range(len(idList)))
    ax1.set_yticklabels(idList,fontproperties=font(12))

    plt.setp(ax1.get_yticklines(), visible=False)

    ax1.set_xlabel('-log10 Amp. q-value',fontproperties=font(16),color=colorlist[0])
    ax1.set_xticks(range(0,xmax,2))
    ax1.set_xticklabels(range(0,xmax,2),fontproperties=font(12),color=colorlist[0])

    ax2.set_xlabel('-log10 Del. q-value',fontproperties=font(16),color=colorlist[1])
    ax2.set_xticks(range(0,xmax,2))
    ax2.set_xticklabels(range(0,xmax,2),fontproperties=font(12),color=colorlist[1])
    
    # ax1.set_title('Group ### arm level\n\n',fontproperties=font(20))

    # ax2.set_ylim([-0.5,len(idList)-0.5])


    for n in [2,4,6,8,10,12,14,16,18,20,22,24,25,26,27,29,31,33,35,37,38]:
        ax1.axhline(n-0.5,0,15,linewidth=1,color='black',alpha=0.6)
        ax2.axhline(n-0.5,0,15,linewidth=1,color='black',alpha=0.6)
    for n in [1,3,5,7,9,11,13,15,17,19,21,23,28,30,32,34,36]:
        ax1.axhline(n-0.5,0,15,linewidth=1,color='black',linestyle='--',alpha=0.6)
        ax2.axhline(n-0.5,0,15,linewidth=1,color='black',linestyle='--',alpha=0.6)





    plt.savefig(prefix+'.png')
    plt.savefig(prefix+'.pdf')


if __name__ == '__main__':
    main()