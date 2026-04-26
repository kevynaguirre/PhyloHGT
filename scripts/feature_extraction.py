from Bio import Entrez, SeqIO, Phylo
from urllib.error import HTTPError, URLError
from pathlib import Path
import time
from ete4 import NCBITaxa
from collections import Counter
from itertools import combinations
import math
import csv
import argparse

# Define command-line arguments
parser = argparse.ArgumentParser(description="Annotate and transform form Newick to Nexus")
parser.add_argument("-i", "--input", required=True, help="The input tree to extract features")
parser.add_argument("-o", "--output", required=True, help="Name of the tsv file with the features")
parser.add_argument("-r", "--receptor", required=True, help="The HGT recpetor clade")
parser.add_argument("-id", "--id", required=True, help="The HGT query")
parser.add_argument("-f", "--format", required=True, help="Could be newick or nexus")
parser.add_argument("-pattern", "--pattern", help="The phylogenetic tree pattern")
parser.add_argument("-api", "--api", help="NCBI api to make a safer run")



args = parser.parse_args()

#Get filename
input_path = Path(args.input)
filename = input_path.stem  # removes both path and extension
#Set NCBI API
if args.api:
    print(f"NCBI API provided >>>>>> {args.api}")
    Entrez.api_key = args.api


ncbi = NCBITaxa()   # ✅ create an instance
### Set important variables
Receptor_MC = args.receptor
#Load tree
tree = Phylo.read(args.input, args.format)

query = [term.name for term in tree.get_terminals() if args.id in term.name]
query = query[0]

print(f"The query is: {query}")

leafs = [leaf.name for leaf in tree.get_terminals()]

# Always identify yourself to NCBI!
Entrez.email = "your_email@example.com"

#Dictionary of MCs
MC_dict = {"Opisthokonta": [33154], "Sar": [2698737], "Amoebozoa": [554915], "Archaeplastide": [33090,2763,38254], "Excavata": [2611341,2795258, 2611352], "Prokaryota": [2, 2157, 1117], "Viruses": [10239]}

#Define minor clades
minor_clades = ['Aphelida','Choanoflagellata','Filasterea','Fungi','Ichthyosporea','Metazoa','Opisthokonta incertae sedis','Rotosphaerida','unclassified Opisthokonta','Alveolata','Rhizaria','Stramenopiles','Discosea','Evosea','Tubulinea','Amoebozoa incertae sedis','unclassified Amoebozoa','Viridiplantae','Rhodophyta','Glaucocystophyceae','Metamonada','Malawimonadida','Discoba','Bacteria','Archaea','Viruses','Ancyromonadida','Apusozoa','Breviatea','Cryptophyceae','Haptista','Hemimastigophora','Provora','Rhodelphea','unclassified eukaryotes','CRuMs']


#Create an empty dictionary
acc_dict = {}


for acc in leafs:
    try:
        print(f"Fetching {acc} ...")
        with Entrez.efetch(db="protein", id=acc, rettype="gb", retmode="text") as handle:
            records = list(SeqIO.parse(handle, "genbank"))

        if not records:
            print(f"⚠️ No records found for {acc}")
            continue

        for record in records:
            taxon_id = None
            for feature in record.features:
                if feature.type == "source":
                    db_xrefs = feature.qualifiers.get("db_xref", [])
                    for ref in db_xrefs:
                        if ref.startswith("taxon:"):
                            taxon_id = ref.split(":")[1].strip()
                            break

            if taxon_id is not None:
                print(f"✅ {record.id} → taxon ID: {taxon_id}")
                print(f"Extracting metadata from {record.id}")
                id = acc
                taxid = taxon_id
                lineage = ncbi.get_lineage(taxid) #first extract a list with taxids of each elemlent of taxonomy
                taxonomy = ncbi.translate_to_names(lineage) #Extract a list of taxids translated to each scientific name
                taxonomy = ", ".join(taxonomy) #Join the element list in a string comma separated
                #Identify to which MC correspond each sequence
                MC = "Unknown_MC"
                for key, value in MC_dict.items():
                    if any(tx in lineage for tx in value):
                        MC = key
                        break
                #Store important variables in a dictionary
                acc_dict[id] = {"id": acc, "taxid": taxid, "taxonomy": taxonomy, "MC": MC}
            else:
                print(f"⚠️ {record.id} → no taxon ID found")

        # Be polite with NCBI (avoid hammering the server)
        time.sleep(0.5)

    except HTTPError as e:
        print(f"❌ HTTP Error for {acc}: {e}")
    except URLError as e:
        print(f"❌ URL Error (maybe connection issue) for {acc}: {e}")
    except Exception as e:
        print(f"❌ Unexpected error for {acc}: {e}")

#print(acc_dict)
print(f"Taxonomy information extracted {len(acc_dict)} out of {len(leafs)} tip labels")

##### Define minor clades

##### Add minor clade information into acc_dict #############################################
###Add mc to each observation
for acc, values in acc_dict.items():
    taxid = values['taxid']
    lineage = ncbi.get_lineage(taxid)
    taxonomy = list(ncbi.get_taxid_translator(ncbi.get_rank(lineage)).values())

    found = False
    for name in taxonomy:
        if name in minor_clades:
            acc_dict[acc]["mc"] = name
            found = True
            break  # stop once we find a match
    if not found:
        acc_dict[acc]["mc"] = "Unknown"


##################### Get a list of Unexpected (Additional) MCS (major clades) ################

#Get a list of all MCs present in the tree
MCs = [entry['MC'] for entry in acc_dict.values()]

#Count the MCs present in the tree, maybe need this later
pMC_dict = {}
pMCs = []
MC_counts = Counter(entry['MC'] for entry in acc_dict.values())

#Calculate which is the greates MC in the tree in order to set the donorMC
print("The proportions of MC in the tree:")
for MC_key, values in MC_counts.items():
    pMC = values/len(acc_dict)
    pMC_dict[MC_key] = {'pMC': pMC}

### We can define which is the putative donor MC
#Remove receptor_MC in order to discover which is the donor MC

def calculate_DonorMC(pMC_dict, Receptor_MC):
    #Get the max MC
    filt_pMC_dict = {k: v for k, v in pMC_dict.items() if k != Receptor_MC}
    if len(filt_pMC_dict) != 0:
        maxpMC = max(p['pMC']for p in filt_pMC_dict.values())
        maxMC = [MC_key for MC_key, p in filt_pMC_dict.items() if p['pMC'] == maxpMC][0]
        print(f"The maximum MC is: {maxMC}, with a proportion of {maxpMC}")
    else:
        maxMC = "There_is_no_donor_in_the_tree"
        print(maxMC)
    return maxMC


print(f"Computing Donor MC by its proportion in the tree")
Donor_MC = calculate_DonorMC(pMC_dict, Receptor_MC)

#Now get ids that belong to those extra MCs
unexpected = set(MCs) - {Donor_MC, Receptor_MC}
print(f"The following MC are unexpected: {unexpected}")

##Complete the tag of donor MC in order to know to which mc belongs to
donor_acc_dict = {acc: values for acc, values in acc_dict.items() if values['MC'] == Donor_MC}
##Count number of mc
#Count how many
if len(donor_acc_dict) != 0:
    dmc_counts = Counter(v['mc'] for v in donor_acc_dict.values())
    max_dmc = max(dmc_counts.items(), key=lambda x: x[1])[0]
    tag_Donor_MC = Donor_MC + "|" + max_dmc
else:
    tag_Donor_MC = Donor_MC

###### Get all IDs with additional(unexpected) MCs
##This create a dictionary with empty lists where keys are the extra MCs
unexpected_ids = {mc: [] for mc in unexpected}

#.items() return me the key and a set a values that are associated to that key
for acc, info in acc_dict.items():
    if info['MC'] in unexpected:
        unexpected_ids[info['MC']].append(acc) #save info in the dictiornary i created

print("Unexpected MCs and their IDs:")
for mc, ids in unexpected_ids.items():
    print(f"{mc}: {ids}")


############################ Calculate distance of those ids that belong to that extra MCs ###############
if len(leafs) > 3:
    tree.root_at_midpoint() #root at midpoint

tree_metrics = {} #where to save the outputs
# Compute tree diameter (max distance between any two terminals)
tips = tree.get_terminals()
diameter = max(tree.distance(a, b) for a, b in combinations(tips, 2))
max_topo = max(len(tree.get_path(a)) + len(tree.get_path(b)) - 2*len(tree.get_path(tree.common_ancestor(a,b))) for a, b in combinations(tips, 2))
print(f"The diameter of the tree is: {diameter}")
print(f"The max topology is: {max_topo}")
#Start tree calculations for important tip labels

for mc, ids in unexpected_ids.items():
    for acc in ids:
        print(f"Computing distance between {query} :::: {acc}")
        mrca = tree.common_ancestor(query, acc)
        topo = len(tree.get_path(query)) + len(tree.get_path(acc)) - 2*len(tree.get_path(mrca))
        norm_topo = topo/max_topo
        d = tree.distance(query, acc) #Calculate distance standarised by tree diameter
        d_std = d / diameter ## Standardized distance
        tree_metrics[acc] = {"topology": topo, "norm_topology": norm_topo, "raw_distance": d, "std_distance": d_std}


## Check wich is the closest unexpected id
# Find the minimum topo distance and std distance if exist unexpected mc
min_topo = math.nan
min_d_std = math.nan
num_uMCs = 0

if len(unexpected) >= 1:
    min_topo = min(d["norm_topology"] for d in tree_metrics.values())
    min_d_std = min(d["std_distance"] for d in tree_metrics.values())
    num_uMCs = len(unexpected)
    # Get all IDs that have this minimum distance
    closest_ids = [acc for acc, d in tree_metrics.items() if d["norm_topology"] == min_topo]
    print(f"Lowest topological distance: {min_topo}")
    print("ID(s) with lowest distance:", closest_ids)
    print(f"{acc_dict[closest_ids[0]]}")
    #print(tree_metrics[closest_ids[0]])
    closest_uMC = acc_dict[closest_ids[0]]["MC"]
    closest_iduMC = closest_ids[0]
    ##Complete the tag of unexpected MC in order to see to wich mc belongs to
    closest_unmc = acc_dict[closest_iduMC]["mc"]
    tag_cuMC = closest_uMC + "|" + closest_unmc
else:
    print("There is not unexpected MC to run distance calculation")
    closest_uMC = "Not_unexpected_MC"
    closest_iduMC = "Not_unexpected_id"
    tag_cuMC = "Not_unexpected_MC"

#####################################################################################################################
########################## Set LECA to know where the gene was transfered ##########################################
###################################################################################################################
def calculate_rLECA(receptor_acc_dict, Receptor_MC):
    if len(receptor_acc_dict) != 0:
        #Get the leca
        receptor_taxids = []
        for acc, values in receptor_acc_dict.items():
            receptor_taxids.append(values['taxid'])
        #Get lineages
        lineages = [ncbi.get_lineage(tid) for tid in receptor_taxids]

        # Find the intersection of all lineages (the shared ancestors)
        common_ancestors = set(lineages[0])
        for lineage in lineages[1:]:
            common_ancestors.intersection_update(lineage)
        # The deepest (most specific) taxid in that intersection is the LCA
        lca_taxid = max(common_ancestors, key=lambda x: lineages[0].index(x))

        # Get its name
        lca_name = ncbi.get_taxid_translator([lca_taxid])[lca_taxid]
        print(f"LCA taxid: {lca_taxid} → {lca_name}")
    else:
        lca_name = "Not taxonomy info available"
    return lca_name

##Extract id infro that belong to receptor MC
print("Extracting the LECA of Receptor MC to define where the gene was transfered")
receptor_acc_dict = {acc: values for acc, values in acc_dict.items() if values['MC'] == Receptor_MC}

print("Calculating rLECA")
lca_name = calculate_rLECA(receptor_acc_dict, Receptor_MC)

############################################################################################

#Saving important data
puMCs = {}
p_dMC = 0
p_rMC = 0
p_uMC = 0
for clade, values in MC_dict.items():
    if clade == Donor_MC:
        p_dMC = MC_counts[Donor_MC]/len(acc_dict)
        print(f"The Donor MC is {Donor_MC} and its proprtion in the tree is {p_dMC}")
    elif clade == Receptor_MC:
        p_rMC = MC_counts[Receptor_MC]/len(acc_dict)
        print(f"The Receptor MC is {Receptor_MC} and its proprtion in the tree is {p_rMC}")
    elif clade in unexpected:
        p_uMC = MC_counts[clade]/len(acc_dict)
        puMCs[clade] = {"uMC": clade, "proportion": p_uMC}
    else:
        p_uMC = 0
        puMCs[clade] = {"uMC": clade, "proportion": p_uMC}

#Put into list the proprtion that are stored in a dictionary and calculate mean of proportions of unexpected MC
prop_uMCs = []
for uMC, values in puMCs.items():
    print(f"The unexpected MC is {uMC} and its proportion is {values['proportion']}")
    prop_uMCs.append(values['proportion'])
mean_puMCs = sum(prop_uMCs)/len(prop_uMCs)

#Set phylogenetic pattern
if args.pattern:
    pattern = args.pattern
else:
    pattern = "Unknown"

##Create a tsv file
with open(args.output, "w", newline="") as f:
    writer = csv.writer(f, delimiter="\t")
    writer.writerow([filename] + [args.id] + [p_dMC] + [p_rMC] + [mean_puMCs] + [num_uMCs] + [min_topo] + [min_d_std] + [tag_cuMC] + [closest_iduMC] + [tag_Donor_MC] + [lca_name] + [max_topo] + [pattern])
