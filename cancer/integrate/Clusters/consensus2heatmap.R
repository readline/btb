library('gplots')
argv <- commandArgs(T)
matrixpath <- argv[1]
grouppath <- argv[2]
prefix <- argv[3]

raw_data = read.table(matrixpath,header=T,sep="\t",row.names=1)
group<-read.table(grouppath,row.names=1,header=T, sep='\t')
data <- raw_data[,rownames(group)]
data = log2(data+1);
data = as.matrix(data);
data = t(scale(t(data), scale=F));
#sample_dist = dist(t(data),method='euclidean');
#hc_samples = hclust(sample_dist, method='complete');
gene_dist = dist(data, method='euclidean');
hc_genes = hclust(gene_dist, method='complete');
ordered_genes = data[hc_genes$order,];

groupcol <- group[colnames(data),'Cluster']
groupcol[which(groupcol==1)]<-'#454553'
groupcol[which(groupcol==2)]<-'#FFDE7D'
groupcol[which(groupcol==3)]<-'#4AA0D5'
groupcol[which(groupcol==4)]<-'#5E1043'
groupcol[which(groupcol==5)]<-'#00B8A9'
groupcol[which(groupcol==6)]<-'#EB586F'
groupcol[which(groupcol==7)]<-'#8D6EC8'
groupcol[which(groupcol==8)]<-'#FF895D'
groupcol[which(groupcol==9)]<-'#83FFE1'
groupcol[which(groupcol==10)]<-'#5BE7A9'
write.table(ordered_genes, file=paste(prefix,"log2.centered.ordered.dat",sep='.'), quote=F, sep='\t');
tmp_data1 <- data;
myheatcol=bluered(75);
pdf(paste(prefix,'pdf',sep='.'),width=8,height=12);
heatmap.2(tmp_data1, dendrogram='row',main=prefix, Rowv=as.dendrogram(hc_genes),Colv=F, col=myheatcol, scale="row", density.info="histogram", trace="none", key=TRUE, keysize=1.2, margins=c(18,10),key.par=list(pin=c(1,0.5),mai=c(0.75,0.5,0.5,0)), cex.main=0.5,ColSideColors=groupcol);
dev.off();
png(paste(prefix,'png',sep='.'),width=800,height=1200);
heatmap.2(tmp_data1, dendrogram='row',main=prefix, Rowv=as.dendrogram(hc_genes),Colv=F, col=myheatcol, scale="row", density.info="histogram", trace="none", key=TRUE, keysize=1.2, margins=c(18,10),key.par=list(pin=c(1,0.5),mai=c(0.75,0.5,0.5,0)), cex.main=0.5,ColSideColors=groupcol);
dev.off();
