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
