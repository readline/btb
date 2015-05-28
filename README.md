# btb
Bio ToolBox

##cancer
Cancer related tools

---

##Fasta.py
A lite weighted module for fasta file import and output.

* class Parse(fastaPath)
        return self.id (list)
        self.seq (dictionary with key in self.id)
        self.des (dictionary with key in self.id)
* func write(fadic, savepath, *orderlist=[default []], *description=[default {}])

---

##grepTsvByCol.py
A grep like tool. Could grep a exactly match or not exactly match column in a line.

    Usage: grepTsvByCol.py [options]

    Options:
      -h, --help            show this help message and exit
      -i INPATH, --input=INPATH
                            Input file path
      -n COLNUM, --columnnum=COLNUM
                            Column number, start from 1
      -t COLTITLE, --columntitle=COLTITLE
                            Column title
      -1, --header          Header is true.[Default=False]
      -o OUTPATH, --output=OUTPATH
                            Output file path
      -e, --exact           Exact match.[Default=False]
      
---

## multithread

Some multithread related tools and examples

---
## refDB

Some tools for database collecting and manipulating

---
## sortMatrix.py

This script can sort a matrix either by row or by column, either in or not in reverse order.
1st column and 1st row must be headers.

```
	Usage: sortMatrix.py [options]
	
	Options:
	  -h, --help            show this help message and exit
	  -i INPATH, --input=INPATH
	                        Input file path
	  -b, --byrow           Sort by row.[Default=False. Default sort by col.]
	  -r, --reverse         Sort in reverse order.[Default=False]
	  -o OUTPATH, --output=OUTPATH
	                        Output file path
```

---
## sortCols.py 

A small tool for soring a table.

The table could have a header line or not, but first column in a line must be a row title.
In this version, first column must be row title, and other values in the row must be int or float.

```
Usage: sortCols.py [options]

Options:
  -h, --help            show this help message and exit
  -i INPATH, --input=INPATH
                        Input table path
  -o OUTPATH, --output=OUTPATH
                        Output table path
  -c COL, --col=COL     Sort with col order. If want to sort by multiple
                        columns, separate items with comma. [Example: 5,3,1]
  -r, --reverse         Sort in reverse order?
  -t, --header          Have header line?
```

---
## bwa-pipe.py

#### version 1.0

A automatic pipeline to run bwa-samtools-sortSam pipeline for either single end or paired end data.

```
./bwa-pipe.py -h 
Usage: bwa-pipe.py [options]

Options:
  -h, --help            show this help message and exit
  -1 FILE1, --read1=FILE1
                        Read 1 file.
  -2 FILE2, --read2=FILE2
                        Read 2 file. If not given, run bwa in SE mode.
  -o PREFIX, --prefix=PREFIX
                        Output prefix. [Default=bwa_output]
  -r REF, --ref=REF     Reference fasta path.
  -t THREADS, --threads=THREADS
                        Threads to use. [Default=1]
  -g RG, --rg=RG        Read Group.
  -a OPTION, --option=OPTION
                        Bwa option. [Default="-e 50 -i 15 -q 10"]
```
