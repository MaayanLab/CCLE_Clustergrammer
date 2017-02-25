import numpy as np
import pandas as pd
import networkx as nx
from clustergrammer import Network
from itertools import combinations

def main():

  make_ppi_sim_mat()

  quick_sim_mat()

def quick_sim_mat():
  net = Network()

  net.load_file('../proc_data/df_ppi.txt')

  # net.filter_threshold('row', threshold=0.5, num_occur=2)
  # net.filter_threshold('col', threshold=0.5, num_occur=2)

  net.make_clust()
  net.write_json_to_file('viz', '../json/ppi.json', 'no-indent')

def make_ppi_sim_mat():

  # # load all 500 genes
  # net = Network()
  # net.load_file('../proc_data/col_ds_50_row_filt_500.txt')
  # tmp_df = net.dat_to_df()
  # df = tmp_df['mat']
  # genes = sorted(df.index.tolist())

  f = open('tmp_cluster_genes.txt', 'r')
  lines = f.readlines()
  f.close()

  genes = []
  for inst_line in lines:
    inst_line = inst_line.strip()
    genes.append(inst_line)

  print(len(genes))

  mat = np.identity(len(genes))

  all_combos = list(combinations(genes, 2))
  print(len(all_combos))

  print(all_combos[0])
  print(all_combos[0][0])
  print(all_combos[0][1])

  ppi = nx.read_edgelist(path="../ppi_ZWang/mPPIN_low_psicquic.txt", delimiter="\t")

  num_interact = 0
  for inst_combo in all_combos:

    inst_source = inst_combo[0]
    inst_target = inst_combo[1]

    source_index = genes.index(inst_source)
    target_index = genes.index(inst_target)

    inst_path = get_path(ppi, inst_source, inst_target)

    path_length = len(inst_path)

    # allow direct or indirect interactions
    if path_length > 1 and path_length < 4:

      # distance falls off with path length
      inst_dist = float(1) / (path_length - 1)

      mat[source_index, target_index] = inst_dist
      mat[target_index, source_index] = inst_dist

      num_interact = num_interact + 1

  print('num interact: ' + str(num_interact))

  # save dataframe
  df_ppi = pd.DataFrame(data=mat, columns=genes, index=genes)

  df_ppi.to_csv('../proc_data/df_ppi.txt', sep='\t')


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