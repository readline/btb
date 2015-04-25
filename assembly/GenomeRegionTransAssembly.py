#!/usr/bin/env python
# trinity_GG_gff.listing_to_continuous_region.py
# version 1.0
# Kai Yu
# github.com/readline
# 150423
##############################################
# version1.0: Runable, but sortcheck and bam2gff module runs in single processor.

import os,sys,time,gzip
import multiprocessing
import commands
import Fasta
from optparse import OptionParser

def timestamp():
    return '[%s] ' %time.strftime('%Y-%m-%d %A %X %Z',time.localtime(time.time()))

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
    start = int(c[1])
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
            if c[0] != lastchr:
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
            elif int(c[1]) - lastgood > options.maxgap:
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
    savegff = open(options.outpath+'/bam.regions.gff','w')
    for chrid in tmpdic:
        for n in range(len(tmpdic[chrid])):
            savegff.write('%s\tpartition\tregion\t%d\t%d\t.\t+\t.\t.\t%s:%d-%d\n' \
                %(tmpdic[chrid][n][0], tmpdic[chrid][n][1], tmpdic[chrid][n][2], \
                  tmpdic[chrid][n][0], tmpdic[chrid][n][1], tmpdic[chrid][n][2]))
    savegff.close()
    return tmpdic

def Tbam2gff():
    '''bam2gff function test'''
    sambin = 'samtools'
    class Arguments(object):
        def __init__(self):
            self.outpath='test1'
            self.mapq=1
            self.bampath='test.bam'
            self.mindep=1
            self.maxgap=10000
    options = Arguments()
    result = bam2gff(sambin,options)
    # for k,v in result.iteritems():
    #     print k,v
    #     raw_input()

def writeFasta(sambin, gffdic, chrid, optdic): 
    # print 'Prepare %s reads in pid %d' %(chrid, os.getpid())
    try:
        os.makedirs('%s/Regions/%s' %(optdic['outpath'], chrid))
    except:
        pass
    tmp = []
    for n in xrange(len(gffdic[chrid])):
        region = '%s:%d-%d' %(gffdic[chrid][n][0], gffdic[chrid][n][1], gffdic[chrid][n][2])
        bamfile = os.popen('%s view %s %s' %(sambin, optdic['bampath'], region))
        savefile = open('%s/Regions/%s/region%d-%d.fa' \
                         %(optdic['outpath'], chrid, gffdic[chrid][n][1], gffdic[chrid][n][2]), 'w')
        tmp.append('%s/Regions/%s/region%d-%d' %(optdic['outpath'], chrid, gffdic[chrid][n][1], gffdic[chrid][n][2]))
        while 1:
            line = bamfile.readline()
            if not line: break
            c = line.rstrip().split('\t')
            readid, seq, flag = c[0], c[9], bin(int(c[1]))[2:][::-1]
            if flag[4] == 1:
                seq = seq[::-1]
            else:
                pass
            if flag[0] == '1' and flag[6] == '1':
                readid += ':1'
            elif flag[0] == '1' and flag[6] != '1':
                readid += ':2'
            elif flag[0] != '1':
                readid += ':1'
            savefile.write('>%s\n%s\n' %(readid, seq))
        savefile.close()
    return tmp

def TwriteFasta():
    sambin = 'samtools'
    class Arguments(object):
        def __init__(self):
            self.bampath = 'test.bam'
            self.outpath = 'test1'
    options = Arguments()
    gffdic = {'scaffold93':{0: ['scaffold93', 651, 56699], 1: ['scaffold93', 91292, 101298], \
    2: ['scaffold93', 112569, 217708], 3: ['scaffold93', 230447, 230545], 4: ['scaffold93', 242112, 265655], \
    5: ['scaffold93', 280225, 418742], 6: ['scaffold93', 434343, 567747]},'scaffold225': \
    {0: ['scaffold225', 221, 73963], 1: ['scaffold225', 87313, 138805], 2: ['scaffold225', 149103, 152824], \
    3: ['scaffold225', 163672, 164670], 4: ['scaffold225', 175165, 206944], 5: ['scaffold225', 217406, 223573], \
    6: ['scaffold225', 241800, 246287], 7: ['scaffold225', 257516, 308020]}}
    for chrid in gffdic.keys():
        writeFasta(sambin, gffdic, chrid, options)

def paraWriteFasta(sambin, tribin, gffdic, options):
    optdic = {'outpath':options.outpath, 'bampath':options.bampath}
    pool = multiprocessing.Pool(processes=options.thread)
    result = []
    for chrid in gffdic:
        result.append(pool.apply_async(writeFasta, args=(sambin, gffdic, chrid, optdic),))    #(funcgo[sambin, gffdic, chrid, options]))
    pool.close()
    pool.join()
    cmdfile = open('%s/region_trinity.cmd' %options.outpath, 'w')
    tmp = []
    for n in result:
        for reg in n.get():
            tmp.append(reg)
            cmd ='%s --single %s/%s.fa --output %s/%s.trinity --CPU 1 --max_memory 1G --seqType fa --full_cleanup --verbose; rm -rf %s/%s.trinity' \
                %(tribin, os.getcwd(), reg, os.getcwd(), reg, os.getcwd(), reg)
            cmdfile.write(cmd+'\n')
    cmdfile.close()
    return tmp

def TparaWriteFasta():
    sambin = 'samtools'
    tribin = 'Trinity'
    class Arguments(object):
        def __init__(self):
            self.bampath = 'test.bam'
            self.outpath = 'test1'
            self.thread  = 24
            self.mapq=1
            self.mindep=1
            self.maxgap=10000
    options = Arguments()
    gffdic = bam2gff(sambin,options)
    paraWriteFasta(sambin, tribin, gffdic, options)

def runCMD(cmd):
    # print os.getpid(), cmd.rstrip()
    tmprun = commands.getoutput('%s' %cmd.rstrip())
    return cmd.rstrip(), tmprun

def paraCMD(options):
    pool = multiprocessing.Pool(processes=options.thread)
    result = []
    cmdfile = open('%s/region_trinity.cmd' %options.outpath, 'r')
    while 1:
        line = cmdfile.readline()
        if not line: break
        # print line
        result.append(pool.apply_async(runCMD, (line,)))
    cmdfile.close()
    pool.close()
    pool.join()
    savefile = gzip.open('%s/region_trinity.cmd.runlog.gz' %options.outpath, 'wb')
    for run in result:
        savefile.write('#'+'-'*80+'\n')
        savefile.write('#CMD %s\n' %run.get()[0])
        savefile.write('#'+'-'*80+'\n')
        savefile.write(run.get()[1])
    savefile.close()

def TparaCMD():
    class Argument(object):
        def __init__(self):
            self.thread=24
            self.outpath='test1'
    options=Argument()
    paraCMD(options)

def getQstatJID():
    tmp = commands.getoutput('qstat')
    jobList = []
    if tmp != '':
        tmplist = tmp.split('\n')
        for line in tmplist[2:]:
            jobList.append(int(line.strip().split()[0]))
    return jobList

def qsubCMD(options):
    pid = os.getpid()
    cmdfile = open('%s/region_trinity.cmd' %options.outpath, 'r')
    count = 0
    subed = []
    while 1:
        cmd = cmdfile.readline().rstrip()
        if not cmd: break
        count += 1
        savefile = open('%s/region_trinity.cmd.%d.%d' %(options.outpath,pid,count), 'w')
        savefile.write(cmd)
        savefile.close()
        while 1:
            sgeJobCount = len(getQstatJID())
            if sgeJobCount > 300: time.sleep(3)
            if sgeJobCount < 390: break
            time.sleep(30)
        run = commands.getoutput('cd %s && %s region_trinity.cmd.%d.%d' \
                                %(options.outpath, options.sge, pid, count))
        subed.append(int(run.strip().split()[2]))
    # print 'subed',subed
    # print 'running',getQstatJID()
    while 1:
        time.sleep(3)
        sgeJobs = getQstatJID()
        count = 0
        for job in sgeJobs:
            if job in subed:
                count += 1
        if count == 0:
            break
    savefile = gzip.open('%s/region_trinity.cmd.runlog.gz' %options.outpath, 'wb')
    for n in range(1,len(subed)+1):
        savefile.write('#'+'-'*80+'\n')
        tmpfile = open('%s/region_trinity.cmd.%d.%d' %(options.outpath,pid,n), 'r')
        cmd = tmpfile.readline().rstrip()
        tmpfile.close()
        savefile.write('#CMD %s\n' %cmd)
        savefile.write('#'+'-'*80+'\n')
        savefile.write('#STDOUT\n')
        savefile.write('#'+'-'*80+'\n')
        tmpfile = open(commands.getoutput('ls %s/region_trinity.cmd.%d.%d.o*'%(options.outpath,pid,n)), 'r')
        savefile.write(tmpfile.read()+'\n')
        tmpfile.close()
        savefile.write('#'+'-'*80+'\n')
        savefile.write('#STDERR\n')
        savefile.write('#'+'-'*80+'\n')
        tmpfile = open(commands.getoutput('ls %s/region_trinity.cmd.%d.%d.e*'%(options.outpath,pid,n)), 'r')
        savefile.write(tmpfile.read()+'\n')
        tmpfile.close()
    savefile.close()
    os.system('rm %s/region_trinity.cmd.%d.*' %(options.outpath,pid))
    return True

def TqsubCMD():
    class Argument(object):
        def __init__(self):
            self.outpath = 'test1'
            self.sge='qsub -q all.q -cwd -V -l vf=1g'
    options = Argument()
    qsubCMD(options)

def mergeRegionAssemblies(regionDirList, options):
    count = 0
    c_count = 0
    g_count = 0
    fadic = {}
    orderlist = []
    desdic= {}

    for tmpdir in regionDirList:
        clist, glist = [],[]
        tridir = '%s.trinity.Trinity.fasta' %tmpdir
        if not os.path.isfile(tridir):
            continue
        tmpfa = Fasta.Parse(tridir)
        for seqid in tmpfa.id:
            count += 1
            id2 = seqid.split('|')[1]
            c, g, i = id2.split('_')
            if c not in clist:
                clist.append(c)
                c_count += 1
            if g not in glist:
                glist.append(g)
                g_count += 1
            newid = 'Transcript%d|c%d_g%d_%s' %(count,c_count,g_count,i)
            chrid = tmpdir.split('/')[-2]
            regid = tmpdir.split('/')[-1][6:]
            seqlen= len(tmpfa.seq[seqid])
            fadic[newid] = tmpfa.seq[seqid]
            desdic[newid] = '%s:%s len=%d' %(chrid,regid,seqlen)
            orderlist.append(newid)
    Fasta.write(fadic, '%s/Transcript.fa' %options.outpath, orderlist=orderlist, description=desdic)

def main():
    '''
    Two way:
    1. Only bam file given
    2. Bam and gff file given
    '''
    ########## Get options ##########
    parser = OptionParser(usage="usage: %prog [options]")
    parser.add_option("-b","--bam",dest="bampath",help="Input bam path. [Required]")
    parser.add_option("-f","--gff",dest="gffpath",default=None,help="GFF file contains regions. [Optional]")
    parser.add_option("-d","--depth",dest="mindep",default=1,type="int",help="Minimum depth. [Default=1]")
    parser.add_option("-g","--gap",dest="maxgap",default=10000,type="int",help="Max gap tollerence in a region. [Default=10000]")
    parser.add_option("-q","--mapq",dest="mapq",default=1,type="int",help="Mapping quality cutoff. [Default=1]")
    parser.add_option("-t","--thread",dest="thread",default=1,type="int",help="Thread to use. [Default=1]")
    parser.add_option("-o","--output",dest="outpath",default="GR_output",help="Output directory. [Default=\"GR_output_(pid)\"]")
    parser.add_option("-s","--sge",dest="sge",default="",help="SGE submit command. [Default=\"\", use single node multiprocessing]")
    (options,args) = parser.parse_args()
    if not options.bampath:
        parser.error("Input bam path not given!")
    if options.gffpath != None:
        print 'GFF file %s given, --depth/--gap/--mapq arguments discarded.' %options.gffpath
    prefix = options.outpath+'_'+str(os.getpid())

    print '%sStart!' %timestamp()
    
    ########## Get samtools path ##########
    sambin = os.popen("which samtools").readline().rstrip()
    if sambin == '':
        sys.exit('Samtools not found. Please add samtools to $PATH')

    if os.path.isfile('%s.bai'%options.bampath) != True and os.path.isfile(options.bampath[:-1]+'i') != True:
        print '%sBam not indexed, index it with samtools.'%timestamp()
        tmp = commands.getoutput('%s index %s' %(sambin, options.bampath))

    ########## Get Trinity path ##########
    tribin = os.popen("which Trinity").readline().rstrip()
    if tribin == '':
        sys.exit('Trinity not found. Please add samtools to $PATH')

    ########## Prepare output directory ##########
    if os.path.exists(options.outpath):
        ifrewrite = raw_input('Output dir %s exist, rewrite? "Y/N"' %options.outpath)
        if ifrewrite.upper() == 'N':
            sys.exit()
        elif ifrewrite.upper() == 'Y':
            pass
        else:
            sys.exit('Unrecognized input, input should be Y or N.')
    else:
        os.mkdir(options.outpath)

    ########## Check wether bam file is sorted #########
    isBamSorted(sambin, options.bampath)

    ########## Get ref chr list ##########
    print '%sBam file checked, import chr list.' %timestamp()
    chrList = getHeaderList(sambin, options.bampath)

    ########## Read bam file to calc regions and generate gff ##########
    print '%sRead bam to generate regions.' %timestamp()
    gffdic = bam2gff(sambin,options)

    ########## Prepare region's fasta and region's downstream cmd ##########
    regionDirList  = paraWriteFasta(sambin, tribin, gffdic, options)
    print '%sRun region CMDs in paralleled mode' %timestamp()
    if options.sge == '':
        print 'Run region CMDs by MP mode.'
        paraCMD(options)
    else:
        print 'Run region CMDs by SGE mode.'
        qsubCMD(options)

    ########## Merge regions' output ##########
    print '%sRegion CMDs all done, merge regions\' outputs.' %timestamp()
    mergeRegionAssemblies(regionDirList, options)

    ########## Clean up region files ##########
    print '%sClean up region files.' %timestamp()
    os.system('rm -rf %s/Regions '%options.outpath)
    print '%sFinished.' %timestamp()

if __name__ == '__main__':
    main()
    # # gffdic = Tbam2gff()
    # # TwriteFasta()
    # TparaWriteFasta()
    # # TparaCMD()
    # TqsubCMD()





