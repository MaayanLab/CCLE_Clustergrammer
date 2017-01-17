import networkx as nx
ppi = nx.read_edgelist(path="../ppi_ZWang/mPPIN_low_psicquic.txt", delimiter="\t")

inst_source = 'NMI'
inst_target = 'PSMB9'

if inst_source in ppi and inst_target in ppi:
  inst_path = nx.shortest_path(ppi, source=inst_source, target=inst_target)

  print(inst_path)

else:
  print('not found in the PPI ')