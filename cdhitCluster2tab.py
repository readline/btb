#!/usr/bin/env python
# =============================================================================
# Filename: cdhitCluster2tab.py
# Version: 
# Author: Kai Yu - finno@live.cn
# https://github.com/readline
# Last modified: 2015-06-20 18:11
# Description: 
# 
# =============================================================================
import os, sys
def main():
    try:
        clusterPath = sys.argv[1]
    except:
        sys.exit(sys.argv[0] + ' [cdhit clstr path]')

    infile = open(clusterPath, 'r')
    clstdic = {}
    clstorder = []

    while 1:
        line = infile.readline()
        if not line:
            break

        if line[0] == '>':
            clstid = line.rstrip()[1:].replace(' ', '_')
            clstdic[clstid] = {}
            clstorder.append(clstid)
            continue
        c = line.rstrip().split()
        if c[-1] == '*':
            clstdic[clstid]['master'] = [c[1][:-3], c[2][1:-3]]
        else:
            clstdic[clstid][c[0]] = [c[1][:-3], c[2][1:-3], c[-1]]

    infile.close()

    savefile = open(clusterPath + '.tab', 'w')
    savefile.write('#Transcript\tClusterID\tClusterHead\tHeadLength\tTranscriptLength\tChainRelationship\tIdentity\n')
    for clstid in clstorder:
        for itemid in clstdic[clstid]:
            if itemid == 'master':
                tmp = [clstdic[clstid]['master'][1],
                       clstid,
                       clstdic[clstid]['master'][1],
                       clstdic[clstid]['master'][0],
                       clstdic[clstid]['master'][0],
                       '*',
                       '*'
                        ]
                savefile.write('\t'.join(tmp) + '\n')
                continue
            item = clstdic[clstid][itemid]
            tmp = [item[1],
                   clstid,
                   clstdic[clstid]['master'][1],
                   clstdic[clstid]['master'][0],
                   item[0],
                   item[2][:-1].replace('/', '\t')]
            savefile.write('\t'.join(tmp) + '\n')
    savefile.close()

if __name__ == '__main__':
    main()
