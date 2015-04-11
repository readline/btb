#!/usr/bin/env python
# Fasta.py
# Kai Yu
# Version 1.3 @ 150411
class Parse(object):
    '''class Parse(fastaPath)
    return self.id (list)
           self.seq (dictionary with key in self.id)
           self.des (dictionary with key in self.id)
    '''
    def __init__(self, fastaPath):
        self.fastaPath = fastaPath
        if self.fastaPath[-3:] == '.gz':
            import gzip
            self.file = gzip.open(self.fastaPath,'rb')
        else:
            self.file = open(self.fastaPath, 'r')
        self.id  = []
        self.seq = {}
        self.des = {}
        while 1:
            line = self.file.readline()
            if not line:
                break
            if line == '':
                continue
            if line[0] == '>':
                break
        while 1:
            if not line:
                break
            if line == '':
                continue
            title = line[1:].rstrip()
            seqid = title.split()[0]
            description = title[len(seqid):]
            seq = ''
            while 1:
                line = self.file.readline()
                if not line:
                    self.seq[seqid] = seq
                    self.id.append(seqid)
                    self.des[seqid] = description
                    break
                if line == '':
                    continue
                if line[0] != '>':
                    seq += line.rstrip()
                elif line[0] == '>':
                    self.seq[seqid] = seq
                    self.id.append(seqid)
                    self.des[seqid] = description
                    break
        self.file.close()

def write(fadic, savepath, orderlist=[],description={}):
    '''class Write(fadic, savepath, *orderlist=[default []], *description=[default {}])
    '''
    from textwrap import wrap
    fadic = fadic
    savepath = savepath
    orderlist = orderlist
    description=description

    if savepath[-3:] == '.gz':
        import gzip
        infile = gzip.open(savepath,'wb')
    else:
        infile = open(savepath,'w')
    if len(orderlist) == 0:
        orderlist = fadic.keys()
    for seqid in orderlist:
        seq = fadic[seqid]
        des = ''
        if seqid in description:
            des = description[seqid]
        infile.write('>'+seqid+des+'\n')
        infile.write('\n'.join(wrap(seq,60)) + '\n')

    infile.close()
