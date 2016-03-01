#!/usr/bin/env Rscript
argv <- commandArgs(T)
matrixpath <- argv[1]
gene <- argv[2]
prefix <- argv[3]

data <- read.table(matrixpath, header=T,row.names=1,sep='\t')
query <- as.numeric(data[gene,])
plist <- c()
clist <- c()

for (i in 1:nrow(data)){
  target <- as.numeric(data[i,])
  result <- cor.test(query,target,method='pearson')
  plist <- rbind(plist,result$p.value)
  clist <- rbind(clist,result$estimate)
}
tmp <- cbind(plist,clist)
colnames(tmp)<- c('pvalue','cor')
rownames(tmp)<- rownames(data)
tmp <- na.omit(tmp)
tmpordered <- tmp[order(tmp[,'pvalue']),]
plist <- tmpordered[,'pvalue']
fdr <- p.adjust(plist, method='BH', n=length(plist))
tmpordered<- cbind(tmpordered,fdr)
tmpfilt <- tmpordered
tmpfilt <- tmpfilt[which(tmpfilt[,'pvalue']<0.01),]
tmpfilt <- tmpfilt[which(tmpfilt[,'fdr']<0.1),]
tmpfilt <- tmpfilt[order(tmpfilt[,'fdr']),]
write.table(tmpfilt,paste(prefix,'cor.tsv',sep='.'),quote=F,row.names=T,col.names=T,sep='\t')
