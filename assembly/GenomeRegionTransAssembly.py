#!/usr/bin/env python
# trinity_GG_gff.listing_to_continuous_region.py
# version 1.0
# Kai Yu
# github.com/readline
# 150423
##############################################

import os,sys,time
from optparse import OptionParser

def timestamp():
    print '[%s] ' %time.strftime('%Y-%m-%d %A %X %Z',time.localtime(time.time()))

def isBamSorted(sambin, bampath):
    '''Check wether the bamfile is sorted.
    If sorted, return True, otherwise exit'''
    tmp = os.popen('%s depth %s | head' %(sambin, bampath)).readline()
    if tmp == '':
        sys.exit('Unsorted bam file. Please sort it first.')
    else:
        return True

def getHeaderList(sambin, bampath):
    '''Get ref chr list by read samtools header.'''
    samHeader = os.popen('%s view -H %s' %(sambin, bampath))
    chrList = []
    while 1:
        line = samHeader.readline().rstrip()
        if not line: break
        c = line.split('\t')
        if c[0] == '@SQ':
            chrList.append(c[1].split(':')[1])
    return chrList

def bam2gff(sambin, options):
    samfile = os.popen('%s depth -Q %d %s' %(sambin, options.mapq, options.bampath))
    tmpline = samfile.readline()
    if tmpline.rstrip() == '':
        sys.exit('Bamfile can not open.')
    tmpdic = {}
    c = tmpline.rstrip().split('\t')
    thischr, start = c[0],int(c[1])
    lastgood, lastchr, status = start,c[0], 1
    while 1:
        line = samfile.readline()
        if not line:
            # If get to the EOF
            if status == 1:
                # Is counting
                if lastchr not in tmpdic:
                    tmpdic[lastchr] = {}
                tmpdic[lastchr][len(tmpdic[lastchr].keys())] = [lastchr, start, lastgood]
            break
        c = line.rstrip().split('\t')
        if status == 1:
            # Is counting
            if int(c[1]) - lastgood > options.maxgap:
                # Gap length exceed
                status = 0  # Quit counting
                if lastchr not in tmpdic:
                    tmpdic[lastchr] = {}
                tmpdic[lastchr][len(tmpdic[lastchr].keys())] = [lastchr, start, lastgood]
                continue
            elif int(c[1]) - lastgood <= options.maxgap:
                # Gap length tollerent area
                if int(c[2]) >= options.mindep:
                    # This base's depth OK
                    lastchr, lastgood = c[0],int(c[1]) # Refresh the "last" words
                    continue
                else:
                    # This base's depth not pass
                    # Do nothing with the "last" words 
                    continue
            elif c[0] != lastchr:
                # If get to another chr
                status = 0 # Quit counting
                if lastchr not in tmpdic:
                    tmpdic[lastchr] = {}
                tmpdic[lastchr][len(tmpdic[lastchr].keys())] = [lastchr, start, lastgood]
                if int(c[2]) >= options.mindep:
                    # This base's depth OK, start counting 
                    # refresh the "last" words and start
                    start = int(c[1])
                    lastgood = start
                    lastchr = c[0]
                    status = 1
                continue
        elif status == 0:
            # If not counting
            if int(c[2]) >= options.mindep:
                # This base's depth OK, start counting 
                # refresh the "last" words and start
                start = int(c[1])
                lastgood = start
                lastchr = c[0]
                status = 1
                continue
            else:
                # This base's depth not pass
                # Do nothing and go to next
                continue
    samfile = ''
    return tmpdic



def main():
    '''
    Two way:
    1. Only bam file given
    2. Bam and gff file given
    '''
    ########## Get options ##########
    parser = parser.add_option(usage="usage: %prog [options]")
    parser.add_options("-b","--bam",dest="bampath",help="Input bam path. [Required]")
    parser.add_options("-f","--gff",dest="gffpath",default=None,help="GFF file contains regions. [Optional]")
    parser.add_options("-d","--depth",dest="mindep",default=1,type="int",help="Minimum depth. [Default=1]")
    parser.add_options("-g","--gap",dest="maxgap",default=10000,type="int",help="Max gap tollerence in a region. [Default=10000]")
    parser.add_options("-q","--mapq",dest="mapq",default=1,type="int",help="Mapping quality cutoff. [Default=1]")
    parser.add_options("-t","--thread",dest="thread",default=1,type="int",help="Thread to use. [Default=1]")
    parser.add_options("-o","--output",dest="outpath",default="GR_output",help="Output directory. [Default=\"GR_output_(pid)\"]")
    (options,args) = parser.parse_args()
    if not options.bampath:
        parser.error("Input bam path not given!")
    if not options.gffpath:
        print 'GFF file %s given, --depth/--gap/--mapq arguments discarded.'
    prefix = options.outpath+'_'+str(os.getpid())

    print '%sStart!'
    
    ########## Get samtools path ##########
    sambin = os.popen("which samtools").readline().rstrip()
    if sambin == '':
        sys.exit('Samtools not found. Please add samtools to $PATH')

    ########## Check wether bam file is sorted #########
    isBamSorted(sambin, options.bampath)

    ########## Get ref chr list ##########
    print '%sBam file checked, import chr list.'
    chrList = getHeaderList(sambin, options.bampath)







