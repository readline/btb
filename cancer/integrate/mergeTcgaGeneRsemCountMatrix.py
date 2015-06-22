#!/usr/bin/env python
# =============================================================================
# Filename: mergeTcgaGeneRsemCountMatrix.py
# Version: 
# Author: Kai Yu - finno@live.cn
# https://github.com/readline
# Last modified: 2015-06-02 20:42
# Description: 
# 
# =============================================================================
import os,sys

def importSdrf(meta_sdrf):
    tmpdic = {}
    infile = open(meta_sdrf, 'r')
    infile.readline()
    while 1:
        line = infile.readline()
        if not line:
            break
        c = line.split('\t')
        tmpdic[c[0]] = c[1]
    infile.close()
    return tmpdic

def main():
    try:
        dataDir = sys.argv[1]
        meta_sdrf = sys.argv[2]
        prefix  = sys.argv[3]
    except:
        sys.exit(sys.argv[0] + ' [TCGA data dir] [meta_sdrf] [output prefix]')

    tmp = os.popen('ls %s/*.rsem.genes.results' %dataDir)
    filelist = []
    while 1:
        line = tmp.readline()
        if not line: break
        filelist.append(line.rstrip())

    sdrfdic = importSdrf(meta_sdrf)

    matdic = {}
    samplelist = []
    genelist = []
    for path in filelist:
        uuid = path.split('/')[-1].split('.')[2]
        sid  = sdrfdic[uuid]
        matdic[sid] = []
        samplelist.append(sid)
        print uuid, sid

        infile = open(path, 'r')
        infile.readline()

        while 1:
            line = infile.readline()
            if not line: break
            c = line.split('\t')
            matdic[sid].append(c[1])
            if len(samplelist) == 1:
                genelist.append(c[0])
        infile.close()

    savefile = open(prefix+'.rsem.count.matrix', 'w')
    savefile.write('gene_id')
    for sample in samplelist:
        savefile.write('\t'+sample)
    savefile.write('\n')
    for n in range(len(genelist)):
        savefile.write(genelist[n])
        for sample in samplelist:
            savefile.write('\t'+matdic[sample][n])
        savefile.write('\n')
    savefile.close()

if __name__ == '__main__':
    main()
