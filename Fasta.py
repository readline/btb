#!/usr/bin/env python
# Fasta.py
# Kai Yu
# Version 1.3 @ 150411
# Modification: Fixed some bugs with which may calse incorrect result when there is 
#               empty line in fasta file.

import os, sys, gzip
class Readfa(object):
    def __init__(self, fastaPath):
        self.fastaPath = fastaPath
        if self.fastaPath[-3:] == '.gz':
            self.file = gzip.open(self.fastaPath,'rb')
        else:
            self.file = open(self.fastaPath, 'r')
        self.id  = []
        self.seq = {}
        self.des = {}
    def 

# def parse(fastapath):
#     if fastapath[-3:] == '.gz':
#         import gzip
#         infile = gzip.open(fastapath,'rb')
#     else:
#         infile = open(fastapath,'r')
#     fadic = {'order':[],'seq':{},'description':{}}
#     while True:
#         line = infile.readline()
#         if not line:
#             break
#         if line == '':
#             continue
#         if line[0] == '>':
#             break
#     while True:
#         if not line:
#             break
#         if line == '':
#             continue
#         title = line[1:].rstrip()
#         seqid = title.split()[0]
#         description = title[len(seqid):]
#         seq = ''
#         while True:
#             line = infile.readline()
#             if not line:
#                 fadic['seq'][seqid] = seq
#                 fadic['order'].append(seqid)
#                 fadic['description'][seqid] = description
#                 break
#             if line == '':
#                 continue
#             if line[0] != '>':
#                 seq += line.rstrip()
#             elif line[0] == '>':
#                 fadic['seq'][seqid] = seq
#                 fadic['order'].append(seqid)
#                 fadic['description'][seqid] = description
#                 break
#     infile.close()
#     return fadic
# def write(fadic,savepath,orderlist=[],description={}):
#     if savepath[-3:] == '.gz':
#         savefile = gzip.open(savepath,'wb')
#     else:
#         savefile = open(savepath,'w')
#     if type(orderlist) == list and len(orderlist) != 0:
#         for seqid in orderlist:
#             seq = fadic[seqid]
#             des = ''
#             if seqid in description:
#                 des = description[seqid]
#             if len(seq) <= 60:
#                 savefile.write('>'+seqid+' '+des+'\n'+seq+'\n')
#             else:
#                 savefile.write('>'+seqid+' '+des+'\n')
#                 while len(seq) > 60:
#                     savefile.write(seq[:60]+'\n')
#                     seq = seq[60:]
#                 savefile.write(seq+'\n')
#     else:
#         for seqid in fadic:
#             seq = fadic[seqid]
#             des = ''
#             if seqid in description:
#                 des = description[seqid]
#             if len(seq) <= 60:
#                 savefile.write('>'+seqid+' '+des+'\n'+seq+'\n')
#             else:
#                 savefile.write('>'+seqid+' '+des+'\n')
#                 while len(seq) > 60:
#                     savefile.write(seq[:60]+'\n')
#                     seq = seq[60:]
#                 savefile.write(seq+'\n')
#     savefile.close()

def main():
    a = Fasta('aaa.fa', mode='wraa')
    print a.fastaPath
    print a.mode


if __name__ == '__main__':
    main()
