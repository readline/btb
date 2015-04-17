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
