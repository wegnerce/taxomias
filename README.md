# taxomias                                                                     
TAXOMIAS v0.1 August, '16


* Carl-Eric Wegner
* Küsel Lab - Aquatic Geomicrobiology
* Friedrich Schiller University of Jena
* carl-eric.wegner(at)uni-jena.de

## Background

NCBI maintains a well-curated, hierarchical database of known taxonomy. Having 
a local copy of this database in combination with mappings to sequence data deposited
in NCBI comes in quite handy in many situations.

The idea behind TAXOMIAS is to locally setup a tailored NCBI taxonomy database
in form of an sqlite database and to provide wrappers to use taxonomic information
to access sequence information. Currently taxomias comprises functions to access
three NCBI resources:

1. NCBI taxonomy
  * locally stored as NCBI database
2. RefSeq genomes
  * access to: ftp://ftp.ncbi.nlm.nih.gov/genomes/
3. NCBI nr 
  * no direct access

## Usage scenarios

1. creation of custom BLAST databases 
  * e.g. collect accession numbers of all bacterial proteins and use these to filter NCBI nr for entries of interest
2. downloading of genomes of interests 
  * e.g. all available phage genomes, either coding gene nucleotide sequences or coding gene protein sequences
3. extracting taxonomic information for whole clades at ones
  * e.g. collecting taxonomic paths for all Alphaproteobacteris genera to create custom mapping files, for instance for functional gene databases

## Credits
The original idea was conceptualized by Sixing Huang (DSMZ, Braunschweig) and most of the original code was written by him. However, NCBI is phasing out GI numbers as identifiiers and links to taxonomic information. 

Therefore the original code was rewritten by me to work with the newly established system of using accession (version) numbers as replacement for GI numbers.

