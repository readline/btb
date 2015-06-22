#!/usr/bin/env python
# =============================================================================
# Filename: tcgaRsemScaledEstimate2TpmMatrix.py
# Version: 
# Author: Kai Yu - finno@live.cn
# https://github.com/readline
# Last modified: 2015-06-04 13:42
# Description: 
# 
# =============================================================================
from __future__ import division
import os,sys

def importFileList(listPath):
    tmpdic = {}
    infile = open(listPath, 'r')
    count  = 0
    while 1:
        line = infile.readline()
        if not line: break
        c = line.rstrip().split('\t')
        tmpdic[count] = c
        count += 1
    infile.close()
    return tmpdic

def main():
    try:
        listPath = sys.argv[1]
        prefix   = sys.argv[2]
    except:
        print 'Path list format:'
        print 'sampleID\tsampleTCGARsemPath'
        sys.exit(sys.argv[0] + ' [TCGA rsem result path] [output prefix]')

    listdic = importFileList(listPath)
    geneList, sampleList = [],[]
    matdic = {}

    infile = open(listdic[0][1],'r')
    infile.readline()
    while 1:
        line =infile.readline()
        if not line: break
        geneList.append(line.split('\t')[0])
    infile.close()

    for n in range(len(listdic)):
        sampleID = listdic[n][0]
        samplePath=listdic[n][1]
        sampleList.append(sampleID)
        matdic[sampleID] = []
        infile = open(samplePath, 'r')
        infile.readline()
        while 1:
            line = infile.readline()
            if not line: break
            matdic[sampleID].append(float(line.rstrip().split('\t')[2]))
        infile.close()

    savefile = open(prefix + '.TPM.matrix','w')
    savefile.write('gene_id')
    for sampleID in sampleList:
        savefile.write('\t' + sampleID)
    savefile.write('\n')
    for n in range(len(geneList)):
        savefile.write(geneList[n])
        savefile.write('\t' + '\t'.join(['%.4f'%(matdic[x][n]*1000000) for x in sampleList]) + '\n')
    savefile.close()

if __name__ == '__main__':
    main()
