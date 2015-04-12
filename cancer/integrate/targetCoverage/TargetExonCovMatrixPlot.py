#!/usr/bin/env python
# TargetExonCovMatrixPlot.py 
# 150412
# Kai Yu
# github.com/readline
##############################################
# Take in the TargetExonCovMatrixSorting.R output sorted matrix and generate a heatmap with GC plot.
# ./TargetExonCovMatrixPlot.py [sorted matrix path]

from __future__ import division
import matplotlib
matplotlib.use('Agg')
import os,sys,matplotlib,pylab
import matplotlib.pyplot as plt

def font(size):
    return matplotlib.font_manager.FontProperties(size=size,fname='/Share/BP/yukai/src/font/ARIAL.TTF')

def fontConsola(size):
    return matplotlib.font_manager.FontProperties(size=size,fname='/Share/BP/yukai/src/font/consola.ttf')

matPath = sys.argv[1]
matFile = open(matPath,'r')
samplelist0 = matFile.readline().rstrip().split('\t')
samplelist = [n[1:] for n in samplelist0]
row = 0
matrix = []
gclist = []
while 1:
    line = matFile.readline().rstrip()
    if not line:break
    row += 1
    column0 = line.split('\t')[1:]
    column = []
    for c in column0[:-1]:
        column.append(float(c))
    gclist.append(float(column0[-1]))
    matrix.append(column)

fig = plt.figure(figsize = (20,20))
ax1 = fig.add_axes([0.115,0.1,0.8,0.8])
ax2 = fig.add_axes([0.93,0.1, 0.025, 0.8])
norm = matplotlib.colors.Normalize(vmin=0,vmax=1)
ax1.set_xticks([x+0.3 for x in range(0,len(samplelist))])
ax1.set_xticklabels(samplelist[:-1],rotation = 'vertical',fontproperties=font(10))
ax1.set_yticks([])
plt.setp(ax1.get_xticklines(), visible=False)

colormap=matplotlib.cm.hot
im = ax1.imshow(matrix, cmap = colormap, norm=norm, interpolation='nearest',aspect='auto')
ax1.set_title('Target Coverage distribution',fontproperties=font(32))

cb = matplotlib.colorbar.ColorbarBase(ax2, cmap=colormap,norm=norm,ticks=[0,0.2,0.4,0.6,0.8,1])
for t in cb.ax.get_yticklabels():
    t.set_fontproperties(font(20))
cb.set_label("Percentage of covered bases in each target",fontproperties=font(28))

ax3 = fig.add_axes([0.05, 0.1, 0.05, 0.8])
ax3.plot(gclist,range(0,len(gclist)),'b.',markersize=0.3,alpha=0.7)

ax3.set_xlim([0,1])
ax3.set_ylim([0,len(gclist)])
ax3.axvline(0.5,0,len(gclist),linestyle='--',linewidth=2,color='black')
ax3.set_xticks([0,0.5,1])
ax3.set_xticklabels([0,0.5,1],fontproperties=font(20))
ax3.invert_xaxis()
ax3.invert_yaxis()
ax3.xaxis.set_label_position("top")
ax3.yaxis.set_label_position("right")
ax3.axes.get_yaxis().set_visible(False)
ax3.set_xlabel('GC%',fontproperties=font(20))

plt.savefig(matPath+'.png')
plt.savefig(matPath+'.pdf')
