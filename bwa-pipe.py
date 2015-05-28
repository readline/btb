#!/usr/bin/env python
# =============================================================================
# Filename: bwa-pipe.py
# Version: 
# Author: Kai Yu - finno@live.cn
# https://github.com/readline
# Last modified: 2015-05-28 21:18
# Description: 
# 
# =============================================================================
import os, sys
import time
import commands
from optparse import OptionParser

def now():
    return time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))

def cmdExec(cmd):
    print '[%s] Exec cmd: %s' %(now(), cmd)
    cmdResult = commands.getstatusoutput(cmd)
    if cmdResult[0] == 0:
        print '[%s] Finished cmd: %s' %(now(), cmd)
        return cmdResult[1]
    else:
        print '[%s] Warning! Failed cmd: %s' %(now(), cmd)
        print cmdResult[1]
        sys.exit()

def pe_run(options, bins):
    if options.option == '':
        option = '-e 50 -i 15 -q 10'
    else:
        option = options.option

    cmd1 = '%s aln -t %d %s %s %s >%s.sai1' \
            %(bins['bwa'], options.threads, option, options.ref, options.file1, options.prefix)
            
    cmd2 = '%s aln -t %d %s %s %s >%s.sai2' \
            %(bins['bwa'], options.threads, option, options.ref, options.file2, options.prefix)

    if options.rg == '':
        sample = options.prefix.split('/')[-1]
        rg = "@RG\tID:%s\tLB:%s\tPL:ILLUMINA\tSM:%s" %(sample, sample, sample) 
    else:
        rg = options.rg
    cmd3 = '%s sampe -r "%s" %s %s.sai1 %s.sai2 %s %s > %s.sam' \
            %(bins['bwa'], rg, options.ref, options.prefix, options.prefix, options.file1, options.file2, options.prefix)

    cmd4 = '%s view -bS %s.sam -o %s.bam' %(bins['sam'], options.prefix, options.prefix) 
    
    cmd5 = 'java -Xmx4g -jar %s INPUT=%s.bam OUTPUT=%s.sort.bam SORT_ORDER=coordinate VALIDATION_STRINGENCY=LENIENT' \
            %(bins['sortsam'], options.prefix, options.prefix)

    cmd6 = '%s flagstat %s.sort.bam >%s.sort.bam.flagstat' %(bins['sam'], options.prefix, options.prefix)

    if os.path.exists('%s.sai1.ok'%options.prefix) == False:
        print cmdExec(cmd1)
        tmp = open('%s.sai1.ok'%options.prefix, 'w')
        tmp.close()
    else:
        print 'Skip cmd: %s' %cmd1

    if os.path.exists('%s.sai2.ok'%options.prefix) == False:
        print cmdExec(cmd2)
        tmp = open('%s.sai2.ok'%options.prefix, 'w')
        tmp.close()
    else:
        print 'Skip cmd: %s' %cmd2

    if os.path.exists('%s.sam.ok'%options.prefix) == False:
        print cmdExec(cmd3)
        tmp = open('%s.sam.ok'%options.prefix, 'w')
        tmp.close()
    else:
        print 'Skip cmd: %s' %cmd3

    if os.path.exists('%s.bam.ok'%options.prefix) == False:
        print cmdExec(cmd4)
        tmp = open('%s.bam.ok'%options.prefix, 'w')
        tmp.close()
    else:
        print 'Skip cmd: %s' %cmd4

    if os.path.exists('%s.sort.bam.ok'%options.prefix) == False:
        print cmdExec(cmd5)
        tmp = open('%s.sort.bam.ok'%options.prefix, 'w')
        tmp.close()
    else:
        print 'Skip cmd: %s' %cmd5

    print cmdExec(cmd6)
    os.system('rm %s.*.ok'%options.prefix)
    os.system('rm %s.sai1 %s.sai2 %s.sam %s.bam'%(options.prefix, options.prefix, options.prefix, options.prefix))


def se_run(options, bins):
    if options.option == '':
        option = '-e 50 -i 15 -q 10'
    else:
        option = options.option

    cmd1 = '%s aln -t %d %s %s %s >%s.sai1' \
            %(bins['bwa'], options.threads, option, options.ref, options.file1, options.prefix)

    if options.rg == '':
        sample = options.prefix.split('/')[-1]
        rg = "@RG\tID:%s\tLB:%s\tPL:ILLUMINA\tSM:%s" %(sample, sample, sample) 
    else:
        rg = options.rg
    cmd3 = '%s samse -r "%s" %s %s.sai1 %s > %s.sam' \
            %(bins['bwa'], rg, options.ref, options.prefix, options.file1, options.prefix)

    cmd4 = '%s view -bS %s.sam -o %s.bam' %(bins['sam'], options.prefix, options.prefix) 
    
    cmd5 = 'java -Xmx4g -jar %s INPUT=%s.bam OUTPUT=%s.sort.bam SORT_ORDER=coordinate VALIDATION_STRINGENCY=LENIENT' \
            %(bins['sortsam'], options.prefix, options.prefix)

    cmd6 = '%s flagstat %s.sort.bam >%s.sort.bam.flagstat' %(bins['sam'], options.prefix, options.prefix)

    if os.path.exists('%s.sai1.ok'%options.prefix) == False:
        print cmdExec(cmd1)
        tmp = open('%s.sai1.ok'%options.prefix, 'w')
        tmp.close()
    else:
        print 'Skip cmd: %s' %cmd1

    if os.path.exists('%s.sam.ok'%options.prefix) == False:
        print cmdExec(cmd3)
        tmp = open('%s.sam.ok'%options.prefix, 'w')
        tmp.close()
    else:
        print 'Skip cmd: %s' %cmd3

    if os.path.exists('%s.bam.ok'%options.prefix) == False:
        print cmdExec(cmd4)
        tmp = open('%s.bam.ok'%options.prefix, 'w')
        tmp.close()
    else:
        print 'Skip cmd: %s' %cmd4

    if os.path.exists('%s.sort.bam.ok'%options.prefix) == False:
        print cmdExec(cmd5)
        tmp = open('%s.sort.bam.ok'%options.prefix, 'w')
        tmp.close()
    else:
        print 'Skip cmd: %s' %cmd5

    print cmdExec(cmd6)
    os.system('rm %s.*.ok'%options.prefix)
    os.system('rm %s.sai1 %s.sam %s.bam' %(options.prefix, options.prefix, options.prefix))


def main():
    parser = OptionParser(usage="usage: %prog [options]")
    parser.add_option("-1","--read1", dest="file1", help="Read 1 file.")
    parser.add_option("-2","--read2", dest="file2", help="Read 2 file. If not given, run bwa in SE mode.")
    parser.add_option("-o","--prefix",dest="prefix",default="bwa_output",help="Output prefix. [Default=bwa_output]")
    parser.add_option("-r","--ref",dest="ref",help="Reference fasta path.")
    parser.add_option("-t","--threads",dest="threads",default=1, type=int, help="Threads to use. [Default=1]")
    parser.add_option("-g","--rg", dest="rg", default="", help="Read Group.")
    parser.add_option("-a","--option", dest="option", default="", help="Bwa option. [Default=\"-e 50 -i 15 -q 10\"]")
    (options, args) = parser.parse_args()

    if not options.file1 or not options.ref:
        parser.error("Incorrect argument.")

    bins = {
            'sam':'/delldata/Analysis/yukai/software/samtools-0.1.19/samtools',
            'bwa':'/delldata/Analysis/yukai/software/bwa-0.7.10/bwa',
            'sortsam':'/delldata/Analysis/yukai/software/picard-tools-1.119/SortSam.jar'
            }

    if not options.file2:
        se_run(options, bins)
    else:
        pe_run(options, bins)


if __name__ == '__main__':
    main()




