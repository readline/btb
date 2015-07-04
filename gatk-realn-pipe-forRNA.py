#!/usr/bin/env python
# =============================================================================
# Filename: gatk-realn-pipe-forRNA.py
# Version: 
# Author: Kai Yu - finno@live.cn
# https://github.com/readline
# Last modified: 2015-07-04 16:59
# Description: 
# 
# =============================================================================

import os, sys, time, commands
from optparse import OptionParser

def now():
    return time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))

def cmdExec(cmd):
    print
    print '[%s] Exec cmd: %s' %(now(), ' '.join(cmd.split()))
    cmdResult = commands.getstatusoutput(cmd)
    if cmdResult[0] == 0:
        print
        print '[%s] Finished cmd: %s' %(now(), ' '.join(cmd.split()))
        print
        return cmdResult[1]
    else:
        print
        print '[%s] Warning! Failed cmd: %s' %(now(), ' '.join(cmd.split()))
        print
        print cmdResult[1]
        print
        sys.exit()

def main():
    parser = OptionParser(usage="usage: %prog [options]")
    parser.add_option("-i", "--input", dest="input", help="Input bam path.")
    parser.add_option("-s", "--sample", dest="sample", help="Sample ID.")
    parser.add_option("-o", "--prefix", dest="prefix", help="Output prefix.")
    parser.add_option("-m", "--tmpdir", dest="tmpdir", help="Java runtime tmp dir.", default="/tmp")
    parser.add_option("-L", "--region", dest="region", help="GATK analysis region.[default=All]", default="")
    parser.add_option("-f", "--fasta", dest="fasta", help="Reference fasta.")
    parser.add_option("-1", "--known1", dest="known1", help="1000G phase1.")
    parser.add_option("-2", "--known2", dest="known2", help="Mills and 1000G.")
    parser.add_option("-3", "--known3", dest="known3", help="dbsnp.")
    parser.add_option("-p", "--picard", dest="picard", help="Path of picard.jar")
    parser.add_option("-g", "--gatk", dest="gatk", help="Path of GenomeAnalysisTK.jar")
    (options, args) = parser.parse_args()
    if options.input:
        input = options.input
    else:
        parser.error("Input bam not given!")

    if options.sample:
        sample = options.sample
    else:
        parser.error("Sample ID not given!")

    if options.prefix:
        prefix = options.prefix
    else:
        parser.error("Output prefix not given!")
    if '/' in prefix:
        prefixdir = '/'.join(prefix.split('/')[:-1])
        try:
            os.system('mkdir -p %s'%prefixdir)
        except:
            print 'Prefix dir %s exists.' %prefixdir

    if options.tmpdir:
        tmpdir = options.tmpdir
        try:
            os.system('mkdir -p %s'%tmpdir)
        except:
            print 'Mkdir %s failed.' %prefixdir

    if options.fasta:
        fasta = options.fasta
    else:
        parser.error("Reference fasta not given")

    if options.region != "":
        region = ' -L %s ' %options.region
    else:
        region = ''

    if options.known1:
        known1 = options.known1
    else:
        parser.error("known1 not given.")
        
    if options.known2:
        known2 = options.known2
    else:
        parser.error("known2 not given.")
        
    if options.known1:
        known3 = options.known3
    else:
        parser.error("known3 not given.")
        
    if options.picard:
        picard = options.picard
    else:
        parser.error("Path of picard.jar not given.")
        
    if options.gatk:
        gatk = options.gatk
    else:
        parser.error("Path of GenomeAnalysisTK.jar not given.")
        

    print '[[[ All start! ]]]'

    # Add RG
    cmd1 = 'java -Xmx8g -Djava.io.tmpdir=%s -jar %s AddOrReplaceReadGroups \
               I=%s \
               O=%s.rg.bam \
               SO=coordinate \
               RGID=%s \
               RGLB=%s \
               RGPL=illumina \
               RGPU=hiseq \
               RGSM=%s' %(tmpdir, picard, input, prefix, sample, sample, sample)
    if os.path.exists('%s.rg.bam.ok'%prefix) == False:
        print
        print cmdExec(cmd1)
        tmp = open('%s.rg.bam.ok'%prefix, 'w')
        tmp.close()
    else:
        print
        print 'Skip cmd: %s' %' '.join(cmd1.split())

    # Markduplicates
    cmd2 = 'java -Xmx8g -Djava.io.tmpdir=%s -jar %s MarkDuplicates \
               I=%s.rg.bam \
               O=%s.rg.rmdup.bam \
               AS=true \
               CREATE_INDEX=true \
               VALIDATION_STRINGENCY=SILENT \
               M=%s.rg.rmdup.metrics' %(tmpdir, picard, prefix, prefix, prefix)
    if os.path.exists('%s.rg.rmdup.bam.ok'%prefix) == False:
        print
        print cmdExec(cmd2)
        tmp = open('%s.rg.rmdup.bam.ok'%prefix, 'w')
        tmp.close()
        os.remove('%s.rg.bam' %prefix)
    else:
        print
        print 'Skip cmd: %s' %' '.join(cmd2.split())

    # SplitNCigarReads
    cmd3 = 'java -Xmx8g -Djava.io.tmpdir=%s -jar %s \
               -T SplitNCigarReads \
               -R %s \
               -I %s.rg.rmdup.bam \
               -o %s.rg.rmdup.sncr.bam \
               -rf ReassignOneMappingQuality \
               %s \
               -RMQF 255 \
               -RMQT 60 \
               -U ALLOW_N_CIGAR_READS' %(tmpdir, gatk, fasta, prefix, prefix, region)
    if os.path.exists('%s.rg.rmdup.sncr.bam.ok'%prefix) == False:
        print
        print cmdExec(cmd3)
        tmp = open('%s.rg.rmdup.sncr.bam.ok'%prefix, 'w')
        tmp.close()
        os.remove('%s.rg.rmdup.bam'%prefix)
        os.remove('%s.rg.rmdup.bai'%prefix)
        os.remove('%s.rg.rmdup.metrics'%prefix)
    else:
        print
        print 'Skip cmd: %s' %' '.join(cmd3.split())

    # RealignerTargetCreator
    cmd4 = 'java -Xmx8g -Djava.io.tmpdir=%s -jar %s \
               -T RealignerTargetCreator \
               -l INFO \
               -R %s \
               %s \
               -known %s\
               -known %s\
               -I %s.rg.rmdup.sncr.bam \
               -o %s.rg.rmdup.sncr.intervals' %(tmpdir, gatk, fasta, region, known1, known2, prefix, prefix)
    if os.path.exists('%s.rg.rmdup.sncr.intervals.ok'%prefix) == False:
        print
        print cmdExec(cmd4)
        tmp = open('%s.rg.rmdup.sncr.intervals.ok'%prefix, 'w')
        tmp.close()
    else:
        print
        print 'Skip cmd: %s' %' '.join(cmd4.split())

    # IndelRealigner
    cmd5 = 'java -Xmx8g -Djava.io.tmpdir=%s -jar %s \
               -T IndelRealigner \
               -l INFO \
               -R %s \
               %s \
               -known %s \
               -known %s \
               -targetIntervals %s.rg.rmdup.sncr.intervals \
               -I %s.rg.rmdup.sncr.bam \
               -o %s.rg.rmdup.sncr.realn.bam' %(tmpdir, gatk, fasta, region, known1, known2, prefix, prefix, prefix)
    if os.path.exists('%s.rg.rmdup.sncr.realn.bam.ok'%prefix) == False:
        print
        print cmdExec(cmd5)
        tmp = open('%s.rg.rmdup.sncr.realn.bam.ok'%prefix, 'w')
        tmp.close()
        os.remove('%s.rg.rmdup.sncr.intervals'%prefix)
        os.remove('%s.rg.rmdup.sncr.bam'%prefix)
        os.remove('%s.rg.rmdup.sncr.bai'%prefix)
    else:
        print
        print 'Skip cmd: %s' %' '.join(cmd5.split())

    # BaseRecalibrator
    cmd6 = 'java -Xmx8g -Djava.io.tmpdir=%s -jar %s \
               -T BaseRecalibrator \
               -R %s \
               %s \
               -knownSites %s \
               -knownSites %s \
               -knownSites %s \
               -I %s.rg.rmdup.sncr.realn.bam \
               -o %s.rg.rmdup.sncr.realn.recal.grp' %(tmpdir, gatk, fasta, region, known1, known2, known3, prefix, prefix)
    if os.path.exists('%s.rg.rmdup.sncr.realn.recal.grp.ok'%prefix) == False:
        print
        print cmdExec(cmd6)
        tmp = open('%s.rg.rmdup.sncr.realn.recal.grp.ok'%prefix, 'w')
        tmp.close()
    else:
        print
        print 'Skip cmd: %s' %' '.join(cmd6.split())

    # PrintReads
    cmd7 = 'java -Xmx8g -Djava.io.tmpdir=%s -jar %s \
               -T PrintReads \
               -R %s \
               %s \
               -BQSR %s.rg.rmdup.sncr.realn.recal.grp \
               -I %s.rg.rmdup.sncr.realn.bam \
               -o %s.phase1.bam' %(tmpdir, gatk, fasta, region, prefix, prefix, prefix)
    if os.path.exists('%s.phase1.bam.ok'%prefix) == False:
        print
        print cmdExec(cmd7)
        tmp = open('%s.phase1.bam.ok'%prefix, 'w')
        tmp.close()
        os.remove('%s.rg.rmdup.sncr.realn.recal.grp'%prefix)
        os.remove('%s.rg.rmdup.sncr.realn.bam'%prefix)
        os.remove('%s.rg.rmdup.sncr.realn.bai'%prefix)
        os.system('rm %s.*.ok'%prefix)
    else:
        print
        print 'Skip cmd: %s' %' '.join(cmd7.split())

    print
    print '[[[ All finished! ]]]'

if __name__ == '__main__':
    main()
