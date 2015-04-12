#!/usr/bin/env python
# pattern10baseRef.py
# 150413
# Kai Yu
# https://github.com/readline
################################################
# Calculate the mutation pattern with both 10 base up/down stream of reference.
# ./pattern10baseRef.py [ref fasta path] [ref bed path] [output prefix]
from __future__ import division
import os, sys, gzip
import Fasta

def revCom(seq):
    tmpseq = ''
    comDic = {'A':'T', 'T':'A', 'G':'C', 'C':'G'}
    for n in range(len(seq)-1, -1, -1):
        tmpseq += comDic[seq[n].upper()]
    return tmpseq

def importBed(bedPath):
    targetDic = {}
    count = 0
    infile = open(bedPath,'r')
    while 1:
        line = infile.readline()
        if not line: break
        count += 1
        c = line.rstrip().split('\t')
        targetDic[count] = [c[0], int(c[1]), int(c[2])]
    infile.close()
    return targetDic

def calcRatio(basedic,base):
    total = 0
    for n in basedic:
        total += basedic[n]
    return basedic[base] / total

def main():
    try:
        reffaPath = sys.argv[1]
        refbedPath= sys.argv[2]
        prefix    = sys.argv[3]
    except:
        print sys.argv[0] + ' [ref fasta path] [ref bed path] [output prefix]'
        sys.exit()

    print 'Import fasta file.'
    fa = Fasta.Parse(reffaPath)
    print 'Import bed file.'
    bedDic = importBed(refbedPath)

    tdic, cdic = {}, {}
    for n in range(1,11):
        tdic[n] = {'A':0, 'T':0, 'C':0, 'G':0}
        cdic[n] = {'A':0, 'T':0, 'C':0, 'G':0}
        tdic[-n] = {'A':0, 'T':0, 'C':0, 'G':0}
        cdic[-n] = {'A':0, 'T':0, 'C':0, 'G':0}

    print 'Calculate bases.'
    for item in bedDic:
        seq = fa.seq[bedDic[item][0]][bedDic[item][1]:bedDic[item][2]].upper()
        seqlen = len(seq)
        for pos in range(seqlen-21):
            k0 = seq[pos:pos+21]
            if k0[10] in 'CT':
                k = k0
            else:
                k = revCom(k0)
            for n in range(-10,11):
                if n == 0: continue
                if k[10] == 'T':
                    tdic[n][k[n+10]] += 1
                elif k[10] == 'C':
                    cdic[n][k[n+10]] += 1

    print 'Write outputs.'
    savefile = open(prefix+'.C10','w')
    for b in 'TGCA':
        savefile.write(b)
        for n in range(-10,11):
            if n == 0:
                if b == 'C':
                    savefile.write('\t1')
                else:
                    savefile.write('\t0')
            else:
                savefile.write('\t%f'%(calcRatio(cdic[n], b)))
        savefile.write('\n')
    savefile.close()

    savefile = open(prefix+'.T10','w')
    for b in 'TGCA':
        savefile.write(b)
        for n in range(-10,11):
            if n == 0:
                if b == 'T':
                    savefile.write('\t1')
                else:
                    savefile.write('\t0')
            else:
                savefile.write('\t%f'%(calcRatio(tdic[n], b)))
        savefile.write('\n')
    savefile.close()

if __name__ == '__main__':
    main()


