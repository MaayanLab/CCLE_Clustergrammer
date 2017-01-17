import pandas as pd
import networkx as nx
from clustergrammer import Network
from itertools import combinations

def main():

  net = Network()
  net.load_file('../proc_data/col_ds_50_row_filt_500.txt')
  tmp_df = net.dat_to_df()
  df = tmp_df['mat']

  genes = df.index.tolist()

  all_combos = list(combinations(genes, 2))
  print(len(all_combos))

  print(all_combos[0])
  print(all_combos[0][0])
  print(all_combos[0][1])

  ppi = nx.read_edgelist(path="../ppi_ZWang/mPPIN_low_psicquic.txt", delimiter="\t")

  for inst_combo in all_combos:

    inst_source = inst_combo[0]
    inst_target = inst_combo[1]

    inst_path = get_path(ppi, inst_source, inst_target)

    # allow direct or indirect interactions
    if len(inst_path) > 1 and len(inst_path) < 4:
      pass

def get_path(ppi, inst_source, inst_target):

  if inst_source in ppi and inst_target in ppi:

    try:
      inst_path = nx.shortest_path(ppi, source=inst_source, target=inst_target)
    except:
      inst_path = []

  else:
    inst_path = []


  return inst_path

main()