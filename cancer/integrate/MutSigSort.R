#!/usr/bin/env Rscript
# MuSicSmgSort.R
# usage: Sort the MuSic output smg file with P-value CT then tot muts.
#        Takes only one argument: smg file path
#        Output to [smg path].sorted
args <- commandArgs(T)
smg <- args[1]

data = read.table(smg,header=T,sep="\t")
data1 = data[with(data,order(q, -n_nonsilent)),] 
#names(data1) <- c("gene","expr","reptime","hic","N_nonsilent","N_silent","N_noncoding","n_nonsilent","n_silent","n_noncoding","nnei","x","X","p","q")
write.table(data1,file=paste(smg,".sorted",sep=""), row.names=F, col.names=T, quote=F, sep="\t")
