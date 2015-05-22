#!/usr/bin/env python
# =============================================================================
# Filename: sortCols.py
# Version: 1.0 
# Author: Kai Yu - finno@live.cn
# https://github.com/readline
# Last modified: 2015-05-22 13:15
# Description: 
#   This script can sort a table by one or more columns, 
#   you can also sort with reverse order.
# =============================================================================
import os,sys
from optparse import OptionParser

def colParser(col):
    colList = []
    for item in col.split(','):
        try:
            colList.append(int(item))
        except:
            sys.exit('%s in column option must be an int!')
    return colList

def importFile(options):
    infile = open(options.inpath,'r')
    count = 0
    fileDic = {}
    if options.header == True:
        headerLine = infile.readline().rstrip()
    else:
        headerLine = ''
    fileDic['header'] = headerLine.split('\t')
    while 1:
        line = infile.readline()
        if not line: break
        c = line.rstrip().split('\t')
        fileDic[count] = [c[0]] + [float(n) for n in c[1:]]
        count += 1
    infile.close()
    return fileDic


def importFile2MatrixDic(options):
    infile = open(options.inpath,'r')
    matDic = {} 
    if options.header == True:
        headerLine = infile.readline().rstrip()
    else:
        headerLine = ''
    matDic['header'] = headerLine.split('\t')
    count = 0
    while 1:
        line = infile.readline()
        if not line:
            break
        c = line.rstrip('\n').split('\t')
        matDic[count] = c
        count += 1
    infile.close()
    return matDic

def matDic2mat(matDic):
    tmp = []
    for n in range(len(matDic)-1):
        tmp.append([n] + [float(n) for n in matDic[n][1:]])
    return tmp


def sortMatrix(mat,options):
    colList = colParser(options.col)
    cmd = 'newmat = sorted(mat, key=lambda x:(%s), reverse=%s)' %(','.join(['x[%d]'%n for n in colList]),str(options.reverse))
    exec cmd
    return newmat


def main():
    parser = OptionParser(usage="usage: %prog [options]")
    parser.add_option("-i", "--input", dest="inpath", help="Input table path")
    parser.add_option("-o", "--output", dest="outpath", help="Output table path")
    parser.add_option("-c", "--col", dest="col", help="Sort with col order. If want to sort by multiple columns, separate items with comma. [Example: 5,3,1]")
    parser.add_option("-r", "--reverse", dest="reverse", action="store_true", default=False, help="Sort in reverse order?")
    parser.add_option("-t", "--header", dest="header", action="store_true",default=False, help="Have header line?")
    (options, args) = parser.parse_args()

    if not options.inpath or not options.outpath or not options.col:
        parser.error("Incorrect input option. Use -h to see the detail help infomation.")

    matDic = importFile2MatrixDic(options)
    mat = matDic2mat(matDic)
    sortedMat = sortMatrix(mat, options)
    savefile = open(options.outpath,'w')
    savefile.write('\t'.join(matDic['header'])+'\n')
    for row in sortedMat:
        savefile.write('\t'.join(matDic[row[0]]) + '\n')
    savefile.close()

if __name__ == '__main__':
    main()

    











