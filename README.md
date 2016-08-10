# taxomias                                                                     
TAXOMIAS v0.1 August, '16


* Carl-Eric Wegner
* Küsel Lab - Aquatic Geomicrobiology
* Friedrich Schiller University of Jena
* carl-eric.wegner(at)uni-jena.de

## Background

NCBI maintains a well-curated, hierarchical database of known taxonomy. Having 
a local copy of this database in combination with mappings to sequence data deposited
in NCBI comes in quite handy in many situations (see usage scenarios).

The idea behind TAXOMIAS is to locally setup a tailored NCBI taxonomy database
in form of an sqlite database and to provide wrappers to use taxonomic information
to access sequence information. Currently taxomias comprises functions to access
two NCBI resources:

1. RefSeq genomes
  * mapping of taxonomic identifiiers to available refseq genomes
2. NCBI nr 
  * mapping of taxonomic identifiiers to accession version numbers of protein deposited in NCBI nr

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

  taxdmp.zip contains a bunch of files, we only need two of them: __paths.dmp__ and __nodes.dmp__, which hold the whole NCBI taxonomy. __prot.accession2taxid.gz__ includes accession version number mappings for all protein sequences deposited in NCBI nr, and __assembly_summary_refseq.txt__ is a list of all deposited and annotated genomes in NCBI including respective taxonomic identifiiers.

3. The heart of taxomias will be a cross-mapped NCBI taxonomy database stored in a sqlite3 database.
   To setup our database execute the following commands on the command-line. Taxomias expects the NCBI taxonomy to be in the same directory.
   __NOTE:__ The import of the accession version number mappings takes a while - be patient.

  ``` shell
  sqlite3 ncbi_taxonomy.db
  create table acc_taxid (accession text, accession_version text, taxid integer, gi integer);
  .tables
  .mode list
  .import prot.accession2taxid acc_taxid 
  CREATE UNIQUE INDEX accvers_idx_on_accvers_taxid ON acc_taxid(accession_version);
  CREATE INDEX taxid_idx_on_accvers_taxid ON acc_taxid(taxid);
  ```

  With these commands we have created a new sqlite3 database object (ncbi_taxonomy.db), a table (acc_taxid) 
  within this object, we have imported the protein sequence to accession version number mappings into acc_taxid and we created
  indices to improve the performance of the sqlite3 database.

4. What is still missing is the underlying NCBI taxonomy database and the mapping of taxonomic identifiiers to available      genomes. To set up these two components of taxomias we will use the ``` setup_taxomias.py ``` and call it as follows:
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
  
  The prompt will return 33075, which is the unique taxonomic identifiier for _Acidobacterium capsulatum_. Taxomias contains a bunch of functions which allows us to easily access our locally stored taxonomy database and to process taxonomic information with respect to setup cross references, see __Implemented functions__ and __Examples__ for details.
  
## Implemented functions
  
  Before we start with having a look at implemented functions we want to tell ``` python ``` where taxomias can be found. In order to do so we create a symbolic link:
  
  ``` shell
  ln -s /your/path/to/taxomias /usr/lib/python2.7/
  ```
  
  Any path listed in your ``` $PYTHONPATH ``` will do the trick.

### Functions
  
  * taxomias.TaxidByName(taxid)
    
    e.g. ``` taxomias.TaxidByName("Acidobacterium capsulatum") ```
    --> the function will return if possible the respective taxonomic identifiier, otherwise it returns "-1"

  * taxomias.RankByTaxid(taxid)
    
    e.g. ``` taxomias.RankByTaxid(33075) ```
    --> the function will return if possible the corresponding rank for instance "genus" or "species", otherwise it returns "no rank"
  
  * taxomias.RankByName("name")
    
    e.g. ``` taxomias.RankByName("Acidobacterium capsulatum") ```
    --> the function will return if possible the corresponding rank for instance "genus" or "species", otherwise it returns "no rank"
  
  * taxomias.NameByTaxid(taxid)
    
    e.g. ``` taxomias.NameByTaxid(33075) ```
    --> returns the name for any valid taxonomic identifiier

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
    --> the function will return if possible the respective taxonomic identifiier, otherwise it returns "-1"

  * taxomias.SonsByTaxid(taxid)
    
    e.g. ``` taxomias.SonsByTaxid(33075) ```
    --> the function will look up all sons of a taxonomic group if possible, otherwise it returns "-1"

  * taxomias.AccByTaxid(taxid)
    
    e.g. ``` taxomias.AccByTaxid(33075) ```
    --> looks up all deposited accession version numbers for a given taxonomic identifiier, otherwise it returns "-1"

  * taxomias.AllSonsByTaxid(taxid)
    
    e.g. ``` taxomias.AllSonsByTaxid(33075) ```
    --> the function will look up all sons of a taxonomic group if possible, otherwise it returns "-1" __NOTE:__ supports multithreading (default: 4 threads will be used)

  * taxomias.AllAccByTaxid(taxid)
    
    e.g. ``` taxomias.AllAccByTaxid(33075) ```
    --> looks up all deposited accession version numbers for a given taxonomic identifiier, otherwise it returns "-1" __NOTE:__ supports multithreading (default: 4 threads will be used)

  * taxomias.GenomeByTaxid(taxid, seq_type)
    
    e.g. ``` taxomias.GenomeByTaxid(240015, "nucl") ```
    --> the function will download the corresponding genome for a given identifiier, dependent on whether nucleotide "nucl" or protein "prot" sequences have been specified, either nucleotide or protein sequences of coding genes of the respective genome are downloaded into a new directory named after the given taxonomic identifiier

  * taxomias.AllGenomesByTaxid(taxid, seq_type)
    
    e.g. ``` taxomias.AllGenomesByTaxid(33075, "prot") ```
    --> the function will download all genomes of given taxonomic group (e.g. a family or order) using the function ```taxomias.GenomeByTaxid``

  
## Credits
The original idea was conceptualized by Sixing Huang (DSMZ, Braunschweig) and most of the original code was written by him. However, NCBI is phasing out GI numbers as identifiiers and links to taxonomic information. 

Therefore the original code was rewritten by me to work with the newly established system of using accession (version) numbers as replacement for GI numbers.

