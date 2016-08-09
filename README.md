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
three NCBI resources:

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
  * approx. 25 GB of disk space (preferentially on a fast drive)
  * needed python package: sqlite3 
  
  Python packages are installed easily using ```pip```. Under Debian-based (e.g. Ubuntu, Debian, Mint) and Red Hat-based (e.g. Red Hat, Centos) systems, ``` pip ``` is availbale from public repositories: ```apt-get install python-pip ``` (Debian-based systems) ``` yum -y install python-pip ``` (Red Hat-based systems).

  Install sqlite3 (pip): ```pip install sqlite3```
  

2. Resources needed from NCBI:
 
  Download the following files and extract them.


  * ftp://ftp.ncbi.nih.gov/pub/taxonomy/taxdmp.zip
  * ftp://ftp.ncbi.nih.gov/pub/taxonomy/accession2taxid/prot.accession2taxid.gz
  * ftp://ftp.ncbi.nih.gov/genomes/ASSEMBLY_REPORTS/assembly_summary_refseq.txt

  taxdmp.zip contains a bunch of files, we only need two of them: paths.dmp and nodes.dmp, which hold the whole NCBI taxonomy. prot.accession2taxid.gz includes accession version number mappings for all protein sequences deposited in NCBI nr, and assembly_summary_refseq.txt is a list of all deposited and annotated genomes in NCBI including respective taxonomic identifiiers.

3. The heart of taxomias will be a cross-mapped NCBI taxonomy database stored in a sqlite3 database.
   To setup our database execute the following commands on the command-line. Taxomias expects the NCBI taxonomy to be in the same directory.
   NOTE: The import of the accession version number mappings takes a while - be patient.

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

4. What is still missing is the underlying NCBI taxonomy database and the mapping of taxonomic identifiiers to available      genomes. To set up this two components of taxomias we will use the ``` setup_taxomias.py ``` and call it as follows:
NOTE: The import of the remaning resources takes again a while.

  ``` shell
  python setup_taxomias.py names.dmp nodes.dmp assembly_summary_refseq.txt ncbi_taxonomy.db
  ```
  After this step our NCBI taxonomy database contains three tables: acc_taxid (mappings of accession version numbers and taxonomic identifiiers for all proteins deposited in NCBI nr), tree (the whole NCBI taxonomy as hierarchical table) and genomes (mappings of taxonomic identifiiers to availabl refseq genomes). The previously imported files are not longer necessary and can be deleted to save disk space. With that our database is ready to be used. To check its integrity we do a little example:
  
  ``` shell
  sqlite ncbi_taxonomy.db
  SELECT taxid FROM tree WHERE name = "Acidobacterium capsulatum":
  ```
  
  The prompt will return 33075, which is the unique taxonomic identifiier for _Acidobacterium capsulatum_. Taxomias contains a bunch of functions which allows us to easily access our locally stored taxonomy database and to process taxonomic information with respect to setup cross references.
  
## Implemented functions

  
  
	
## Credits
The original idea was conceptualized by Sixing Huang (DSMZ, Braunschweig) and most of the original code was written by him. However, NCBI is phasing out GI numbers as identifiiers and links to taxonomic information. 

Therefore the original code was rewritten by me to work with the newly established system of using accession (version) numbers as replacement for GI numbers.

