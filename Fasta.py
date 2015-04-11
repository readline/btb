#!/usr/bin/env python
# Fasta.py
# Kai Yu
# Version 1.2 @ 141020
# Modification: Fixed some bugs with which may calse incorrect result when there is 
#               empty line in fasta file.
def parse(fastapath):
    if fastapath[-3:] == '.gz':
        import gzip
        infile = gzip.open(fastapath,'rb')
    else:
        infile = open(fastapath,'r')
    fadic = {'order':[],'seq':{},'description':{}}
    while True:
        line = infile.readline()
        if not line:
            break
        if line == '':
            continue
        if line[0] == '>':
            break
    while True:
        if not line:
            break
        if line == '':
            continue
        title = line[1:].rstrip()
        seqid = title.split()[0]
        description = title[len(seqid):]
        seq = ''
        while True:
            line = infile.readline()
            if not line:
                fadic['seq'][seqid] = seq
                fadic['order'].append(seqid)
                fadic['description'][seqid] = description
                break
            if line == '':
                continue
            if line[0] != '>':
                seq += line.rstrip()
            elif line[0] == '>':
                fadic['seq'][seqid] = seq
                fadic['order'].append(seqid)
                fadic['description'][seqid] = description
                break
    infile.close()
    return fadic
def write(fadic,savepath,orderlist=[],description={}):
    if savepath[-3:] == '.gz':
        savefile = gzip.open(savepath,'wb')
    else:
        savefile = open(savepath,'w')
    if type(orderlist) == list and len(orderlist) != 0:
        for seqid in orderlist:
            seq = fadic[seqid]
            des = ''
            if seqid in description:
                des = description[seqid]
            if len(seq) <= 60:
                savefile.write('>'+seqid+' '+des+'\n'+seq+'\n')
            else:
                savefile.write('>'+seqid+' '+des+'\n')
                while len(seq) > 60:
                    savefile.write(seq[:60]+'\n')
                    seq = seq[60:]
                savefile.write(seq+'\n')
    else:
        for seqid in fadic:
            seq = fadic[seqid]
            des = ''
            if seqid in description:
                des = description[seqid]
            if len(seq) <= 60:
                savefile.write('>'+seqid+' '+des+'\n'+seq+'\n')
            else:
                savefile.write('>'+seqid+' '+des+'\n')
                while len(seq) > 60:
                    savefile.write(seq[:60]+'\n')
                    seq = seq[60:]
                savefile.write(seq+'\n')
    savefile.close()
def main():
    print """#!/usr/bin/env python
# Fasta.py
# Kai Yu
# Version 1.2 @ 141020
# Modification: Fixed some bugs with which may calse incorrect result when there is 
#               empty line in fasta file."""
    print "Include:\n\tparse(fastapath)\treturn {'order':[],'seq':{},'description':{}}\n\t\
write(fadic,savepath,orderlist*,description*)\treturn None\tOutput to savepath"
if __name__ == '__main__':
    main()
