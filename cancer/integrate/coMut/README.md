#btb/cancer/integrate/coMut

---

##Mutation signature

---

###maf2MutSignature.py
Import a maf file and generate both 1/10 base surrounding mutation base and signature matrix.
	./maf2MutSignature.py [maf path] [ref fasta path] [bed K3 path] [output prefix]

---

###mafSignature2plot.py
Import the signature matrix and plot to png and pdf file.
	./mafSignature2plot.py [input signature path]

---

##tripplemut2Spectra.py

Import the trimut file produced by maf2MutSignature.py and calculate the spectra info.

	./tripplemut2Spectra.py [tripple mut path] [output prefix]

---

##pattern 10 base

---

###pattern10baseRef.py

Calculate the mutation pattern with both 10 base up/down stream of reference.

	./pattern10baseRef.py [ref fasta path] [ref bed path] [output prefix]

---

