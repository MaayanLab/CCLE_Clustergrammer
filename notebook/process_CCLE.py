import json_scripts
import numpy as np
import pandas as pd
from sklearn.cluster import MiniBatchKMeans

def main():

  # # run once: save metadata to json
  # get_cell_line_metadata()

  # # save CCLE data to pandas dataframe
  # proc_CCLE()

  quick_downsample()

  quick_viz()


def quick_downsample():

  from clustergrammer import Network
  net = Network()

  # load matrix tsv file
  ######################3
  # net.load_file('../proc_data/rc_two_cats.txt')

  net.load_file('../original_data/CCLE.txt')

  inst_df = net.dat_to_df()

  inst_df = inst_df['mat']

  print(inst_df.shape)

  # Gather categories if necessary
  ########################################
  # if there are string categories, then keep track of how many of each category
  # are found in each of the downsampled clusters.
  tmp = inst_df.columns.tolist()

  # check if there are categories
  if type(tmp[0]) is tuple:
    print('found categories ')

    # check if category is string
    if (type(tmp[0][0]) is str):
      print('found string category ')


  # downsample cols
  num_clusts = 50
  ds_df, cluster_labels = run_kmeans_mini_batch(inst_df, num_clusts, axis=1,
    random_state=1000)

  print(ds_df.shape)

  ds_df.to_csv('../proc_data/inst_ds.txt', sep='\t')

def calc_mbk_clusters(X, n_clusters, random_state=1000):

  # kmeans is run with rows as data-points and columns as dimensions
  mbk = MiniBatchKMeans(init='k-means++', n_clusters=n_clusters,
                         max_no_improvement=100, verbose=0,
                         random_state=random_state)

  # need to loop through each label (each k-means cluster) and count how many
  # points were given this label. This will give the population size of each label
  mbk.fit(X)
  cluster_labels = mbk.labels_
  clusters = mbk.cluster_centers_

  mbk_cluster_names, cluster_pop = np.unique(cluster_labels, return_counts=True)

  num_returned_clusters = len(cluster_pop)

  return clusters, num_returned_clusters, cluster_labels, cluster_pop

def run_kmeans_mini_batch(df, n_clusters, axis=0, random_state=1000):

  print('number of clusters')
  print(n_clusters)

  import pandas as pd
  import numpy as np

  # downsample rows
  if axis == 0:
    X = df
  else:
    X = df.transpose()

  # run until the number of returned clusters with data-points is equal to the
  # number of requested clusters
  num_returned_clusters = 0
  while n_clusters != num_returned_clusters:

    clusters, num_returned_clusters, cluster_labels, cluster_pop = calc_mbk_clusters(X,
      n_clusters, random_state)

    random_state = random_state + random_state

  row_numbers = range(num_returned_clusters)
  row_labels = [ 'cluster-' + str(i) for i in row_numbers]

  # add number of points in each cluster
  cluster_info = []
  for i in range(num_returned_clusters):

    inst_name = 'Cluster: ' + row_labels[i]
    num_in_clust_string =  'number in clust: '+ str(cluster_pop[i])

    inst_tuple = (inst_name, num_in_clust_string)

    cluster_info.append(inst_tuple)

  if axis == 0:
    cols = df.columns.tolist()
  else:
    cols = df.index.tolist()

  # ds_df is always downsampling the rows, if the use wanted to downsample the
  # columns, the df will be switched back later
  ds_df = pd.DataFrame(data=clusters, index=cluster_info, columns=cols)

  # swap back for downsampled columns
  if axis == 1:
    ds_df = ds_df.transpose()

  return ds_df, cluster_labels

def quick_viz():
  # df = pd.DataFrame()

  from clustergrammer import Network
  net = Network()

  # load matrix tsv file
  # net.load_file('../original_data/CCLE.txt')
  net.load_file('../proc_data/inst_ds.txt')

  keep_top_n = 500

  net.filter_N_top('row', keep_top_n, rank_type='var')

  net.normalize(axis='row', norm_type='zscore', keep_orig=False)

  net.make_clust(dist_type='cos',views=[], sim_mat=False, calc_cat_pval=False)

  net.write_json_to_file('viz', '../json/mult_view.json', 'no-indent')
  # net.write_json_to_file('sim_row', '../json/mult_view_sim_row.json', 'no-indent')
  # net.write_json_to_file('sim_col', '../json/mult_view_sim_col.json', 'no-indent')

def get_cell_line_metadata():

  f = open('../original_data/CCLE_sample_info_file_2012-10-18.txt', 'r')
  lines = f.readlines()
  f.close()

  cl_meta = {}

  for i in range(len(lines)):

    # skip title row
    if i > 0:

      inst_line = lines[i].strip().split('\t')

      ccle_name = inst_line[0]

      inst_info = {}
      inst_info['primary_name'] = inst_line[1]
      inst_info['gender'] = inst_line[3]
      inst_info['tissue'] = inst_line[4]
      inst_info['hist'] = inst_line[5]
      inst_info['hist_sub'] = inst_line[6]
      inst_info['notes'] = inst_line[7]
      inst_info['source'] = inst_line[8]
      inst_info['exp_array'] = inst_line[9]

      if i == 1:
        print(inst_info)
        print('\n')

      # save to cl_meta
      cl_meta[ccle_name] = inst_info

  json_scripts.save_to_json(cl_meta, '../proc_data/CCLE_CL_meta.json', indent='indent')

  all_keys = cl_meta.keys()


def proc_CCLE():

  cl_meta = json_scripts.load_to_dict('../proc_data/CCLE_CL_meta.json')

  # open file
  filename = '../original_data/CCLE_Expression_Entrez_2012-09-29.gct'
  f = open(filename, 'r')
  ccle_ini = f.readlines()
  f.close()

  # get all cell lines
  row_cl = 2
  cell_lines_long = ccle_ini[row_cl].strip().split()[2:]

  # gene symbols are on the second column
  row_gs = 1
  # the data starts on the third column
  data_start = 2

  # number of cell lines
  num_cl = len(cell_lines_long)

  row_names = []
  col_names = []

  # add meta-data to cell lines
  # tissue, histology, sub-histology, gender
  dup_nci = 1
  dup_tt = 1
  for inst_cl in cell_lines_long:

    short_name = inst_cl.split('_')[0]

    if short_name == 'NCIH292':
      short_name = short_name + '-' + str(dup_nci)
      dup_nci = dup_nci + 1

    if short_name == 'TT':
      short_name = short_name + '-' + str(dup_tt)
      dup_tt = dup_tt + 1

    short_name = 'cell line: ' + short_name

    inst_tuple = (short_name,)

    # remove duplicate number at end of cell line if necesary
    if '-' in inst_cl:
      inst_cl = inst_cl.split('-')[0]

    inst_tuple = inst_tuple + ('tissue: ' + cl_meta[inst_cl]['tissue'],)
    inst_tuple = inst_tuple + ('histology: ' + cl_meta[inst_cl]['hist'],)
    inst_tuple = inst_tuple + ('sub-histology: ' + cl_meta[inst_cl]['hist_sub'],)

    inst_gender = cl_meta[inst_cl]['gender']
    if inst_gender == '':
      inst_gender = 'NA'

    inst_tuple = inst_tuple + ('gender: '+ inst_gender,)

    col_names.append(inst_tuple)

  # loop through the file, save gene names and values
  dup_ttl = 1
  for i in range(len(ccle_ini)):

    # skip the first two lines
    if i > 2:

      if i % 1000 == 0:
        print('i\t' + str(i))

      # get row
      inst_row = ccle_ini[i].strip().split('\t')

      inst_gene_name = inst_row[row_gs]

      if len(inst_gene_name) > 0:

        # make sure that there is a gene name: check the first letter
        if str.isalpha(inst_gene_name[0]):

          inst_gene = inst_row[row_gs]

          if inst_gene == 'TTL':
            inst_gene = inst_gene + str(dup_ttl)
            dup_ttl = dup_ttl + 1

          # get gene name
          row_names.append( inst_gene )

          # get data
          inst_data = np.asarray( inst_row[data_start:] )

          # save data
          ################
          # initialize array
          if i == 3:
            mat = inst_data

          # append more data
          else:
            mat = np.vstack([mat, inst_data])

          # check that there are the correct number of data points
          if len(inst_data) != num_cl:
            print('missing data in row')

  print('size before unique')
  print(len(row_names))
  print(len(col_names))

  u_row_names = list(set(row_names))
  u_col_names = list(set(col_names))

  print('size after unique')
  print(len(u_row_names))
  print(len(u_col_names))

  df = pd.DataFrame(data=mat, columns=col_names, index=row_names)

  df.to_csv('../original_data/CCLE.txt', sep='\t')

main()