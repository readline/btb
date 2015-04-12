#btb/cancer/integrate/TargetCoverage

---

## Target Coverage Distribution
### bam2TargetCoverage.py
  

    bam2TargetCoverage.py [ref fasta path] [bed path] [blood bam path] [tumor bam path] [output prefix]

  
  * Use both blood and tumor bam to generate each sample's depth of exome sequencing coverage


### TargetExonCovMatrixSorting.R

    ./TargetExonCovMatrixSorting.R [matrix path] [gc path] [output prefix]

Sort the multi sample target coverage matrix.
>1. By sample's average coverage.
2. By target's average coverage.
3. By target's GC%


Input matrix format:

    Sample1       Sample2 ...
    
    0.3   0.98    ...
    
    ...   ...     ...

Input GC format

    GC

    0.54

    0.38

    ...


###  TargetExonCovMatrixPlot.py
Take in the TargetExonCovMatrixSorting.R output sorted matrix and generate a heatmap with GC plot.

    ./TargetExonCovMatrixPlot.py [sorted matrix path]

