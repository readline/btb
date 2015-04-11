#btb/cancer/integrate
Cancer related tools.

##bam2TargetCoverage.py
  * bam2TargetCoverage.py [ref fasta path] [bed path] [blood bam path] [tumor bam path] [output prefix]
  
  * Use both blood and tumor bam to generate each sample's depth of exome sequencing coverage

##MuSicSmgSort.R
  * MuSicSmgSort.R [MuSic smg file]
  * Sort the MuSic output smg file with P-value CT then tot muts.
  * Takes only one argument: smg file path
  * Output to [smg path].sorted

##Mutation signature
###maf2MutSignature.py
  * maf2MutSignature.py [maf path] [ref fasta path] [bed K3 path] [output prefix]
  * Import a maf file and generate both 1/10 base surrounding mutation base and signature matrix.
###mafSignature2plot.py
  * mafSignature2plot.py [input signature path]
  * Import the signature matrix and plot to png and pdf file.