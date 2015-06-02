#!/usr/bin/env python
# =============================================================================
# Filename: tcgaMaf37to19.py
# Version: 
# Author: Kai Yu - finno@live.cn
# https://github.com/readline
# Last modified: 2015-06-02 16:03
# Description: 
# 
# =============================================================================
import os,sys
def main():
    try:
        inpath = sys.argv[1]
        outpath= sys.argv[2]
    except:
        sys.exit(sys.argv[0] + ' [input maf] [output maf]')

    infile = open(inpath, 'r')
    savefile=open(outpath,'w')
    header = infile.readline().rstrip().split('\t')
    tmp = []
    for item in header:
        if item.upper() == 'NCBI_BUILD':
            tmp.append('NCBI_Build')
        elif item.upper()=='CHROM' or item.upper()=='CHROMOSOME':
            tmp.append('Chromosome')
        else:
            tmp.append(item)
    savefile.write('\t'.join(tmp) + '\n')

    while 1:
        line = infile.readline()
        if not line:
            break
        tmp = []
        c = line.rstrip().split('\t')
        tmp += c[:3]
        if c[3] == '37':
            tmp.append('hg19')
        else:
            print "Invalid build %s" %c[3]
        tmp.append('chr%s'%c[4])
        tmp += c[5:]
        savefile.write('\t'.join(tmp) + '\n')
    savefile.close()
    infile.close()

if __name__ == '__main__':
    main()
