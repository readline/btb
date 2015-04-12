#btb/cancer/integrate
Cancer related tools.


##MuSicSmgSort.R
  * MuSicSmgSort.R [MuSic smg file]
  * Sort the MuSic output smg file with P-value CT then tot muts.
  * Takes only one argument: smg file path
  * Output to [smg path].sorted

---

##Mutation signature
###maf2MutSignature.py
  * maf2MutSignature.py [maf path] [ref fasta path] [bed K3 path] [output prefix]
  * Import a maf file and generate both 1/10 base surrounding mutation base and signature matrix.

###mafSignature2plot.py
  * mafSignature2plot.py [input signature path]
  * Import the signature matrix and plot to png and pdf file.
