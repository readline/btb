#!/usr/bin/env python
# tripplemut2Spectra.py
# 150412
# Kai Yu
# https://github.com/readline
# Import the trimut file produced by maf2MutSignature.py and calculate the spectra info.
# ./tripplemut2Spectra.py [tripple mut path] [output prefix]

from __future__ import division
import os,sys,gzip

def revCom(seq):
    tmpseq = ''
    comDic = {'A':'T', 'T':'A', 'G':'C', 'C':'G'}
    for n in range(len(seq)-1, -1, -1):
        tmpseq += comDic[seq[n].upper()]
    return tmpseq

def importTrimut(trimutPath):
    '''Import the trimut file produced by maf2MutSignature.py and calculate the spectra info.
    importTrimut(trimutPath)
    return dic {'m1':,...,'m2':}
    '''
    # m1:   transver
    # m2:   A -> G
    # m3:   *Cp(A/C/T)->T
    # m4:   (C/T)p*CpG->T
    # m5:   (A/G)p*CpG->T
    if trimutPath[-3:] == '.gz':
        infile = gzip.open(trimutPath, 'rb')
    else:
        infile = open(trimutPath, 'r')
    
    infile.readline()
    tmpdic = {'m1':0, 'm2':0, 'm3':0, 'm4':0, 'm5':0,}

    while 1:
        line = infile.readline()
        if not line:
            break
        c = line.rstrip().split('\t')
        seq0 = ''.join(c[3:6])
        if seq0[1] in 'TG':
            seq = revCom(seq0)
            alt = revCom(c[2])
        else:
            seq = seq0
            alt = c[2]

        if seq[1] == 'A':
            if alt == 'G':
                tmpdic['m2'] += 1
            else:
                tmpdic['m1'] += 1
        elif seq[1] == 'C':
            if seq[2] in 'ACT' and alt == 'T':
                tmpdic['m3'] += 1
            elif seq[0] in 'CT' and seq[2] == 'G' and alt == 'T':
                tmpdic['m4'] += 1
            elif seq[0] in 'AG' and seq[2] == 'G' and alt == 'T':
                tmpdic['m5'] += 1
            else:
                tmpdic['m1'] += 1

    infile.close()
    return tmpdic

def main():
    try:
        trimutPath = sys.argv[1]
        prefix = sys.argv[2]
    except:
        print sys.argv[0] + ' [tripple mut path] [output prefix]'
        sys.exit()

    spectra = importTrimut(trimutPath)
    infodic = {'m1':'transver','m2':'A->G','m3':'*Cp(A/C/T)->T',\
    'm4':'(C/T)p*CpG->T','m5':'(A/G)p*CpG->T'}
    savefile = open(prefix+'.mutTypes','w')
    total = 0
    for n in spectra:
        total += spectra[n]
    for n in ['m1','m2','m3','m4','m5']:
        savefile.write('%s\t%d\t%f\n' %(infodic[n],spectra[n],spectra[n]/total))
    savefile.close()

if __name__ == '__main__':
    main()