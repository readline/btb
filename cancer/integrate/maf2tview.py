#!/usr/bin/env python
# maf2tview.py
# version 1.0
# Kai Yu
# github.com/readline
# 150421
##############################################
import os, sys

def importMaf(mafPath):
    tmpdic = {}
    infile = open(mafPath,'r')
    infile.readline()
    count = 0
    while 1:
        line = infile.readline()
        if not line: break
        c = line.rstrip().split('\t')
        gene = c[0]
        chrid = c[4]
        start = int(c[5])
        end = int(c[6])
        sample = c[15]
        control = c[16]
        tmpdic[count] = [gene,chrid,start,end,sample,control,line.rstrip()]
        count += 1
    infile.close()
    return tmpdic


def main():
    try:
        mafPath = sys.argv[1]
        outPath = sys.argv[2]
        tumorbam = sys.argv[3]
        normbam = sys.argv[4]
        reffa = sys.argv[5]
    except:
        sys.exit(sys.argv[0] + ' [maf path] [out path] [tumor bam] [normal bam] [ref fasta]')
    
    mafdic = importMaf(mafPath)

    try:
        os.mkdir(outPath)
    except:
        pass

    htmlfile = open('%s.html' %(outPath),'w')
    for n in range(len(mafdic)):
        c = mafdic[n]
        savepath = '%s/%s[%s][%s:%d].tview' %(outPath, c[4], c[0], c[1], c[2])
        savefile = open(savepath,'w')
        savefile.write('# %s\n################################################\n' %c[6])
        tview = os.popen('samtools tview -d T -p %s:%d %s %s' %(c[1],c[2]-40,tumorbam,reffa))
        # print 'samtools tview -d T -p %s:%d-%d %s %s' %(c[1],c[2]-80,c[3]+80,tumorbam,reffa)
        savefile.write(tview.read())
        savefile.write('\n################################################\n')
        tview = os.popen('samtools tview -d T -p %s:%d %s %s' %(c[1],c[2]-40,normbam,reffa))
        # print 'samtools tview -d T -p %s:%d-%d %s %s' %(c[1],c[2]-80,c[3]+80,normbam,reffa)
        savefile.write(tview.read())
        savefile.close()

        htmlfile.write("%s\n<hr>\nTumor\n" %c[-1].rstrip())
        tview = os.popen('samtools tview -d H -p %s:%d %s %s'\
         %(c[1],c[2]-40,tumorbam, reffa))
        htmlfile.write(tview.read()+'\n<hr>\nControl\n<br>\n')
        tview = os.popen('samtools tview -d H -p %s:%d %s %s'\
         %(c[1],c[2]-40,normbam, reffa))
        htmlfile.write(tview.read()+'\n<br>\n<hr>\n<hr>\n<hr>\n<br>\n')
    htmlfile.close()
if __name__ == '__main__':
    main()

