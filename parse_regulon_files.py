
#Tiffany Gassmann BIMM 185 Week 5+ 6

import re, math, MySQLdb

from operator import itemgetter

#OPEN FILES
TU_table_open = open("TU_table")
TU_table= TU_table_open.readlines()

# Columns:
# (1) Transcription Unit identifier assigned by RegulonDB
# (2) Transcription unit name
# (3) Operon name containing the transcription unit
# (4) Name of the gene(s) contained in the transcription unit
# (5) Promoter Name
# (6) Evidence that supports the existence of the transcription unit
# (7) Evidence confidence level (Confirmed, Strong, Weak)

#Tiffany Gassmann
#BIMM 185 Week 6

#-------------------------------OPEN-FILES------------------------------------------------------------------------------

operonset_table_open =open("operonset_table")
operonset_table = operonset_table_open.readlines()

# Columns:
# (1) Operon name
# (2) First gene-position left
# (3) Last gene-position right
# (4) DNA strand where the operon is coded
# (5) Number of genes contained in the operon
# (6) Name or Blattner number of the gene(s) contained in the operon
# (7) Evidence that support the existence of the operon's TUs
# (8) Evidence confidence level (Confirmed, Strong, Weak)

geneproduct_table_open = open("geneproduct_table")
geneproduct_table = geneproduct_table_open.readlines()
# Columns:
# (1) Gene identifier assigned by RegulonDB
# (2) Gene name
# (3) Blattner number (bnumber) of the gene
# (4) Gene left end position in the genome
# (5) Gene right end position in the genome
# (6) DNA strand where the gene is coded
# (7) Product name of the gene
# (8) Evidence that supports the existence of the gene
# (9) PMIDs list


#Reads File in and seperates each according to a tabular
def readfile_table(table):
    for i in xrange(len(table)):
        #making table into list of lists without tab
        table[i] = table[i].strip().split("\t")
    return table


def get_locus_tag(table):
    for i in xrange(len(table)):
        # making table into list of lists without tab
        table[i] = table[i].strip().split("\t")

    #B-NUMS
    B_NUM = 2
    b_nums = ""

    for row in table:
        try:
            if row[1]:
                index = len(row) -2
                if row[1]:
                    b_nums += str(row[1]).strip(" ") + ", "
        except IndexError:
            "None"

    return b_nums



open_pos = open("pos_con")
pos_con_table = open_pos.readlines()




#Formal File
def format (list1):
    return str(list1).replace('[','').replace(']','').replace("'",'').replace('(','').replace(')','')


#---------------------------------------------------------------------------------------------------------------------

#EXTRACT GENES IN CURATED OPERONS
#Task: from TU_table and operonset_table extract the name of the genes in each transcription unit
# with evidence "strong" or "confirmed"

#Note: if there in genes in file TU_table and Operonset_table use the file GeneProduct_table to map
# the gene name to the locus_tag which we have in our data base

#Note: we can transform all operons to their b-numbers (locus-tag) before we query the database for
# their coordinates

#Extract gene name of each transcription unit with evidence strong or confirmed
#Returns: list of gene names
def extract_genes_TU_table():
    tu_table = readfile_table(TU_table)

    #index of name in TU_file
    NAME = 3
    find_confirmed_strong = "?:Strong|Confirmed"

    gene_names = []

    for line in tu_table:
        CONFIDENCE_LEVEL = len(line)-1
        if  re.findall(line[CONFIDENCE_LEVEL],find_confirmed_strong):
            if line[NAME]:
                gene_names.append(line[NAME])
    return gene_names
#----------------------------------------------------------------------------------------------------------------------

def name_to_num():

    #Number Index
    B_NUM = 2

    #Name Index
    G_NAME = 1

    geneprod_table = readfile_table(geneproduct_table)

    name_2_num_dict = {}

    for line in geneprod_table:
        if line[B_NUM] and line[G_NAME]:
            name_2_num_dict[line[G_NAME]] = line[B_NUM]

    return name_2_num_dict


#----------------------------------------------------------------------------------------------------------------------

#Task: Extracting the data to model h1 and h0
#The distances of genes inside operons will be taken directly from all
# retrieved operons with two or more genes.

def operon_model_h1_h0():

    name_2_num = name_to_num()

    operon_table = readfile_table(operonset_table)

    # index of operon table
    OPERON_NAME = 0
    GENE_NAME = 5
    LEFT = 1
    RIGHT = 2
    NUM_GENES_IN_OPERON = 4

    find_confirmed_strong = "?:Strong|Confirmed"

    gene_names = []
    operon_names = []

    gene_names_left_positions = []
    distances = []



    for line in operon_table:
        CONFIDENCE_LEVEL = len(line) - 1
        if re.findall(line[CONFIDENCE_LEVEL], find_confirmed_strong):

            #more than 2 genes - extract
            number_genes = len(line[GENE_NAME].split(","))
            if number_genes >= 2:
                try:
                    if str(line[CONFIDENCE_LEVEL]).isalpha():
                        names = str(line[GENE_NAME])
                        operon_names.append(line[OPERON_NAME])
                        gene_names.append(line[GENE_NAME])
                        b_nums = []
                        for name in names.split(','):

                            b_num = (name_2_num.get(name))
                            b_nums.append(b_num)
                        print "\t".join([line[OPERON_NAME], format(b_nums), line[CONFIDENCE_LEVEL]])
                except IndexError:
                    return None


                # MODEL H1
                distance = int(line[RIGHT]) - int(line[LEFT])
                distances.append(distance)

                #MODEL H0
            if line[GENE_NAME]:
                gene_names_left_positions.append((line[GENE_NAME],line[LEFT]))
                sorted_name_pos = sorted(gene_names_left_positions,key=itemgetter(1))



            elif not line[GENE_NAME]:
                print "flag - no gene name"

    #Test to get total number of adjacent pairs of genes in operons
    #print len(gene_names)

    #H1 testing variables

    #print gene_names
    #print num_genes_in_operons
    #print distances

    #print str(sorted_name_pos).replace("[","").replace(']','')


#operon_model_h1_h0()

#--------------------------------------------------------------------------------------------

#Positive Control
#Tasks:
# 1.) Read in Output of SQL Query Format: b_num gene_id left    right   string'").strip("(").strip("')").strip("'(").strip("")

    print hey2


# 2.) Load into dictionary with b_num as key







