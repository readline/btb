#!/usr/bin/env python
# keggAPIdownload.py
# 150417
# Kai Yu
# github.com/readline
##############################################
# Download KEGG data by API

import urllib2
import os, sys, gzip

data = urllib2.urlopen('http://rest.kegg.jp/list/genome')


class AAseq(object):
    '''Get KEGG AA seq. 2 arg required. 
    1st arg could be organism code, genome ID with "T" start, or "ko" for all genomes.
    2nd arg should be the output path'''
    def __init__(self,org,outpath):
        self.org = org
        if os.path.exists(outpath):
            rewritetmp = raw_input('Output path %s exists, "Y" for over write; "N" for quit!').upper()
            if rewritetmp == 'Y':
                pass
            elif rewritetmp == 'N':
                sys.exit('Abort!')
            else:
                sys.exit('Incorrect option, abort!')
        self.outpath = outpath

        def getGenomeList(self):
            url = 'http://rest.kegg.jp/list/genome'
            try:
                response = urllib2.urlopen(url)
            except:
                sys.exit('%s API connect error, abort!'%url)
            self.genomeC2T = {}
            self.genomeTnum = []
            while 1:
                line = response.readline()
                if not line: break
                c = line.rstrip().split('\t')
                t = c[0].split(':')[1]
                self.genomeTnum.append(t)
                if '; ' not in c[1]:
                    continue
                self.genomeC2T[c[1].split(',')[0]] = t

        def isOrgTure(self):
            if self.org in self.genomeC2T:
                return [self.genomeC2T[self.org]]
            elif self.org in self.genomeTnum:
                return [self.org]
            elif self.org == 'ko':
                return self.genomeTnum
            return False

        def getSeqList(self):
            self.seqList = []
            for org in self.orgList:
                print 'Fetch %s protein list.'%org
                url = 'http://rest.kegg.jp/list/%s' %org
                try:
                    response = urllib2.urlopen(url)
                except:
                    sys.exit('%s API connect error, abort!'%url)
                while 1:
                    line = response.readline()
                    if not line: break
                    self.seqList.append(line.rstrip().split('\t')[0])

        def makeURL(self):
            self.url = []
            for seqid in self.seqList:
                url = 'http://rest.kegg.jp/get/%s/aaseq'%seqid
                self.url.append(url)
            

        



def main():
    K = AAseq('hsa','hsa.fa')
    


if __name__ == '__main__':
    main()
        


