#!/usr/bin/env python
from __future__ import division
import os, sys, gzip
import Fasta

def importBed(bedPath):
    bedDic = {}
    targetDic = {}
    count = 0
    for n in range(1,23):
        bedDic['chr%d'%n] = {}
        targetDic['chr%d'%n] = {}
    for n in 'XY':
        bedDic['chr%s'%n] = {}
        targetDic['chr%s'%n] = {}
    infile = open(bedPath,'r')
    while 1:
        line = infile.readline()
        if not line: break
        count += 1
        c = line.rstrip().split('\t')
        for n in range(int(c[1]), int(c[2])):
            bedDic[c[0]][n] = [0,0]
        targetDic[c[0]][count] = [int(c[1]),int(c[2])]
    infile.close()
    return bedDic, targetDic

def importBlood(bedDic, bloodBamPath):
    infile = os.popen('samtools depth %s' %bloodBamPath)
    count = 0
    while 1:
        line = infile.readline().rstrip()
        if not line: break
        count += 1
        if count % 1000000 == 0:
            print 'Reached line %d.' %count
        c = line.split('\t')
        if c[0] not in bedDic:
            continue
        if int(c[1])-1 not in bedDic[c[0]]:
            continue
        bedDic[c[0]][int(c[1])-1][0] = int(c[2])
    infile.close()
    return bedDic

def importTumor(bedDic, tumorBamPath):
    infile = os.popen('samtools depth %s' %tumorBamPath)
    count = 0
    while 1:
        line = infile.readline().rstrip()
        if not line: break
        count += 1
        if count % 1000000 == 0:
            print 'Reached line %d.' %count
        c = line.split('\t')
        if c[0] not in bedDic:
            continue
        if int(c[1])-1 not in bedDic[c[0]]:
            continue
        bedDic[c[0]][int(c[1])-1][1] = int(c[2])
    infile.close()
    return bedDic

def calcCov(bedDic, targetDic, b_cut = 8, t_cut = 14):
    tmpdic = {}
    for chrid in targetDic:
        print chrid
        tmpdic[chrid] = {}
        for item in targetDic[chrid]:
            itemlen = targetDic[chrid][item][1] - targetDic[chrid][item][0]
            passlen = 0
            for pos in range(targetDic[chrid][item][0], targetDic[chrid][item][1]):
                covlist = bedDic[chrid][pos]
                if covlist[0] >= b_cut and covlist[1] >= t_cut:
                    passlen += 1
            tmpdic[chrid][item] = passlen / itemlen
    return tmpdic

def calcGC(targetDic, faPath):
    tmpdic = {}
    fa = Fasta.Parse(faPath)
    for chrid in targetDic:
        print chrid
        tmpdic[chrid] = {}
        for item in targetDic[chrid]:
            seq = fa.seq[chrid][targetDic[chrid][item][0]:targetDic[chrid][item][1]].upper()
            gc = (seq.count('G') + seq.count('C') ) / len(seq)
            tmpdic[chrid][item] = gc
    return tmpdic

def outputResult(targetDic, covDic, gcDic, prefix):
    savefile = open(prefix+'.exonStat','w')
    savefile.write('#chr\tstart\tend\tGC\tCov\n')
    for n in range(1,23) + ['X','Y']:
        chrid = 'chr'+str(n)
        print chrid
        for item in sorted(targetDic[chrid]):
            rate = covDic[chrid][item]
            gc   = gcDic[chrid][item]
            region = targetDic[chrid][item]
            savefile.write('%s\t%d\t%d\t%f\t%f\n' \
                %(chrid, region[0],region[1],gc,rate))
    savefile.close()

def main():
    try:
        faPath = sys.argv[1]
        bedPath= sys.argv[2]
        bloodBamPath = sys.argv[3]
        tumorBamPath = sys.argv[4]
        prefix = sys.argv[5]
    except:
        print sys.argv[0] + ' [ref fasta path] [bed path] [blood bam path] [tumor bam path] [output prefix]'
        sys.exit()

    print 'Import bed file.'
    bedDic, targetDic = importBed(bedPath)
    print 'Import blood bam.'
    bedDic = importBlood(bedDic, bloodBamPath)
    print 'Import tumor bam.'
    bedDic = importTumor(bedDic, tumorBamPath)
    print 'Calculate coverage.'
    covDic = calcCov(bedDic, targetDic)
    print 'Calculate GC content.'
    gcDic = calcGC(targetDic, faPath)
    print 'Output result.'
    outputResult(targetDic, covDic, gcDic, prefix)

if __name__ == '__main__':
    main()

