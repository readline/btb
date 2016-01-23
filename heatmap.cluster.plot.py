#!/usr/bin/env python
# =============================================================================
# Filename: heatmap.cluster.plot.py
# Version: 
# Author: Kai Yu - finno@live.cn
# https://github.com/readline
# Last modified: 2015-07-31 00:51
# Description: 
# 
# =============================================================================
import os,sys
import scipy,numpy,math
from scipy import stats
from scipy.spatial.distance import pdist
from scipy.cluster.hierarchy import linkage, dendrogram
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def font(size):
    return matplotlib.font_manager.FontProperties(size=size,fname='/delldata/Analysis/yukai/src/font/ARIAL.TTF')

class LoadMatrix():
    '''In:\n\tMatrix path.\nOut:\n\tself.matrix\n\tself.rownames\n\tself.colnames'''
    def __init__(self, matrixPath):
        infile = open(matrixPath, 'r')
        rownames=[]
        colnames = infile.readline().rstrip().split('\t')[1:]
        mat = []
        while 1:
            line = infile.readline()
            if not line:
                break
            c = line.rstrip().split('\t')
            rownames.append(c[0])
            mat.append([math.log(float(n)+1,2) for n in c[1:]])
        infile.close()
        matrix = numpy.array(mat)
        self.matrix = matrix
        self.rownames=rownames
        self.colnames=colnames
        self.filename=matrixPath.split('/')[-1]
    @property
    def matrix(self):
        return self.matrix
    @property
    def rownames(self):
        return self.rownames
    @property
    def colnames(self):
        return self.colnames
    @property
    def filename(self):
        return self.filename

def matrixMax(matrix):
    maxvalue = -1000000
    for n in matrix:
        if max(n) >= maxvalue:
            maxvalue = max(n)
    if maxvalue != int(maxvalue):
        maxvalue = int(maxvalue) + 1
    return maxvalue

def matrixMin(matrix):
    minvalue = 1000000
    for n in matrix:
        if min(n) <= minvalue:
            minvalue = min(n)
    if minvalue != int(minvalue):
        minvalue = int(minvalue) - 1
    return minvalue

def clusterPlot(matrix, prefix):
    m = matrix.matrix
    print 'Matrix loaded.'

    # cluster
    print 'Calculating row linkage'
    lnk_r = linkage(pdist(m,   'euclidean'), method = 'complete')
    print 'Calculating col linkage'
    lnk_c = linkage(pdist(m.T, 'euclidean'), method = 'complete')
    
    dendro_r = dendrogram(lnk_r, orientation='left')
    dendro_c = dendrogram(lnk_c, orientation='top')

    idx_r = dendro_r['leaves']
    idx_c = dendro_c['leaves']
    #idx_c = [1, 2, 0, 4, 7, 8, 9, 6, 3, 5]

    sorted_rowname = [matrix.rownames[n] for n in idx_r]
    sorted_colname = [matrix.colnames[n] for n in idx_c]

    m1 = m[:, idx_c]
    m2 = m1[idx_r,:]
    m3 = stats.zscore(m2, axis=1)

    # plot
    fig = plt.figure(figsize=(16,20),dpi=300)
    ## heatmap
    print matrixMin(m3), matrixMax(m3)
    #norm = matplotlib.colors.Normalize(vmin=matrixMin(m3)*0.5, vmax=matrixMax(m3)*0.5)
    norm = matplotlib.colors.Normalize(vmin=-2.5, vmax=2.5)
    ax_heat = fig.add_axes([0.2,0.13,0.6,0.7], frame_on=True)
    ax_heat_cb = fig.add_axes([0.035,0.865,0.125,0.06], frame_on=True)

    ## dendro
    #ax_den_top = fig.add_axes([0.2,0.855, 0.6,0.1], frame_on=False)
    #ax_den_left= fig.add_axes([0.035,0.13,0.125,0.7], frame_on=False)
    ax_den_top = fig.add_axes([0.2,0.84, 0.6,0.1], frame_on=False)
    ax_den_left= fig.add_axes([0.035,0.13,0.15,0.7], frame_on=False)
    heatmap = ax_heat.imshow(m3, aspect='auto', origin='lower', norm=norm, interpolation='nearest', cmap=plt.cm.bwr)
    ## colorbar
    heatmap_cb = matplotlib.colorbar.Colorbar(ax_heat_cb, heatmap, ticklocation='bottom', orientation='horizontal')

    den_left = dendrogram(lnk_r, ax=ax_den_left, orientation='right', color_threshold=3, above_threshold_color='black', no_labels=True)
    den_top =  dendrogram(lnk_c, ax=ax_den_top,  orientation='top', color_threshold=0, above_threshold_color='black', no_labels=True)
    
    ax_den_top.set_yticks([])
    ax_den_left.set_xticks([])

    

    modified_colname = ['Muscle', 'Notochord', 'Gut', 'Hepatic caecum', 'Branchial arch',\
                        'Nerve chord 1-7', 'Nerve chord 7+', 'Skin', 'Wheel organ', 'Endostyle']
    ax_heat.set_yticks([])
    ax_heat.set_xticks([n+0.1  for n in range(len(sorted_colname))])
    ax_heat.set_xticklabels(sorted_colname, fontproperties=font(20), rotation=45, horizontalalignment='right')
    ax_heat.tick_params(axis='both', length=0)
    ax_heat.yaxis.set_ticks_position('right')
    ax_heat.set_yticks(range(len(sorted_rowname)))
    ax_heat.set_yticklabels(sorted_rowname, fontproperties=font(16))


    heatmap_cb.set_ticks([-2, 0, 2])
    heatmap_cb.set_ticklabels([-2, 0, 2])
    ax_heat_cb.set_title('Z-score', fontproperties=font(22))
    for tmp in heatmap_cb.ax.get_xticklabels():
        tmp.set_fontproperties(font(20))
    ax_heat_cb.tick_params(axis='y')

    fig.suptitle('Log2 centered heatmap of %s'%matrix.filename, fontproperties = font(24))

    fig.savefig(prefix+'.pdf')
    fig.savefig(prefix+'.svg')
    fig.savefig(prefix+'.png')
    
    savefile = open(prefix + '.log2.clustered.matrix','w')
    savefile.write('Item\t' + '\t'.join(sorted_colname) + '\n')
    for n in range(len(sorted_rowname)):
        savefile.write(sorted_rowname[n] + '\t' + '\t'.join([str(i) for i in m2[n]]) + '\n')
    savefile.close()

    savefile = open(prefix + '.log2.clustered.zscore.matrix','w')
    savefile.write('Item\t' + '\t'.join(sorted_colname) + '\n')
    for n in range(len(sorted_rowname)):
        savefile.write(sorted_rowname[n] + '\t' + '\t'.join([str(i) for i in m3[n]]) + '\n')
    savefile.close()


def main():
    try:
        matrixPath = sys.argv[1]
        outprefix  = sys.argv[2]
    except:
        sys.exit(sys.argv[0] + ' [matrix path] [output prefix]')

    mat = LoadMatrix(matrixPath)

    clusterPlot(mat, outprefix)


if __name__ == '__main__':
    main()
