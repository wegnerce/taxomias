
"""
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

The given script automatically sets up a local installation of the NCBI taxonomy
databases, as well as a mapping of taxonomic identifiers to available annotated
genomes.

**** SEE README.md for details

"""
# needed modules
import sqlite3, sys

# needed dictionaries for reading the taxonomy and the accession to genome
# mappings
tree = {}
tax_genomes = {}

#process the names.dmp, path to names dump
input_names = open(sys.argv[1], "rU")
for line in input_names:
    fields = line.strip().split("\t")
    notion = fields[6]
    taxid = fields[0]
    name = fields[2]
    if notion== "scientific name":
        if taxid not in tree:
            tree[taxid] = [name,"0",""]            
input_names.close()

#process the nodes.dmp, path to nodes.dmp
input_nodes = open(sys.argv[2], "rU")
for line in input_nodes:
    fields = line.strip().split("\t")    
    taxid = fields[0]
    parent = fields[2]
    rank = fields[4]    
    if taxid in tree:
        tree.get(taxid)[1] = parent
        tree.get(taxid)[2] = rank        
input_nodes.close()

#process genomes accessory table, path to genomes accessory table
for line in open(sys.argv[3], "r"):
	fields = line.strip().split("\t")
	taxid = fields[0]
	path = fields[1]
	tax_genomes[taxid] = path

#link to setup database
conn = sqlite3.connect(sys.argv[4])
cursor = conn.cursor()
cursor.execute("CREATE TABLE tree (taxid integer, name text, parent integer, rank text);") # create table harboring

for taxid in tree.keys():
    command = "INSERT INTO tree VALUES ('" + taxid + "', '" + tree[taxid][0].replace("'","''") + "', '" + tree[taxid][1] + "','" + tree[taxid][2] +"');"
    cursor.execute(command)    

cursor.execute("CREATE TABLE genomes (taxid integer, path text);") # create table containing taxid genome path pairs

for taxid in tax_genomes.keys():
	command = "INSERT INTO genomes VALUES ('" + taxid + "', '" + tax_genomes[taxid] + "');"
	cursor.execute(command)

conn.commit()


