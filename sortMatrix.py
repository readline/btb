#!/usr/bin/env python
# sortMatrix.py
# version 1.0
# Kai Yu
# github.com/readline
# 150504
##############################################
from optparse import OptionParser
import copy,sys

def splitContinuousList(tmplist):
    l = []
    tmp = []
    for n in range(len(tmplist)-1):
        tmp.append(tmplist[n])
        if tmplist[n][1] != tmplist[n+1][1]:
            l.append(tmp)
            tmp = []
    tmp.append(tmplist[len(tmplist)-1])
    l.append(tmp)
    return l

def transpose(m):
    tmpm = []
    for c in range(len(m[0])):
        tmpm.append([])
    for r in range(len(m)):
        for c in range(len(m[0])):
            tmpm[c].append(m[r][c])
    return tmpm

def sortMatrix(m, reverse=False, bycol=True):
    if bycol == False:
        m = transpose(m)

    row = 0
    tmprow = m[row]

    s0 = [[(n, m[row][n]) for n in range(len(m[row]))]]
    while 1:
        s0copy = copy.deepcopy(s0)
        s0 = []
        for sublist in s0copy:
            sublist = [(x[0],m[row][x[0]]) for x in sublist]
            s1 = sorted(sublist, lambda x,y: cmp(x[1],y[1]), reverse=reverse)
            s2 = splitContinuousList(s1)
            for item in s2:
                s0.append(item)
        row += 1
        if row >= len(m):
            break
    result = []
    for item in s0:
        for single in item:
            result.append(single[0])
    new = []
    for row in m:
        new.append([row[x] for x in result])

    if bycol == False:
        new = transpose(new)
    return new,result

def main():
    parser = OptionParser(usage="usage: %prog [options]")
    parser.add_option("-i", "--input", dest="inpath",help="Input file path")
    parser.add_option("-b", "--byrow", action="store_false", dest="byrow", default = True,help="Sort by row.[Default=False. Default sort by col.]")
    parser.add_option("-r", "--reverse", action="store_true", dest="reverse", default = False,help="Sort in reverse order.[Default=False]")
    parser.add_option("-o", "--output", dest="outpath", help="Output file path")
    (options, args) = parser.parse_args()
    # print len()

    if not options.inpath or not options.outpath:
        parser.error('Incorrect input option. Use -h to see the help infomation.')

    infile = open(options.inpath,'r')
    headerc = infile.readline().rstrip().split('\t')
    colnamelist = headerc[1:]

    rownamelist = []
    m = []
    while 1:
        line = infile.readline().rstrip()
        if not line: break
        c = line.split('\t')
        rownamelist.append(c[0])
        m.append(c[1:])
    infile.close()
    # for r in m:
    #     print r

    new, order = sortMatrix(m, reverse=options.reverse, bycol=options.byrow)
    if options.byrow == True:
        tmplist = [colnamelist[n] for n in order]
        colnamelist = tmplist
    else:
        tmplist = [rownamelist[n] for n in order]
        rownamelist = tmplist


    savefile = open(options.outpath,'w')
    savefile.write(headerc[0]+'\t'+'\t'.join(colnamelist)+'\n')
    for n in range(len(new)):
        savefile.write(rownamelist[n]+'\t'+'\t'.join(new[n])+'\n')
    savefile.close()

if __name__ == '__main__':
    main()


