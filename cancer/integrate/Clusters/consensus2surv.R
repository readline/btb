#!/usr/bin/env Rscript
library(survival)
argv <- commandArgs(T)
grouppath <- argv[1]
prefix <- argv[2]

data <- read.table(grouppath,header=T,row.names=1,sep='\t')
osdata <- read.table('/home/yukai/yukai/project/glioma/STARfusion/99.Integrate/00.samples/OS.rna319.tsv',header=T,row.names=1,sep='\t')
osdata2 <- osdata
osdata2$OS <- osdata$OS/30
colnames(osdata2) <- c('Surv_month','Status')
Group <- data[rownames(osdata2),]
osdata2 <- cbind(osdata2,Group)
osdata2 <- na.omit(osdata2)
fit <- survfit(Surv(Surv_month, Status) ~ Group, data=osdata2)
diff <- survdiff(Surv(Surv_month, Status) ~ Group, data=osdata2)
p.value <- round(1-pchisq(diff$chi,df=1),4)
sub.text <- paste("p =",p.value)

color10=c('#454553','#FFDE7D','#4AA0D5','#5E1043','#00B8A9','#EB586F','#8D6EC8','#FF895D','#83FFE1','#5BE7A9')
color=color10[1:length(osdata2$Group[!duplicated(osdata2$Group)])]
groups = osdata2$Group[!duplicated(osdata2$Group)]
groups = as.character(groups[order(groups)])

pdf(paste(prefix,'pdf',sep='.'),width=6,height=6)
plot(fit,xlab="Time (Months)",ylab="Survival Probability",main="Survival Curve",col=color,lty=1,lwd=4)
legend("topright",groups,col=color,lty=1,lwd=5)
legend(0.5,0.15,legend=c(sub.text),bty="n",col=1,cex=1)
dev.off()

png(paste(prefix,'png',sep='.'),width=500,height=500)
plot(fit,xlab="Time (Months)",ylab="Survival Probability",main="Survival Curve",col=color,lty=1,lwd=4)
legend("topright",paste('Group',groups,sep=' '),col=color,lty=1,lwd=5)
legend(0.5,0.15,legend=c(sub.text),bty="n",col=1,cex=1.6)
dev.off()
write.table(osdata2,paste(prefix,'surv',sep='.'),quote=F,row.names=T,col.names=T,sep='\t')
write(p.value,paste(prefix,'pvalue',sep='.'))
