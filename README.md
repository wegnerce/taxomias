# taxomias
_________ _______           _______  _______ _________ _______  _______ 
\__   __/(  ___  )|\     /|(  ___  )(       )\__   __/(  ___  )(  ____ \
   ) (   | (   ) |( \   / )| (   ) || () () |   ) (   | (   ) || (    \/
   | |   | (___) | \ (_) / | |   | || || || |   | |   | (___) || (_____ 
   | |   |  ___  |  ) _ (  | |   | || |(_)| |   | |   |  ___  |(_____  )
   | |   | (   ) | / ( ) \ | |   | || |   | |   | |   | (   ) |      ) |
   | |   | )   ( |( /   \ )| (___) || )   ( |___) (___| )   ( |/\____) |
   )_(   |/     \||/     \|(_______)|/     \|\_______/|/     \|\_______)
                                                                        
TAXOMIAS v0.1 August, '16

@author:      Carl-Eric Wegner
@affiliation: Küsel Lab - Aquatic Geomicrobiology
              Friedrich Schiller University of Jena

              carl-eric.wegner@uni-jena.de

The idea behind TAXOMIAS is to locally setup a tailored NCBI taxonomy database
 and to provide wrappers to utilize this database for common tasks such as:
	
	- creation of custom BLAST databases (e.g. all bacterial proteins)
	- downloading of genomes of interests (e.g. all available phage genomes)
	- etc...

The original idea was conceptualized by Sixing Huang (DSMZ, Braunschweig). However,
NCBI is phasing out GI numbers as identifiiers and links to taxonomic information. 

Therefore the original code was rewritten by me to work with the newly established 
system of using accession (version) numbers as replacement.

