#!/usr/bin/env python
# coMutPlot.py
# version 1.0
# Kai Yu
# github.com/readline
# 150413

from __future__ import division
import os,sys,math
import matplotlib
matplotlib.use('Agg')
import os,sys,matplotlib,pylab
import matplotlib.pyplot as plt
import numpy as np

def font(size):
    return matplotlib.font_manager.FontProperties(size=size,fname='/Share/BP/yukai/src/font/ARIAL.TTF')

def importMatrix(matrixPath):
    geneList = []
    matrix = []
    infile = open(matrixPath,'r')
    sampleList = infile.readline().rstrip().split('\t')[1:]
    while 1:
        line = infile.readline()
        if not line: break
        c = line.rstrip().split('\t')
        geneList.append(c[0])
        matrix.append([int(n) for n in c[1:]])
    infile.close()
    return matrix, geneList, sampleList

def importSampleRate(sampleRatePath):
    misList, silList = [],[]
    infile = open(sampleRatePath,'r')
    infile.readline()
    while 1:
        line = infile.readline()
        if not line: break
        c = line.rstrip().split('\t')
        misList.append(float(c[3]))
        silList.append(float(c[4]))
    infile.close()
    return misList, silList

def importMeta(clinicPath):
    infile = open(clinicPath,'r')
    infile.readline()
    gender,grade = [],[]
    while 1:
        line = infile.readline()
        if not line: break
        c = line.rstrip().split('\t')
        if c[4] == 'F':
            gender.append(1)
        elif c[4] == 'M':
            gender.append(2)
        else:
            gender.append(0)

        if c[8] == '2':
            grade.append(3)
        elif c[8] == '3':
            grade.append(4)
        elif c[8] == '4':
            grade.append(5)
        else:
            grade.append(0)
    infile.close()
    metaMat = [gender,grade]
    return metaMat

def importSampleType(sampleTypePath):
    tmp = []
    infile = open(sampleTypePath,'r')
    infile.readline()
    while 1:
        line = infile.readline()
        if not line:
            break
        tmp.append([float(n) for n in line.rstrip().split('\t')[1:]])
    infile.close()
    return tmp

def importGeneRate(geneMutCountPath):
    infile = open(geneMutCountPath,'r')
    infile.readline()
    misList, silList = [],[]
    while 1:
        line = infile.readline()
        if not line: break
        c = line.rstrip().split('\t')
        misList.append(int(c[2]))
        silList.append(int(c[8]))
    infile.close()
    return [misList,silList]

def importGeneFDR(geneMutResultPath):
    tmp = []
    infile = open(geneMutResultPath,'r')
    header = infile.readline()
    if header.rstrip().split('\t')[-1] == 'q':
        fdrtitle = 'q-value (-log10)'
    else:
        fdrtitle = 'FDR CT (-log10)'
    while 1:
        line = infile.readline()
        if not line: break
        c = line.rstrip().split('\t')
        fdr = float(c[-1])
        if fdr == 0:
            tmp.append(20)
        else:
            tmp.append(-math.log10(float(c[-1])))
    infile.close()
    return tmp, fdrtitle


def main():
    try:
        matrixPath = sys.argv[1]
        sampleRatePath = sys.argv[2]
        sampleTypePath = sys.argv[3]
        geneMutCountPath = sys.argv[4]
        geneMutResultPath = sys.argv[5]
        clinicPath = sys.argv[6]
        prefix = sys.argv[7]
    except:
        print sys.argv[0] + ' [matrixPath] [sampleRatePath] [sampleTypePath] [geneMutCountPath] [geneMutResultPath] [output prefix]'
        exit()

    fig = plt.figure(figsize = (20,20))
    ax = {}
    ax[11] = fig.add_axes([0.01,0.88,0.11,0.06], frameon=False)
    ax[12] = fig.add_axes([0.18,0.88,0.6,0.1])  #sample mut rate
    ax[13] = fig.add_axes([0.82,0.86,0.15,0.1], frameon=False)

    ax[21] = fig.add_axes([0.01,0.22,0.125,0.65]) # gene mut rate
    ax[22] = fig.add_axes([0.18,0.22,0.6,0.65])  #mut heatmap
    ax[23] = fig.add_axes([0.85,0.22,0.12,0.65])

    ax[32] = fig.add_axes([0.18,0.18,0.6,0.03])  # meta

    ax[42] = fig.add_axes([0.18,0.07,0.6,0.1])
    ax[41] = fig.add_axes([0.01,0.07,0.15,0.1], frameon=False)
    ax[4311] = fig.add_axes([0.82,0.09,0.15,0.08], frameon=False)


    ### heatmap
    matrix, geneList, sampleList = importMatrix(matrixPath)
    # ax[22].set_xlim([0,len(matrix[0])])
    # ax[22].set_ylim([0,len(matrix)])

    # codeDic = { "Missense_Mutation":1,
    #         "Frame_Shift_Del":2,
    #         "Frame_Shift_Ins":2,
    #         "In_Frame_Del":3,
    #         "In_Frame_Ins":3,
    #         "Splice_Site":4,
    #         "Nonstop_Mutation":5,
    #         "Nonsense_Mutation":6,
    #         "Silent":7,
    #         "3'Flank":8,
    #         "3'UTR":8,
    #         "5'Flank":8,
    #         "5'UTR":8,
    #         "Intergenic":'0',
    #         "Intron":8,
    #         "RNA":8}

    # colorlist = ['#f0f0f0','#336699','#FF9900','#ff00ea','#996699','#FF6666','#CCCC66','#99CC33','#CCCCCC']
    colorlist = ['#f0f0f0','#336699','#FF9900','#99CCFF','#996699','#FF6666','#FFFF00','#99CC33','#CCCCCC']
    #             blank    missense   fsINDEL   ifINDEL    splice    nonstop   nonsense  silent    other
    colorDic = {}
    for n in range(len(colorlist)):
        colorDic[n] = colorlist[n]


    colormap = matplotlib.colors.ListedColormap(colorlist)
    norm = matplotlib.colors.Normalize(vmin=0,vmax=8)
    im = ax[22].imshow(matrix, cmap=colormap,norm=norm, interpolation='nearest', aspect='auto')
    # ax[22].set_xlim([-0.5,len(matrix[0])-0.5])
    # ax[22].set_ylim([-0.5,len(matrix)-0.5])
    ax[22].vlines([n-0.51 for n in range(1,len(matrix[0]))],-0.5, len(matrix)-0.5, color='white',linewidth=1.4)
    ax[22].hlines([n-0.51 for n in range(1,len(matrix))],-0.5, len(matrix[0])-0.5, color='white',linewidth=1.4)
    ax[22].set_xticks([])
    ax[22].set_yticks([])



    # ax[100] = fig.add_axes([0.1,0.1,0.02,0.5])
    # cb = matplotlib.colorbar.ColorbarBase(ax[100], cmap=colormap,norm=norm)

    ### top sample mutation type rate
    misList, silList = importSampleRate(sampleRatePath)
    ax[12].set_xlim([0,len(misList)])
    ax[12].bar(range(len(misList)), misList, color=colorDic[1],width=0.95,edgecolor='white')
    ax[12].bar(range(len(silList)), silList, color=colorDic[7],width=0.95,edgecolor='white',bottom=misList)
    ax[12].spines['right'].set_visible(False)
    ax[12].spines['top'].set_visible(False)
    ax[12].spines['bottom'].set_visible(False)
    ax[12].set_xticks([])
    ax[12].yaxis.set_ticks_position('left')
    ax[12].set_yticks(range(0,int(max([a+b for a,b in zip(misList,silList)]))+1,2))
    ax[12].set_yticklabels(range(0,int(max([a+b for a,b in zip(misList,silList)]))+1,2),fontproperties=font(16))
    ax[12].get_yaxis().set_tick_params(direction='out')
    ax[12].set_ylabel('# mutations / Mb',fontproperties=font(16))
    for loc, spine in ax[12].spines.items():
        if loc in 'left':
            spine.set_position(('outward', 10))  # outward by 10 points
            spine.set_smart_bounds(True)



    ### meta heatmap
    metaMat = importMeta(clinicPath)
    norm2 = matplotlib.colors.Normalize(vmin=0,vmax=5)
    metaCol = ['#f0f0f0','#FF99CC','#99CCFF','#99CC66','#FFFF66','#FF6666']
    #            NA        Female     Male     grade2     grade3   grade4
    metaColorDic = {}
    for n in range(len(colorlist)):
        metaColorDic[n] = colorlist[n]

    metaColMap = matplotlib.colors.ListedColormap(metaCol)
    ax[32].imshow(metaMat, cmap=metaColMap,norm=norm2, interpolation='nearest', aspect='auto')
    ax[32].vlines([n-0.5 for n in range(len(metaMat[0]))],-0.5, len(metaMat)-0.5, color='white',linewidth=1)
    ax[32].hlines([n-0.53 for n in range(len(metaMat))],-0.5, len(metaMat[0])-0.5, color='white',linewidth=1)
    ax[32].set_xticks([])
    ax[32].set_yticks([])



    ### bottom sample mut type
    sampleTypeMat = importSampleType(sampleTypePath)
    sampleTypeCol = ['#99d594','#e6f598','#fee08b','#fc8d59','#d53e4f']
    sampleColorDic = {}
    for n in range(len(sampleTypeCol)):
        metaColorDic[n] = sampleTypeCol[n]

    bsmt = {}
    bsmt[0] = ax[42].bar(range(len(sampleTypeMat[0])), sampleTypeMat[0], color=sampleTypeCol[0],width=1,edgecolor=sampleTypeCol[0],bottom=[a+b+c+d for a,b,c,d in zip(sampleTypeMat[4],sampleTypeMat[3],sampleTypeMat[2],sampleTypeMat[1])])
    bsmt[1] = ax[42].bar(range(len(sampleTypeMat[1])), sampleTypeMat[1], color=sampleTypeCol[1],width=1,edgecolor=sampleTypeCol[1],bottom=[a+b+c for a,b,c in zip(sampleTypeMat[4],sampleTypeMat[3],sampleTypeMat[2])])
    bsmt[2] = ax[42].bar(range(len(sampleTypeMat[2])), sampleTypeMat[2], color=sampleTypeCol[2],width=1,edgecolor=sampleTypeCol[2],bottom=[a+b for a,b in zip(sampleTypeMat[4],sampleTypeMat[3])])
    bsmt[3] = ax[42].bar(range(len(sampleTypeMat[3])), sampleTypeMat[3], color=sampleTypeCol[3],width=1,edgecolor=sampleTypeCol[3],bottom=sampleTypeMat[4])
    bsmt[4] = ax[42].bar(range(len(sampleTypeMat[4])), sampleTypeMat[4], color=sampleTypeCol[4],width=1,edgecolor=sampleTypeCol[4])
    ax[42].set_xlim([0,len(sampleTypeMat[0])])
    ax[42].set_ylim([0,1])
    ax[42].set_xticks([])
    ax[42].yaxis.set_ticks_position('right')
    ax[42].set_xticks([])
    ax[42].get_yaxis().set_tick_params(direction='out')
    ax[42].set_yticks([0,0.2,0.4,0.6,0.8,1])
    ax[42].set_yticklabels(['0%','20%','40%','60%','80%','100%'], fontproperties=font(16))
    # for loc, spine in ax[42].spines.items():
    #     if loc in 'right':
    #         spine.set_position(('outward', 10))  # outward by 10 points
    #         spine.set_smart_bounds(True)


    ### left gene mute rate 
    geneMutRateMat = importGeneRate(geneMutCountPath)
    ax[21].barh(range(len(geneMutRateMat[0])),geneMutRateMat[0], color=colorDic[1],height=0.95,edgecolor='white')
    ax[21].barh(range(len(geneMutRateMat[1])),geneMutRateMat[1], color=colorDic[7],height=0.95,edgecolor='white',left=geneMutRateMat[0])
    ax[21].set_ylim([0,len(geneMutRateMat[0])])
    ax[21].invert_xaxis()
    ax[21].invert_yaxis()
    ax[21].yaxis.set_ticks_position('right')
    ax[21].spines['left'].set_visible(False)
    ax[21].spines['top'].set_visible(False)
    ax[21].spines['right'].set_visible(False)
    ax[21].get_xaxis().set_tick_params(direction='out')
    ax[21].xaxis.set_ticks_position('bottom')
    ax[21].set_xlabel('# SNV / Mb',fontproperties=font(18))
    plt.setp(ax[21].get_yticklines(), visible=False)
    for loc, spine in ax[21].spines.items():
        if loc in 'bottom':
            spine.set_position(('outward', 10))  # outward by 10 points
            spine.set_smart_bounds(True)
    ax[21].set_xticks(range(0,81,20))
    ax[21].set_xticklabels(range(0,81,20),fontproperties=font(16))
    ax[21].set_yticks([n+0.5 for n in range(len(geneMutRateMat[0]))])
    ax[21].set_yticklabels(['%.1f%%'%((a+b)/len(sampleList)*100) for a,b in zip(geneMutRateMat[0],geneMutRateMat[1])],fontproperties=font(16))

    ### right gene fdr 
    fdrMat,fdrtitle = importGeneFDR(geneMutResultPath)
    ax[23].barh(range(len(fdrMat)),fdrMat,color='grey',height=0.95,edgecolor='white')
    ax[23].set_ylim([0,len(fdrMat)])
    ax[23].invert_yaxis()
    ax[23].spines['right'].set_visible(False)
    ax[23].spines['top'].set_visible(False)
    ax[23].spines['left'].set_visible(False)
    ax[23].get_xaxis().set_tick_params(direction='out')
    ax[23].xaxis.set_ticks_position('bottom')
    ax[23].set_xlabel(fdrtitle,fontproperties=font(16))
    plt.setp(ax[23].get_yticklines(), visible=False)
    for loc, spine in ax[23].spines.items():
        if loc in 'bottom':
            spine.set_position(('outward', 10))  # outward by 10 points
            spine.set_smart_bounds(True)
    ax[23].set_yticks([n+0.5 for n in range(len(fdrMat))])
    ax[23].set_yticklabels(geneList,fontproperties=font(16))
    if fdrtitle == 'FDR CT (-log10)':
        ax[23].axvline(2,0,len(fdrMat),color='red')
        ax[23].set_xlim([0,20])
        ax[23].set_xticks(range(0,21,5))
        ax[23].set_xticklabels(range(0,21,5),fontproperties=font(16))
    else:
        ax[23].axvline(1,0,len(fdrMat),color='red')
        ax[23].set_xlim([0,10])
        ax[23].set_xticks(range(0,11,2))
        ax[23].set_xticklabels(range(0,11,2),fontproperties=font(16))


    ### top left legend
    bsnv = {}
    bsnv[0] = ax[11].bar([0],[0],color=colorDic[1],edgecolor=colorDic[1],bottom=[2])
    bsnv[1] = ax[11].bar([0],[0],color=colorDic[7],edgecolor=colorDic[7],bottom=[2])
    ax[11].set_ylim([0,1])
    ax[11].xaxis.set_visible(False)
    ax[11].yaxis.set_visible(False)
    leg0 = ax[11].legend((bsnv[0],bsnv[1]),('Non syn.','Syn.'),\
        handlelength=0.8, framealpha=0)
    legtext = leg0.get_texts()
    for t in legtext:
        t.set_font_properties(font(15))



    ### top right legend
    # colorlist = ['#f0f0f0','#336699','#FF9900','#99CCFF','#996699','#FF6666','#FFFF00','#99CC33','#CCCCCC']
    bheat = {}
    for n in range(1,len(colorlist)):
        bheat[n] = ax[13].bar([0],[0], color=colorlist[n],edgecolor=colorlist[n],bottom=[2])
    ax[13].set_ylim([0,1])

    ax[13].xaxis.set_visible(False)
    ax[13].yaxis.set_visible(False)
    leg1 = ax[13].legend((bheat[1],bheat[2],bheat[3],bheat[4],bheat[5],bheat[6],bheat[7],bheat[8]),\
        ('Missense','Franme shift','In frame InDel','Splice site','Nonstop','Nonsense','Syn.','Other'), \
        ncol=2,handlelength=0.8,framealpha=0)
    legtext = leg1.get_texts()
    for t in legtext:
        t.set_font_properties(font(15))
    



    ### bottom left legend
    # for spine in ['left','right','top','bottom']:
    ax[41].xaxis.set_visible(False)
    ax[41].yaxis.set_visible(False)
    leg2 = ax[41].legend((bsmt[0],bsmt[1],bsmt[2],bsmt[3],bsmt[4]),\
            ('transver','A->G','*Cp(A/C/T)->T','(C/T)p*CpG->T','(A/G)p*CpG->T'),\
            framealpha=0, handlelength=0.8, labelspacing=0.6)
    legtext = leg2.get_texts()
    for t in legtext:
        t.set_font_properties(font(15))
    # leg.get_title().set_font_properties(font(20))

    ### bottom gender legend
    bgen = {}
    for n in range(1,6):
        bgen[n] = ax[4311].bar([0],[0],color=metaCol[n],edgecolor=metaCol[n],bottom=[2])
    ax[4311].set_ylim([0,1])

    ax[4311].xaxis.set_visible(False)
    ax[4311].yaxis.set_visible(False)
    leg3 = ax[4311].legend((bgen[3],bgen[4],bgen[5],bgen[1],bgen[2]),\
        ('Grade2','Grade3','Grade4','Female','Male'),ncol=2,loc=2,handlelength=0.8,framealpha=0)
    legtext = leg1.get_texts()
    for t in legtext:
        t.set_font_properties(font(15))


    fig.savefig(prefix+'.png')
    fig.savefig(prefix+'.pdf')

if __name__ == '__main__':
    main()
