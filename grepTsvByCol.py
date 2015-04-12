#!/usr/bin/env python
import os,sys
from optparse import OptionParser
def main():
    parser = OptionParser(usage="usage: %prog [options]")
    parser.add_option("-i", "--input", dest="inpath",help="Input file path")
    parser.add_option("-n", "--columnnum", type="int", dest="colnum", help="Column number, start from 1")
    parser.add_option("-t", "--columntitle", dest="coltitle", help="Column title")
    parser.add_option("-1", "--header", action="store_true", dest="header", default = False,help="Header is true.[Default=False]")
    parser.add_option("-o", "--output", dest="outpath", help="Output file path")
    parser.add_option("-e", "--exact", action="store_true", dest="exact", default = False,help="Exact match.[Default=False]")

    (options, args) = parser.parse_args()
    if not options.inpath:
        parser.error("Argument -i not given") 
    elif options.colnum and options.coltitle:
        parser.error("options -n and -t art exclusive")
    elif options.colnum == None and options.coltitle == None:
        parser.error("There should be at least one of argument -n and -t")
    elif options.coltitle and options.header != True:
        parser.error("Argument -t requires argument -1")

    if len(options.inpath) >=3 and options.inpath[-3:] == '.gz':
        import gzip
        infile = gzip.open(options.inpath, 'rb')
    else:
        infile = open(options.inpath, 'r')

    if options.outpath:
        savefile = open(options.outpath,'w')
    if options.header == True:
        header = infile.readline().rstrip('\n').split('\t')
        if options.outpath:
            savefile.write('\t'.join(header) + '\n')
        else:
            print '\t'.join(header)
        if options.coltitle:
            col = -1
            for n in range(0,len(header)):
                if header[n] == options.coltitle:
                    col = n
                    break
            if col == -1:
                print 'Can not find column title %s in the header line!' %(options.coltitle)
                sys.exit()
        elif options.colnum:
            if options.colnum -1 >= len(header):
                print 'Column number %d exceed max column number' %(options.colnum)
                sys.exit()
            else:
                col = options.colnum - 1
    else:
        col = options.colnum -1
    while 1:
        line = infile.readline()
        if not line: break
        c = line.rstrip('\n').split('\t')
        if col < len(c):
            for key in args:
                if options.exact == False and key in c[col]:
                    if options.outpath:
                        savefile.write(line)
                    else:
                        print line.rstrip('\n')
                    break
                elif options.exact == True and key == c[col]:
                    if options.outpath:
                        savefile.write(line)
                    else:
                        print line.rstrip('\n')
                    break
        else:
            print 'Column number %d exceed max column number' %(col+1)
            sys.exit()
    if options.outpath:
        savefile.close()
    infile.close()






if __name__ == '__main__':
    main()