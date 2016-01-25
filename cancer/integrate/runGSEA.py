#!/usr/bin/env python
# FPKM file is a matrix with 1 row.name colume and 1 col.name row
# Group file is a file contains several columes. Each colume is a class, with a class name in the first row. 
# There are no row.names
import os,sys

def loadGroups(groupath):
    groupcount = {}
    samplelist = []
    groupdic = {}

    with open(groupath, 'r') as infile:
        grouplist = infile.readline().rstrip().split('\t')
        for group in grouplist:
            groupcount[group] = 0
        while 1:
            line = infile.readline()
            if not line:
                break
            c = line.rstrip().split('\t')
            for n in range(len(c)):
                item = c[n]
                group = grouplist[n]
                if item == '' or item in samplelist:
                    continue
                samplelist.append(item)
                groupcount[group] += 1
                groupdic[item] = group
    return groupcount, samplelist, groupdic

def prepareMatrix(fpkmpath, groupath, prefix):
    groupcount, samplelist, groupdic = loadGroups(groupath)
    with open(prefix+'/GSEA.input.cls', 'w') as savefile:
        savefile.write('%d %d 1\n#'%(len(samplelist), len(groupcount)))
        savefile.write(' '.join(groupcount.keys())+'\n')
        savefile.write(' '.join([groupdic[i] for i in samplelist])+'\n')

    genedic = {}
    with open(fpkmpath, 'r') as infile:
        tmpheader = infile.readline().rstrip().split('\t')
        order = []
        for n in samplelist:
            order.append(tmpheader.index(n))
        while 1:
            line = infile.readline()
            if not line:
                break
            if line.split('\t')[0] not in genedic:
                genedic[line.split('\t')[0]] = 1
    genecount = len(genedic)
    genedic = {}

    with open(prefix+'/GSEA.input.gct','w') as savefile:
        savefile.write('#1.2\n%d\t%d\nNAME\tDESCRIPTION'%(genecount, len(samplelist)))
        for sample in samplelist:
            savefile.write('\t%s'%sample)
        savefile.write('\n')

        infile = open(fpkmpath, 'r')
        infile.readline()
        while 1:
            line = infile.readline()
            if not line:
                break
            c = line.rstrip().split('\t')
            if c[0] in genedic:
                continue
            else:
                genedic[c[0]] = 1
            savefile.write('%s\tna'%c[0])
            for n in order:
                savefile.write('\t%s'%c[n])
            savefile.write('\n')
        infile.close()

def main():
    try:
        fpkmpath = sys.argv[1]
        groupath = sys.argv[2]
        refpath  = sys.argv[3]
        groupname= sys.argv[4]
        prefix   = sys.argv[5]
    except:
        sys.exit(sys.argv[0] + ' [fpkm path] [group path] [ref gmt path] [output group name] [output dir]')

    if os.path.exists(prefix):
        pass
    else:
        os.mkdir(prefix)

    prepareMatrix(fpkmpath, groupath, prefix)

    template = '''GSEA.program.location <- "/delldata/Analysis/yukai/software/GSEA-P-R/GSEA.1.0.R"
source(GSEA.program.location, verbose=F, max.deparse.length=9999)

GSEA(
 input.ds =  "[[[GCT]]]",
 input.cls = "[[[CLS]]]",
 gs.db =     "[[[GMT]]]",
 output.directory = "[[[DIR]]]/",
 doc.string            = "[[[SAMPLE]]]",
 non.interactive.run   = F,
 reshuffling.type      = "sample.labels",
 nperm                 = 1000,
 weighted.score.type   =  1,
 nom.p.val.threshold   = -1,
 fwer.p.val.threshold  = -1,
 fdr.q.val.threshold   = 0.25,
 topgs                 = 20,
 adjust.FDR.q.val      = T,
 gs.size.threshold.min = 15,
 gs.size.threshold.max = 500,
 reverse.sign          = F,
 preproc.type          = 0,
 random.seed           = 760435,
 perm.type             = 0,
 fraction              = 1.0,
 replace               = F,
 save.intermediate.results = F,
 OLD.GSEA              = F,
 use.fast.enrichment.routine = T
 )

GSEA.Analyze.Sets(
 directory = "[[[DIR]]]/",
 topgs = 20,
 height = 16,
 width = 16
)'''
    script = template.replace('[[[GCT]]]', '%s/GSEA.input.gct'%prefix)
    script = script.replace('[[[CLS]]]', '%s/GSEA.input.cls'%prefix)
    script = script.replace('[[[GMT]]]', refpath)
    script = script.replace('[[[DIR]]]', prefix)
    script = script.replace('[[[SAMPLE]]]', groupname)
    with open('%s/GSEA.run.R'%prefix,'w') as savefile:
        savefile.write(script)
    print 'Running GSEA...'
    os.system('Rscript %s/GSEA.run.R'%prefix)

if __name__ == '__main__':
    main()

