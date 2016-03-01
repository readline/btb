library('gplots')
argv <- commandArgs(T)
matrixpath <- argv[1]
grouppath <- argv[2]
prefix <- argv[3]

raw_data = read.table(matrixpath,header=T,sep="\t",row.names=1)
group<-read.table(grouppath,row.names=1, sep='\t')
colnames(group) <- c('group')
data <- raw_data[,rownames(group)]
data = log2(data+1);
data = as.matrix(data);
data = t(scale(t(data), scale=F));
sample_dist = dist(t(data),method='euclidean');
hc_samples = hclust(sample_dist, method='complete');
gene_dist = dist(data, method='euclidean');
hc_genes = hclust(gene_dist, method='complete');
ordered_genes = data[hc_genes$order,hc_samples$order];

groupcol <- group[colnames(data),'group']
groupcol[which(groupcol==1)]<-'#F2676A'
groupcol[which(groupcol==0)]<-'#ECF0F1'

write.table(ordered_genes, file=paste(prefix,"log2.centered.ordered.dat",sep='.'), quote=F, sep='	');
tmp_data1 <- data;
myheatcol=bluered(75);
pdf(paste(prefix,'pdf',sep='.'),width=8,height=12);
heatmap.2(tmp_data1, dendrogram='both',main=prefix, Rowv=as.dendrogram(hc_genes), Colv=as.dendrogram(hc_samples), col=myheatcol, scale="row", density.info="histogram", trace="none", key=TRUE, keysize=1.2, margins=c(18,10),key.par=list(pin=c(1,0.5),mai=c(0.75,0.5,0.5,0)), cex.main=0.5,ColSideColors=groupcol);
dev.off();
png(paste(prefix,'png',sep='.'),width=800,height=1200);
heatmap.2(tmp_data1, dendrogram='both',main=prefix, Rowv=as.dendrogram(hc_genes), Colv=as.dendrogram(hc_samples), col=myheatcol, scale="row", density.info="histogram", trace="none", key=TRUE, keysize=1.2, margins=c(18,10),key.par=list(pin=c(1,0.5),mai=c(0.75,0.5,0.5,0)), cex.main=0.5,ColSideColors=groupcol);
dev.off();
