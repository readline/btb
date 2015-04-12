#!/usr/bin/env Rscript
# TargetExonCovMatrixSorting.R 
# 150412
# Kai Yu
# github.com/readline
#############################################################
# ./TargetExonCovMatrixSorting.R [matrix path] [gc path] [output prefix]
#
# Sort the multi sample target coverage matrix.
# 1. By sample's average coverage.
# 2. By target's average coverage.
# 3. By target's GC%
# Input matrix format:
# Sample1	Sample2	...
# 0.3	0.98	...
# ...	...	...
#
# Input GC format
# GC
# 0.54
# 0.38
# ...

library('gplots')
library(ape)
args = commandArgs(T)
matpath = args[1]
gcpath = args[2]
prefix = args[3]
# matpath="All.1504.cov"
# gcpath="All.1504.gc"
# prefix="test"
print('Import matrix...')
data <- read.table(matpath,header=T,sep="\t")
print('Import GC...')
gcdata<-read.table(gcpath,header=T,sep="\t")
rawrow = length(rownames(data))
rawcol = length(colnames(data))

print('Merge matrix and GC...')
data <- cbind(data,gcdata$GC)

print('Calc sample\'s avg value...')
for (i in 1:rawcol){
    data['avg',i] <- mean(as.matrix(data[1:rawrow,i]))
}
print('Calc targets\' avg value...')
for (i in 1:rawrow){
    data[i,'avg'] <- mean(as.matrix(data[i,1:rawcol]))
}

# sort by sample
print('Sort samples...')
data_s1 <- data[order(data['avg',])]
# write.table(t(data_s1),file=paste(prefix,'.samplesorted.matrix',sep=""),quote=F,sep="\t")
# sort by -(roi avg) and -(roi gc) 
print('Sort targets...')
data_s2 <- data_s1[order(-data_s1[1:rawrow,'avg'],-data_s1[1:rawrow,'gcdata$GC']),]
# write.table(data_s2,file=paste(prefix,'.roisorted.matrix',sep=""),quote=F,sep="\t")
data <- data_s2[1:rawrow,1:(rawcol+1)]
colnames(data)[length(colnames(data))] <- 'GC'
print('Write table...')
write.table(data,file=paste(prefix,'.sorted.matrix',sep=""),row.names=F,quote=F,sep="\t")

# print('Plot heatmap...')
# myheatcol=colorRampPalette(c("#1000af", "#ffffff"))(n = 128)
# tmp_data <- as.matrix(data[,1:rawcol])
# png(paste(prefix,".png",sep=""),width=800,height=800)
# heatmap.2(tmp_data, dendrogram='none', col=myheatcol, scale="none", trace="none", 
#     key=FALSE,labRow=NA)
# dev.off()
