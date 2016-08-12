# -*- coding: utf-8 -*-
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

**** SEE README.md for details

"""
#needed modules
import os, sqlite3

#path to local NCBI taxonomy database
db = "ncbi_taxonomy.db"
#default return values if no results are found
unknown = -1
no_rank = "no rank"

#taxomias.TaxidByName("Bacteria")
def TaxidByName(name,limit=1):
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    command = 'SELECT taxid FROM tree WHERE name = "' + name +  '";'   
    cursor.execute(command)
    result = cursor.fetchone()
    cursor.close()
    if result:
		  return result[0]
    else:
		  return [unknown]  

#taxomias.RankByTaxid(2)
def RankByTaxid(taxid):
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    command = "SELECT rank FROM tree WHERE taxid = '" + str(taxid) +  "';"      
    cursor.execute(command)
    result = cursor.fetchone()
    cursor.close()    
    if result:
        return result[0]
    else:
        return no_rank

#taxomias.getRankByName("Bacteria")
def RankByName(name):
    try:
        return RankByTaxid(TaxidByName(name))
    except:
        return no_rank

#taxomias.NameByTaxid(2)
def NameByTaxid(taxid):
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    command = "SELECT name FROM tree WHERE taxid = '" + str(taxid) +  "';"    
    cursor.execute(command)
    result = cursor.fetchone()
    cursor.close()       
    if result:
        return result[0]
    else:
        return "unknown"

#taxomias.NameByTaxid(2)    
def ParentByTaxid(taxid):
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    command = 'SELECT parent FROM tree WHERE taxid = "' + str(taxid) +  '";'
    cursor.execute(command)    
    result = cursor.fetchone()
    cursor.close()
    if result:
        return result[0]
    else:
        return unknown
    
#taxomias.ParentByName("Flavobacteriia")
def ParentByName(name):
    try:
        return ParentByTaxid(TaxidByName(name))
    except:
        return unknown
    
#taxomias.PathByTaxid(1224)				
def PathByTaxid(taxid):
    path = []    
    current_id = int(taxid)
    path.append(current_id)    
    while current_id != 1 and current_id != unknown:
        #print current_id
        current_id = int(ParentByTaxid(current_id))
        path.append(current_id)    
    return path[::-1]

#taxomias.TaxidByAcc("P15711.1")
def TaxidByAcc(acc):
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    command = "SELECT taxid FROM acc_taxid WHERE accession_version = '" + acc +  "';"
    cursor.execute(command)    
    result = cursor.fetchone()
    cursor.close()
    if result:
        return result[0]
    else:
        return unknown

#taxomias.SonsByTaxid(1239)
def SonsByTaxid(taxid):
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    command = "SELECT taxid FROM tree WHERE parent = '" + str(taxid) +  "';"
    result = [row[0] for row in cursor.execute(command)]
    cursor.close()
    return result

#taxomias.SonsByName("Firmicutes")
def SonsByName(name):
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    command = "SELECT taxid FROM tree WHERE parent = '" + str(TaxidByName(name)) +  "';"
    result = [row[0] for row in cursor.execute(command)]
    cursor.close()
    return result

#taxomias.AccByTaxid(1239)
def AccByTaxid(taxid):
    conn = sqlite3.connect(db)
    command = "SELECT accession_version FROM acc_taxid WHERE taxid = '" + str(taxid) +  "';"
    cursor = conn.cursor()
    try:
        result = [row[0] for row in cursor.execute(command)]         
        cursor.close()
        return result
    except Exception, e:
        print e
 
#taxomias.AllSonsByTaxid(1239)       
def AllSonsByTaxid(taxid):
    from threading import Thread
    import Queue
    in_queue = Queue.Queue()
    out_queue = Queue.Queue()
    def work():
        while True:
            sonId = in_queue.get()
            for s_s_id in SonsByTaxid(sonId):
                out_queue.put(s_s_id)
                in_queue.put(s_s_id)       
            in_queue.task_done()    
    for i in range(4):        
        t = Thread(target=work)
        t.daemon = True
        t.start()    
    for son in SonsByTaxid(taxid):
        out_queue.put(son)
        in_queue.put(son)
    in_queue.join()    
    result = []
    while not out_queue.empty():        
        result.append(out_queue.get())    
    return result
    
#taxomias.AllAccByTaxid(1239)
def AllAccByTaxid(taxid):
    from threading import Thread
    import Queue
    in_queue = Queue.Queue()
    out_queue = Queue.Queue()
    allSons = AllSonsByTaxid(taxid)    
    def work():
        while True:
            sonId = in_queue.get()
            out_queue.put(AccByTaxid(sonId))
            in_queue.task_done()
    for i in range(4):        
        t = Thread(target=work)
        t.daemon = True
        t.start()        
    in_queue.put(taxid)
    for son in allSons:
        in_queue.put(son)
    in_queue.join()            
    result = []
    while not out_queue.empty():        
        result += out_queue.get()  
    result = [item.encode("utf-8") for item in result]
    return result

#taxomias.GenomeByTaxid(240015, "nucl")
def GenomeByTaxid(taxid, seqs):
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    command = "SELECT path FROM genomes WHERE taxid = '" + str(taxid) +  "';"
    cursor.execute(command)    
    result = cursor.fetchone()
    cursor.close()
    if result and seqs == "nucl":
        cmd = "wget --user=anonymous --password=carl-eric.wegner@uni-jena.de --directory-prefix "+str(taxid)+" "+"'"+result[0]+"/*.fna.gz"+"'"
        os.system(cmd)        
        return "Genome (nucleotide sequences) downloaded for " + str(taxid) + "."
    elif result and seqs == "prot":
        cmd = "wget --user=anonymous --password=carl-eric.wegner@uni-jena.de --directory-prefix "+str(taxid)+" "+"'"+result[0]+"/*.faa.gz"+"'"
        os.system(cmd)
        return "Genome (protein sequences) downloaded for " + str(taxid) + "."
    else:
        return unknown

#taxomias.AllGenomesByTaxid(2207, "prot")
def AllGenomesByTaxid(taxids, seqs):
	for taxid in AllSonsByTaxid(taxids):
		GenomeByTaxid(taxid, seqs)