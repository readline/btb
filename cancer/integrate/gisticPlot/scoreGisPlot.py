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

def importScoreFile(scorePath):
    infile = open(scorePath,'r')
    infile.readline()
    ampcount,delcount = 0,0
    ampdic = {}
    deldic = {}

    while 1:
        line = infile.readline()
        if not line: break
        c = line.rstrip().split('\t')
        if c[0] == 'Amp':
            tmp = [c[1],int(c[2]),int(c[3]),float(c[4]),float(c[5])]
            ampdic[ampcount] = tmp
            ampcount += 1
        elif c[0] == 'Del':
            tmp = [c[1],int(c[2]),int(c[3]),float(c[4]),float(c[5])]
            deldic[delcount] = tmp
            delcount += 1
    infile.close()
    return ampdic, deldic

def main():
    try:
        scorePath = sys.argv[1]
        prefix = sys.argv[2]
    except IndexError:
        sys.exit(sys.argv[0] + ' [score path] [output prefix]')

    chrlendic = {"1":249250621,"2":243199373,"3":198022430,"4":191154276,\
        "5":180915260,"6":171115067,"7":159138663,"8":146364022,\
        "9":141213431,"10":135534747,"11":135006516,"12":133851895,\
        "13":115169878,"14":107349540,"15":102531392,"16":90354753,\
        "17":81195210,"18":78077248,"19":59128983,"20":63025520,\
        "21":48129895,"22":51304566,"X":155270560}
    cytodic = {"1":125000000,"2":93300000,"3":91000000,"4":50400000,\
        "5":48400000,"6":61000000,"7":59900000,"8":45600000,\
        "9":49000000,"10":40200000,"11":53700000,"12":35800000,\
        "13":17900000,"14":17600000,"15":19000000,"16":36600000,\
        "17":24000000,"18":17200000,"19":26500000,"20":27500000,\
        "21":13200000,"22":14700000,"X":60600000}
    chrcumudic = {"1":0,"2":249250621,"3":492449994,"4":690472424,\
        "5":881626700,"6":1062541960,"7":1233657027,"8":1392795690,\
        "9":1539159712,"10":1680373143,"11":1815907890,"12":1950914406,\
        "13":2084766301,"14":2199936179,"15":2307285719,"16":2409817111,\
        "17":2500171864,"18":2581367074,"19":2659444322,"20":2718573305,\
        "21":2781598825,"22":2829728720,"X":2881033286}

    ampdic, deldic = importScoreFile(scorePath)

    colorlist = ['red','blue']

    fig = plt.figure(figsize = (20,20))
    ax1 = fig.add_axes([0.1,0.1,0.38,0.8])
    ax2 = fig.add_axes([0.52,0.1,0.38,0.8])
    ax3 = fig.add_axes([0.49,0.1,0.02,0.8])
    ampxlist,ampylist = [],[]
    delxlist,delylist = [],[]

    for n in range(len(ampdic)):
        # print ampdic[n]
        start = ampdic[n][1] + chrcumudic[ampdic[n][0].strip()]
        end   = ampdic[n][2] + chrcumudic[ampdic[n][0].strip()]
        ampxlist.append(0)
        ampylist.append(start-1)
        ampxlist.append(ampdic[n][3])
        ampylist.append(start)
        ampxlist.append(ampdic[n][3])
        ampylist.append(end)
        ampxlist.append(0)
        ampylist.append(end+1)
    for n in range(len(deldic)):
        # print deldic[n]
        start = deldic[n][1] + chrcumudic[deldic[n][0].strip()]
        end   = deldic[n][2] + chrcumudic[deldic[n][0].strip()]
        delxlist.append(0)
        delylist.append(start-1)
        delxlist.append(deldic[n][3])
        delylist.append(start)
        delxlist.append(deldic[n][3])
        delylist.append(end)
        delxlist.append(0)
        delylist.append(end+1)

    ax1.invert_xaxis()
    ax1.invert_yaxis()
    ax1.plot(ampxlist,ampylist,color=colorlist[0],linewidth=2)

    ax2.plot(delxlist,delylist,color=colorlist[1],linewidth=2)
    ax2.invert_yaxis()

    ax1.axvline(-math.log(0.25,10),0,2881033286,color='green')
    ax2.axvline(-math.log(0.25,10),0,2881033286,color='green')


    ax1.set_ylim([2881033286,0])
    ax2.set_ylim([2881033286,0])
    ax1.set_xlim([max(ampxlist+delxlist),0])
    ax2.set_xlim([0,max(ampxlist+delxlist)])

    ax1.set_xticks(range(0,int(max(ampxlist+delxlist)),2))
    ax1.set_xticklabels(range(0,int(max(ampxlist+delxlist)),2),fontproperties=font(20))
    ax2.set_xticks(range(0,int(max(ampxlist+delxlist)),2))
    ax2.set_xticklabels(range(0,int(max(ampxlist+delxlist)),2),fontproperties=font(20))

    chrstart,chrlen,cyto = [],[],[]
    for n in range(1,23):
        chrlen.append(chrlendic[str(n)])
        chrstart.append(chrcumudic[str(n)])
        cyto.append(chrcumudic[str(n)]+cytodic[str(n)])
    

    ax3.invert_yaxis()
    ax3.set_xlim([0,1])
    ax3.set_ylim([2881033286,0])
    ax3.set_xticks([])
    ax3.set_yticks([])

    for n in range(1,23,2):
        ax1.bar(0,chrlen[n],bottom=chrstart[n],width=max(ampxlist+delxlist),color='grey',alpha=0.3,edgecolor='white')
        ax2.bar(0,chrlen[n],bottom=chrstart[n],width=max(ampxlist+delxlist),color='grey',alpha=0.3,edgecolor='white')
        ax3.bar(0,chrlen[n],bottom=chrstart[n],width=max(ampxlist+delxlist),color='black')
        ax3.axhline(cyto[n],0,1,color='white',linewidth=2,linestyle='-')
        ax3.axhline(cyto[n-1],0,1,color='black',linewidth=2,linestyle='-')
    for n in range(0,22):
        ax1.axhline(cyto[n],0,max(ampxlist+delxlist),color='black',linewidth=1,linestyle=':')
        ax2.axhline(cyto[n],0,max(ampxlist+delxlist),color='black',linewidth=1,linestyle=':')

    yticklist = []
    for n in range(1,23):
        if n%2 == 0:
            yticklist.append(str(n)+'        ')
        else:
            yticklist.append(str(n))

    ax1.set_yticks(cyto)
    ax1.set_yticklabels(yticklist,fontproperties=font(18))
    ax2.set_yticks([])

    ax1.set_xlabel('-log10 amp q-value',fontproperties=font(20))
    ax2.set_xlabel('-log10 del q-value',fontproperties=font(20))







    # ax1.xaxis.set_ticks_position('bottom')
    # ax2.xaxis.set_ticks_position('top')
    # ax1.yaxis.set_ticks_position('left')
    # ax2.yaxis.set_ticks_position('right')

    # # xmax = int(max([-math.log(x,10) for x in ampList]+[-math.log(x,10) for x in delList]))+1
    # # amin,dmin = 1,1
    # # for n in ampList:
    # #     if n < amin and n > 0:
    # #         amin = n
    # # for n in delList:
    # #     if n < dmin and n > 0:
    # #         dmin = n

    # xmax = 0
    # for n in range(len(ampList)):
    #     if ampList[n] == 0 or delList[n] == 0:
    #         continue
    #     else:
    #         if -math.log(ampList[n],10)-math.log(delList[n],10) > xmax:
    #             xmax = -math.log(ampList[n],10)-math.log(delList[n],10)
    # xmax = int(xmax)+1
    # alist,dlist = [],[]
    # for n in range(len(ampList)):
    #     if ampList[n] == 0:
    #         alist.append(xmax)
    #         dlist.append(0)
    #     elif delList[n] == 0:
    #         alist.append(0)
    #         dlist.append(xmax)
    #     else:
    #         alist.append(-math.log(ampList[n],10))
    #         dlist.append(-math.log(delList[n],10))





    # ax1.barh(range(len(idList)),alist,color=colorlist[0],edgecolor=colorlist[0],height=1,align='center')
    # ax2.barh(range(len(idList)),dlist,color=colorlist[1],edgecolor=colorlist[1],height=1,align='center')

    # ax2.invert_xaxis()
    
    # ax1.invert_yaxis()
    # # ax2.invert_yaxis()

    # ax1.set_xlim([0,xmax])
    # ax2.set_xlim([xmax,0])
    # ax1.set_ylim([len(idList)-0.5,-0.5])


    # ax1.set_yticks(range(len(idList)))
    # ax1.set_yticklabels(idList,fontproperties=font(12))

    # plt.setp(ax1.get_yticklines(), visible=False)

    # ax1.set_xlabel('-log10 Amp. q-value',fontproperties=font(16),color=colorlist[0])
    # ax1.set_xticks(range(0,xmax,2))
    # ax1.set_xticklabels(range(0,xmax,2),fontproperties=font(12),color=colorlist[0])

    # ax2.set_xlabel('-log10 Del. q-value',fontproperties=font(16),color=colorlist[1])
    # ax2.set_xticks(range(0,xmax,2))
    # ax2.set_xticklabels(range(0,xmax,2),fontproperties=font(12),color=colorlist[1])
    
    # # ax1.set_title('Group ### arm level\n\n',fontproperties=font(20))

    # # ax2.set_ylim([-0.5,len(idList)-0.5])


    # for n in [2,4,6,8,10,12,14,16,18,20,22,24,25,26,27,29,31,33,35,37,38]:
    #     ax1.axhline(n-0.5,0,15,linewidth=1,color='black',alpha=0.6)
    #     ax2.axhline(n-0.5,0,15,linewidth=1,color='black',alpha=0.6)
    # for n in [1,3,5,7,9,11,13,15,17,19,21,23,28,30,32,34,36]:
    #     ax1.axhline(n-0.5,0,15,linewidth=1,color='black',linestyle='--',alpha=0.6)
    #     ax2.axhline(n-0.5,0,15,linewidth=1,color='black',linestyle='--',alpha=0.6)





    plt.savefig(prefix+'.png')
    # plt.savefig(prefix+'.pdf')


if __name__ == '__main__':
    main()