#!/usr/bin/env python
# pattern10baseByFlank10.py
# 150413
# Kai Yu
# https://github.com/readline
################################################
# Use the flank10 file produced by maf2MutSignature.py
# generate 6 types' mutation pattern with up/down stream 10bases
# ./pattern10baseByFlank10.py [flank 10 path] [output prefix]
from __future__ import division
import os,sys,gzip

def revCom(seq):
    tmpseq = ''
    comDic = {'A':'T', 'T':'A', 'G':'C', 'C':'G'}
    for n in range(len(seq)-1, -1, -1):
        tmpseq += comDic[seq[n].upper()]
    return tmpseq

def importFlank10(flankPath):
    ctmpDic = {'A':[], 'T':[], 'C':[], 'G':[]}
    ttmpDic = {'A':[], 'T':[], 'C':[], 'G':[]}

    if flankPath[-3:] == '.gz':
        infile = gzip.open(flankPath,'rb')
    else:
        infile = open(flankPath,'r')
    infile.readline()
    while 1:
        line = infile.readline()
        if not line: break
        c = line.rstrip().split('\t')
        seq0 = ''.join(c[3:])
        if c[13] not in 'CT':
            ref = revCom(seq0)
            alt = revCom(c[2])
        else:
            ref = seq0
            alt = c[2]
        if ref[10] == 'T':
            ttmpDic[alt].append(ref)
        elif ref[10] == 'C':
            ctmpDic[alt].append(ref)
    infile.close()
    return ttmpDic, ctmpDic

# def calcRatio(basedic,base):
#     total = 0
#     for n in basedic:
#         total += basedic[n]
#     return basedic[base] / total

def calcSeq(seqlist):
    tmpDic = {}
    for n in range(len(seqlist[0])):
        tmpDic[n] = {'A':0, 'T':0, 'C':0, 'G':0}
    for seq in seqlist:
        for n in range(len(seq)):
            tmpDic[n][seq[n]] += 1
    return tmpDic

def main():
    try:
        flankPath = sys.argv[1]
        prefix    = sys.argv[2]
    except:
        print sys.argv[0] + ' [flank 10 path] [output prefix]'
        sys.exit()
    tDic, cDic = importFlank10(flankPath)

    for b in 'ACG':
        savefile = open('%s.T%s10'%(prefix,b),'w')
        result = calcSeq(tDic[b])
        for base in 'TGCA':
            savefile.write(base)
            for n in range(len(result)):
                savefile.write('\t%f'%result[n][base])
            savefile.write('\n')
        savefile.close()

    for b in 'ATG':
        savefile = open('%s.C%s10'%(prefix,b),'w')
        result = calcSeq(cDic[b])
        for base in 'TGCA':
            savefile.write(base)
            for n in range(len(result)):
                savefile.write('\t%d'%result[n][base])
            savefile.write('\n')
        savefile.close()

if __name__ == '__main__':
    main()










