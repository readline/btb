#!/usr/bin/env python
# maf2SNVneighbour.py
# 150409
# Kai Yu
# github.com/readline

from __future__ import division
import os,sys,gzip
from Bio import SeqIO

def importFasta(fastaPath):
    if fastaPath[-3:] == '.gz':
        import gzip
        infile = gzip.open(fastaPath,'rb')
    else:
        infile = open(fastaPath,'r')
    tmpdic = {}
    for seq_record in SeqIO.parse(infile,'fasta'):
        chrid = seq_record.id
        seq = str(seq_record.seq)
        tmpdic[chrid] = seq
    infile.close()
    return tmpdic

def importBedK3(bedk3Path):
    infile = open(bedk3Path,'r')
    tmpdic = {}
    total = 0
    while 1:
        line = infile.readline().rstrip()
        if not line: break
        c = line.split('\t')
        if c[0][1] in 'CT':
            seq = c[0]
            if seq not in tmpdic:
                tmpdic[seq] = 0
            tmpdic[seq] += int(c[1])
        else:
            seq = revCom(c[0])
            if seq not in tmpdic:
                tmpdic[seq] = 0
            tmpdic[seq] += int(c[1])
        total += int(c[1])
    infile.close()
    # print tmpdic
    freqdic = {}
    for seq in tmpdic:
        freqdic[seq] = tmpdic[seq] / total
        # print seq, freqdic[seq]
    return freqdic

def getBases(fadic, chrid, mafpos):
    base_l = fadic[chrid][mafpos-2].upper()
    base_m = fadic[chrid][mafpos-1].upper()
    base_r = fadic[chrid][mafpos].upper()
    return base_l+base_m+base_r

def revCom(seq):
    tmpseq = ''
    comDic = {'A':'T', 'T':'A', 'G':'C', 'C':'G'}
    for n in range(len(seq)-1, -1, -1):
        tmpseq += comDic[seq[n].upper()]
    return tmpseq

def makeTrippleDic():
    triList, triDic = [],{}
    for t_alt in 'ACG':
        for a in 'ACGT':
            for c in 'ACGT':
                ref = a+'T'+c
                triList.append(ref+t_alt)
                if ref not in triDic:
                    triDic[ref] = {}
                triDic[ref][t_alt] = 0
    for c_alt in 'AGT':
        for a in 'ACGT':
            for c in 'ACGT':
                ref = a+'C'+c
                triList.append(ref+c_alt)
                if ref not in triDic:
                    triDic[ref] = {}
                triDic[ref][t_alt] = 0
    return triList, triDic

def maf2flank(mafPath, fadic, prefix):
    patientdic = {}
    count = 0
    infile = open(mafPath,'r')
    infile.readline()
    save3 = gzip.open(prefix+'.tripplemut.gz','wb')
    save10= gzip.open(prefix+'.flank10.gz','wb')
    save3.write('#chrid\tpos\talt\t-1\t0\t1\n')
    save10.write('#chrid\tpos\talt')
    for n in range(-10,11):
        save10.write('\t%d' %(n))
    save10.write('\n')
    while 1:
        line = infile.readline()
        if not line: break
        c = line.rstrip().split('\t')
        if c[9] != 'SNP': continue
        patientdic[c[15]] = 1
        count += 1
        chrid, pos, ref, alt = c[4], int(c[5]), c[10], c[12]
        save3.write('%s\t%d\t%s\t%s\n'%(chrid,pos,alt,'\t'.join(list(fadic[chrid][pos-2:pos+1].upper()))))
        save10.write('%s\t%d\t%s\t%s\n'%(chrid,pos,alt,'\t'.join(list(fadic[chrid][pos-11:pos+11].upper()))))
    save3.close()
    save10.close()
    return len(patientdic), count

def statTripple(prefix):
    infile = gzip.open(prefix+'.tripplemut.gz','rb')
    infile.readline()
    tmpdic = {}
    for a in 'AGCT':
        for b in 'TC':
            for c in 'AGCT':
                tmpdic[a+b+c] = {'A':0,'T':0,'C':0,'G':0}
    while 1:
        line = infile.readline()
        if not line: break
        c = line.rstrip().split('\t')
        ref0 = ''.join(c[3:])
        if ref0[1] in 'CT':
            ref = ref0
            altb= c[2]
        else:
            ref = revCom(ref0)
            altb= revCom(c[2])
        tmpdic[ref][altb] += 1
    infile.close()
    return tmpdic

def main():
    try:
        mafPath = sys.argv[1]
        faPath  = sys.argv[2]
        bedk3Path = sys.argv[3]
        prefix  = sys.argv[4]
    except:
        print sys.argv[0] + ' [maf path] [ref fasta path] [bed K3 path] [output prefix]'
        sys.exit()
    fadic = importFasta(faPath)
    print 'Reference fasta file %s imported.' %faPath
    patient, countn = maf2flank(mafPath,fadic,prefix)
    beddic = importBedK3(bedk3Path)
    tridic = statTripple(prefix)
    size = 51.189318
    savefile = open(prefix+'.signature','w')
    savefile.write('#n=%d\n' %(countn))
    for b_alt in 'ACG':
        for a in 'ACGT':
            for c in 'ACGT':
                ref = a+'T'+c
                alt = a+b_alt+c
                rawcount = tridic[ref][b_alt]
                savefile.write('%s>%s\t%f\n' %(ref,alt,rawcount/patient/size/beddic[ref]))
    for b_alt in 'AGT':
        for a in 'ACGT':
            for c in 'ACGT':
                ref = a+'C'+c
                alt = a+b_alt+c
                rawcount = tridic[ref][b_alt]
                savefile.write('%s>%s\t%f\n' %(ref,alt,rawcount/patient/size/beddic[ref]))
    savefile.close()

if __name__ == '__main__':
    main()

