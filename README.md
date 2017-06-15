<img src="https://github.com/wegnerce/taxomias/blob/master/logo_taxomias.png" width="250">

# taxomias                                                                     
TAXOMIAS v0.2 June, '17


* Carl-Eric Wegner
* Küsel Lab - Aquatic Geomicrobiology
* Friedrich Schiller University of Jena
* carl-eric.wegner(at)uni-jena.de

## Revision history

v0.2 (June '17)
- bug fix, modification of the routines to retrieve genome data
  revised routines:
  * taxomias.GenomeByTaxid
  * taxomias.AllGenomesByTaxid
- bug fix, revision of the setup procedure for genome path
  to taxid mappings

v0.1 (August '16)
- initial release

## Background

NCBI maintains a well-curated, hierarchical database of known taxonomy. Having 
a local copy of this database in combination with mappings to sequence data deposited
in NCBI comes in quite handy in many situations (see usage scenarios).

TAXOMIAS is a small module written in python (python 2.7).The idea behind TAXOMIAS is to locally 
setup a tailored NCBI taxonomy database in form of an sqlite database and to provide 
wrappers to use taxonomic information to access sequence information. Currently TAXOMIAS 
comprises functions to access two NCBI resources:

1. RefSeq genomes
  * mapping of taxonomic identifiers to available refseq genomes
2. NCBI nr 
  * mapping of taxonomic identifiers to accession version numbers of protein sequences deposited in NCBI nr

## Usage scenarios

1. creation of custom BLAST databases 
  * e.g. collect accession numbers of all bacterial proteins and use these to filter NCBI nr for entries of interest
2. downloading of genomes of interests 
  * e.g. all available phage genomes, either coding gene nucleotide sequences or coding gene protein sequences
3. extracting taxonomic information
  * e.g. collecting taxonomic paths for all Alphaproteobacteris genera to create custom mapping files, for instance for functional gene databases

## Installation (Linux-based systems)

1. Download Taxomias: ``` git clone https://github.com/wegnerce/taxomias.git ```

  Pre-requisites:
  * approx. __25 GB__ of disk space (preferentially on a fast drive)
  * the sqlite3 command-line tool 
  * optional python packages: __biopython__ (primarily needed to execute exemplary code)
  
  Python packages are installed easily using ```pip```. Under Debian-based (e.g. Ubuntu, Debian, Mint) and Red Hat-based (e.g. Red Hat, Centos) systems, ``` pip ``` is availbale from public repositories: ```apt-get install python-pip ``` (Debian-based systems) ``` yum -y install python-pip ``` (Red Hat-based systems).

  The sqlite3 command line tool is shipped with many Linux distributions by default. If necessary it can be installed from respective package repositories (e.g. Debian-based systems):
  ``` apt-get install sqlite3 ``` 
  

2. Resources needed from NCBI:
 
  Download the following files and extract them.


  * ftp://ftp.ncbi.nih.gov/pub/taxonomy/taxdmp.zip
  * ftp://ftp.ncbi.nih.gov/pub/taxonomy/accession2taxid/prot.accession2taxid.gz
  * ftp://ftp.ncbi.nih.gov/genomes/ASSEMBLY_REPORTS/assembly_summary_refseq.txt

  taxdmp.zip contains a bunch of files, we only need two of them: __paths.dmp__ and __nodes.dmp__, which hold the whole NCBI taxonomy. __prot.accession2taxid.gz__ includes accession version number mappings for all protein sequences deposited in NCBI nr, and __assembly_summary_refseq.txt__ is a list of all deposited and annotated genomes in NCBI refseq including respective taxonomic identifiers.

3. The heart of TAXOMIAS will be a cross-mapped NCBI taxonomy database stored in a sqlite3 database.
   To setup our database execute the following commands on the command-line. Taxomias expects the NCBI taxonomy to be in the same directory.
   __NOTE:__ The import of the accession version number mappings takes a while - be patient.

  ``` shell
  sqlite3 ncbi_taxonomy.db
  create table acc_taxid (accession text, accession_version text, taxid integer, gi integer);
  .tables
  .mode list
  .separator \t
  .import prot.accession2taxid acc_taxid 
  CREATE UNIQUE INDEX accvers_idx_on_accvers_taxid ON acc_taxid(accession_version);
  CREATE INDEX taxid_idx_on_accvers_taxid ON acc_taxid(taxid);
  ```

  With these commands we have created a new sqlite3 database object (ncbi_taxonomy.db), a table (acc_taxid) 
  within this object, we have imported the protein sequence to accession version number mappings into acc_taxid and we created
  indices to improve the performance of the sqlite3 database.

4. What is still missing is the underlying NCBI taxonomy database and the mapping of taxonomic identifiers to available      genomes. To set up these two components of TAXOMIAS we will use the ``` setup_taxomias.py ``` script and call it as follows:
__NOTE:__ Again, the import takes a bit of time.

  ``` shell
  python setup_taxomias.py names.dmp nodes.dmp assembly_summary_refseq.txt ncbi_taxonomy.db
  ```
  After this step our NCBI taxonomy database contains three tables: __acc_taxid (mappings of accession version numbers and taxonomic identifiiers for all proteins deposited in NCBI nr)__, __tree (the whole NCBI taxonomy as hierarchical table)__ and __genomes (mappings of taxonomic identifiiers to availabl refseq genomes)__. The previously imported files are not longer necessary and can be deleted to save disk space. With that our database is ready to be used. To check its integrity we do a little example:
  
  ``` shell
  sqlite ncbi_taxonomy.db
  SELECT taxid FROM tree WHERE name = "Acidobacterium capsulatum";
  .exit
  ```
  
  With the first command we connect to our local NCBI taxonomy database (make sure that you indicate the right path). The second command searched the table __tree__ for _Acidobacterium capsulatum_ and returns it taxonomic identifier. The prompt will return 33075, which is the unique identifiier for _Acidobacterium capsulatum_. TAXOMIAS contains a bunch of functions which allows us to easily access our locally stored taxonomy database and to process taxonomic information with respect to setup cross references, see __Implemented functions__ and __Examples__ for details.
  
## Implemented functions
  
  Before we start with having a look at implemented functions we want to tell ``` python ``` where taxomias can be found. In order to do so we create a symbolic link of the folder containing taxomias.py to a location known to your ```$PYTHONPATH``` variable:
  
  ``` shell
  ln -s /your/path/to/taxomias /usr/lib/python2.7/
  ```
  
  Any path listed in your ``` $PYTHONPATH ``` (/usr/lib/python2.7/ is only one example) will do the trick.

### Functions
  
  * taxomias.TaxidByName(taxid)
    
    e.g. ``` taxomias.TaxidByName("Acidobacterium capsulatum") ```
    --> the function will return if possible the respective taxonomic identifier, otherwise it returns "-1"

  * taxomias.RankByTaxid(taxid)
    
    e.g. ``` taxomias.RankByTaxid(33075) ```
    --> the function will return if possible the corresponding rank for instance "genus" or "species", otherwise it returns "no rank"
  
  * taxomias.RankByName("name")
    
    e.g. ``` taxomias.RankByName("Acidobacterium capsulatum") ```
    --> the function will return if possible the corresponding rank for instance "genus" or "species", otherwise it returns "no rank"
  
  * taxomias.NameByTaxid(taxid)
    
    e.g. ``` taxomias.NameByTaxid(33075) ```
    --> returns the name for any valid taxonomic identifier

  * taxomias.ParentByTaxid(taxid)
    
    e.g. ``` taxomias.ParentByTaxid(33075) ```
    --> the function will return the parent of the respective taxonomic group, otherwise it returns "-1"

  * taxomias.ParentByName("name")
    
    e.g. ``` taxomias.ParentByName("Acidobacterium capsulatum") ```
    --> --> the function will return the parent of the respective taxonomic group, otherwise it returns "-1"

  * taxomias.PathByTaxid(taxid)
    
    e.g. ``` taxomias.PathyByTaxid(33075) ```
    --> given a taxonomic identifiier the whole taxonomic path is resolved if possible, otherwise it returns "-1"

  * taxomias.TaxidByAcc(acc.version.number)
    
    e.g. ``` taxomias.TaxidByAcc(AAK58570.1) ```
    --> the function will return if possible the respective taxonomic identifier, otherwise it returns "-1"

  * taxomias.SonsByTaxid(taxid)
    
    e.g. ``` taxomias.SonsByTaxid(33075) ```
    --> the function will look up all sons of a taxonomic group if possible, otherwise it returns "-1"

  * taxomias.AccByTaxid(taxid)
    
    e.g. ``` taxomias.AccByTaxid(33075) ```
    --> looks up all deposited accession version numbers for a given taxonomic identifier, otherwise it returns "-1"

  * taxomias.AllSonsByTaxid(taxid)
    
    e.g. ``` taxomias.AllSonsByTaxid(33075) ```
    --> the function will look up all sons of a taxonomic group if possible, otherwise it returns "-1" __NOTE:__ supports multithreading (default: 4 threads will be used)

  * taxomias.AllAccByTaxid(taxid)
    
    e.g. ``` taxomias.AllAccByTaxid(33075) ```
    --> looks up all deposited accession version numbers for a given taxonomic identifier, otherwise it returns "-1" __NOTE:__ supports multithreading (default: 4 threads will be used)

  * taxomias.GenomeByTaxid(taxid, seq_type)
    
    e.g. ``` taxomias.GenomeByTaxid(240015, "nucl") ```
    --> the function will download the corresponding genome for a given identifier, dependent on whether nucleotide "nucl" or protein "prot" sequences have been specified, either nucleotide or protein sequences of coding genes of the respective genome are downloaded into a new directory named after the given taxonomic identifier

  * taxomias.AllGenomesByTaxid(taxid, seq_type)
    
    e.g. ``` taxomias.AllGenomesByTaxid(33075, "prot") ```
    --> the function will download all genomes of given taxonomic group (e.g. a family or order) using the function ```taxomias.GenomeByTaxid``

## Examples

### Example (1) - Collecting and downloading all Verrucomicrobia genomes

``` python
# Import needed modules
import sqlite3, taxmomias

# Whats the taxonomic idnetifiier of Verrucomicrobia?
print taxomias.TaxidByName("Verrucomicrobia")

# Ah, apparently its 74201, so lets collect all the genomes (protein sequences)
taxomias.AllGenomesByTaxid(74201, "prot")

# That's it, we just collected all available Verrucomicrobia genomes, with three lines of code... ;-)
```

### Example (2) - Filter NCBI nr for archaeal proteins

1. First we need to grab the latest NCBI nr database as .fasta. Download the corresponding file and unpack it

``` shell
wget ftp://ftp.ncbi.nlm.nih.gov/blast/db/FASTA/nr.gz 
gzip -d nr.gz
```

``` python
# Import needed modules
import sqlite3, taxomias
from Bio import SeqIO

# define in- and output files
input_file = "nr.fasta"
output_file = "nr_archaea.fasta"

# What is the taxonomic identifiier for archaea? it's 2157!
print taxomias.TaxidByName("Archaea")

# Write all accession version numbers belonging to archaea into a set,
# sets are faster than lists due to the use of hash tables as underlying
# data structure
wanted = set(taxomias.AllAccByTaxid(2157))

# Filter NCBI nr using the set of archaea accession version numbers
# for the filtering the fasta file is read and the ID of every entry is checked
# for archaeal accessions, every entry looks roughly as follows:
# >gi|2340931|emb|CAA74950.1| hypothetical protein [Methanosarcina mazei]
# MQAFYNLNISHVHVPDKDFNRSTFYSIIGAEFFADPAAFAFKQVYLVRDAVFLADCFMWA
# the accession versiom number is the last part of the id (>gi|2340931|emb|CAA74950.1|),
# in this case: CAA74950.1
records = (r for r in SeqIO.parse(input_file, "fasta") if r.id.split("|")[3] in wanted)
count = SeqIO.write(records, output_file, "fasta")
print "Saved %i records from %s to %s" % (count, input_file, output_file)

# That's it, again only few lines of code are needed
```

  
## Credits
The original code was written by Sixing Huang (DSMZ, Braunschweig, Germany) and published on his blog (http://dgg32.blogspot.de/) in 2013. In the beginning of 2016 NCBI decided to phase out GI numbers. I used Sixing's code a lot and decided to modify it to make it work with NCBI's new system of taxonomy mappings based on accession version numbers.

In addition I added functions to easily access refseq genomes based on taxonomic information.
