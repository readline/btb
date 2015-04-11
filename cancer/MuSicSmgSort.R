#!/usr/bin/env Rscript
# MuSicSmgSort.R
# usage: Sort the MuSic output smg file with P-value CT then tot muts.
#        Takes only one argument: smg file path
#        Output to [smg path].sorted
args <- commandArgs(T)
smg <- args[1]

data = read.table(smg)
data1 = data[with(data,order(V9, -V4)),]
names(data1) <- c("Gene","Indels","SNVs","Tot Muts","Covd Bps","Muts pMbp","P-value FCPT","P-value LRT","P-value CT","FDR FCPT","FDR LRT","FDR CT")
write.table(data1,file=paste(smg,".sorted",sep=""), row.names=F, col.names=T, quote=F, sep="\t")