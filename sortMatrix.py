#!/usr/bin/env python
# =============================================================================
# Filename: sortMatrix.py
# Version: 1.0 
# Author: Kai Yu - finno@live.cn
# https://github.com/readline
# Last modified: 2015-05-22 15:01
# Description: 
#   This script can sort a matrix either by row or by column, either in or not in reverse order.
#   1st column and 1st row must be headers. 
# =============================================================================
from optparse import OptionParser
import copy,sys

def transpose(m):
    tmpm = []
    for c in range(len(m[0])):
        tmpm.append([])
    for r in range(len(m)):
        for c in range(len(m[0])):
            tmpm[c].append(m[r][c])
    return tmpm

def importFile2mat(options):
    infile = open(options.inpath, 'r')
    tmp = []
    while 1:
        line = infile.readline()
        if not line: break
        tmp.append(line.rstrip().split('\t'))
    infile.close()
    return tmp

def mat2dic(mat):
    tmpdic = {}
    sortableMat = []
    tmpdic['header'] = mat[0]
    count = 0
    for row in mat[1:]:
        tmpdic[count] = row
        sortableMat.append([count] + [float(n) for n in row[1:]])
        count += 1
    return tmpdic, sortableMat

def sortMatrix(mat,options):
    cmd = 'newmat = sorted(mat, key=lambda x:(%s), reverse=%s)' \
          %(','.join(['x[%d]'%n for n in range(1,len(mat[0]))]),str(options.reverse))
    print cmd
    exec cmd
    return newmat

def saveMat(mat, options):
    savefile = open(options.outpath,'w')
    for row in mat:
        savefile.write('\t'.join(row)+'\n')
    savefile.close()

def main():
    parser = OptionParser(usage="usage: %prog [options]")
    parser.add_option("-i", "--input", dest="inpath",help="Input file path")
    parser.add_option("-b", "--byrow", action="store_true", dest="byrow", default = False, help="Sort by row.[Default=False. Default sort by col.]")
    parser.add_option("-r", "--reverse", action="store_true", dest="reverse", default = False,help="Sort in reverse order.[Default=False]")
    parser.add_option("-o", "--output", dest="outpath", help="Output file path")
    (options, args) = parser.parse_args()

    if not options.inpath or not options.outpath:
        parser.error('Incorrect input option. Use -h to see the help infomation.')

    rawMat = importFile2mat(options)
    
    if options.byrow == True:
        rawMat = transpose(rawMat)
    
    tmpdic, sortableMat = mat2dic(rawMat)
    
    sortedMat = sortMatrix(sortableMat, options)
    
    outMat = []
    outMat.append(tmpdic['header'])
    
    for n in sortedMat:
        outMat.append(tmpdic[n[0]])

    if options.byrow == True:
        outMat = transpose(outMat)

    saveMat(outMat, options)
    
if __name__ == '__main__':
    main()


