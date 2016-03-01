#!/usr/bin/env Rscript
# =============================================================================
# Filename: clusterGroupFpkmTests.Rscript
# Version: 
# Author: Kai Yu - finno@live.cn
# https://github.com/readline
# Last modified: 2016-01-24 16:41
# Description: 
# 
# =============================================================================
library(parallel)
argv <- commandArgs(T)
matrixpath <- argv[1]
clusterpath<- argv[2]
test <- argv[3]
prefix <- argv[4]

print('Load expression matrix')
exp_data <- read.table(file=matrixpath, sep='\t', header=T, row.names=1)
print('Load group matrix')
group_data <- read.table(file=clusterpath, sep='\t', header=T, row.names=1)
colnames(group_data) <- c('Cluster')

calcTtest <- function(x, group_data) {
    group_data <- as.vector(group_data)
    sample_a <- rownames(group_data)[group_data$Cluster==1]
    sample_b <- rownames(group_data)[group_data$Cluster==0]
    data_a <- as.numeric(x[sample_a])
    data_b <- as.numeric(x[sample_b])
    pvalue <- t.test(data_a, data_b)$p.value
    return(pvalue)
}

calcWilcox <- function(x, group_data) {
    group_data <- as.vector(group_data)
    sample_a <- rownames(group_data)[group_data$Cluster==1]
    sample_b <- rownames(group_data)[group_data$Cluster==0]
    data_a <- as.numeric(x[sample_a])
    data_b <- as.numeric(x[sample_b])
    pvalue <- wilcox.test(data_a, data_b)$p.value
    return(pvalue)
}

calcFc <- function(x, group_data) {
    group_data <- as.vector(group_data)
    sample_a <- rownames(group_data)[group_data$Cluster==1]
    sample_b <- rownames(group_data)[group_data$Cluster==0]
    data_a <- as.numeric(x[sample_a])
    data_b <- as.numeric(x[sample_b])
    med1 <- median(data_a,na.rm=T)
    med2 <- median(data_b,na.rm=T)

    if (med1 >= med2) {
        log2fc = log2((med1+1)/(med2+1))
    } else {
        log2fc = log2((med2+1)/(med1+1)) * -1
    }
    return(log2fc)
}

if (test=='t.test'){
    usetest <- calcTtest
    print('Using T-test')
} else {
    usetest <- calcWilcox
    print('Using Wilcox-test')
}



cl.cores <- detectCores()
cl <- makeCluster(cl.cores)

out <- c()

#apply(exp_data, 1, usetest, group_data)

t_pvalue <- parApply(cl=cl, exp_data, 1, usetest, group_data)
t_qvalue <- p.adjust(t_pvalue, method='BH', n=length(t_pvalue))
t_diff <- parApply(cl=cl, exp_data, 1, calcFc, group_data)
tmpout <- cbind(t_pvalue, t_qvalue, t_diff)
colnames(tmpout) <- c('pvalue', 'fdr', 'log2fc')
rownames(tmpout) <- rownames(exp_data)
out <- rbind(out, tmpout)

#orderout <- out[order(out[,'pvalue']),]
#orderout <- out[abs(out[,'log2fc'])>=1,]

out <- out[which(abs(out[,'log2fc'])>2),]
#out <- out[order(out[,'fdr']),]
out <- out[order(out[,'pvalue']),]
out <- out[which(out[,'pvalue']<0.01),]
out <- out[which(out[,'fdr']<0.1),]

#out <- out[-which(apply(out,2,function(x)all(is.na(x)))), -which(apply(out,4,function(x)all(is.na(x))))]

write.table(out, prefix, sep='\t', quote=F, row.name=T, col.name=T)
