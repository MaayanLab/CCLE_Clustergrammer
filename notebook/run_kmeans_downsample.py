def run_kmeans_mini_batch(df, n_clusters, axis=0):
  from sklearn.cluster import MiniBatchKMeans
  import pandas as pd
  import numpy as np

  # downsample rows
  if axis == 0:
    X = df
  else:
    X = df.transpose()
  # kmeans is run with rows as data-points and columns as dimensions
  mbk = MiniBatchKMeans(init='k-means++', n_clusters=n_clusters,
                        max_no_improvement=10, verbose=0, random_state=1000)

  # need to loop through each label (each k-means cluster) and count how many
  # points were given this label. This will give the population size of each label
  # For MNIST, I also need to get the digit breakdown of each cluster to see what
  # digits make up each cluster. Then I can work on overrepresentation examples.
  ################################################
  mbk.fit(X)
  mbk_labels = mbk.labels_
  mbk_clusters = mbk.cluster_centers_

  mbk_cluster_names, mbk_cluster_pop = np.unique(mbk_labels, return_counts=True)

  print('============================')
  print('mbk cluster names')
  print(mbk_cluster_names)
  print('mbk cluster populations')
  print(mbk_cluster_pop)
  print('============================')

  # make a dictionary with cluster keys
  # each value in the dictionary will be an array with 10 digits that gives
  # the fraction of digits in the cluster that fall into each digit category
  digit_cats = {}
  digit_types = ['Zero', 'One', 'Two', 'Three', 'Four', 'Five', 'Six', \
                 'Seven', 'Eight', 'Nine']

  # initialize digit_cats dictionary
  for inst_clust in range(n_clusters):
    digit_cats[inst_clust] = np.zeros([10])

  col_array = np.asarray(df.columns.tolist())

  # populate the dictionary
  for inst_clust in range(n_clusters):

    # get the indices of all digits that fall in cluster
    found = np.where(mbk_labels == inst_clust)

    found_indices = found[0]

    check = mbk_labels[found_indices]

    clust_names = col_array[found_indices]

    for inst_name in clust_names:

      # simple format
      #######################################
      inst_digit = inst_name.split('-')[0]

      # # complex format
      # ####################################################
      # inst_digit = inst_name[0].split(': ')[1].split('-')[0]

      tmp_index = digit_types.index(inst_digit)

      digit_cats[inst_clust][tmp_index] = digit_cats[inst_clust][tmp_index] + 1

  # calculate fractions
  for inst_clust in range(n_clusters):

    counts = digit_cats[inst_clust]

    inst_total = np.sum(counts)

    digit_cats[inst_clust] = digit_cats[inst_clust] / inst_total

    print(digit_cats[inst_clust])


  row_numbers = range(n_clusters)
  row_labels = [ 'cluster-' + str(i) for i in row_numbers]

  # add number of points in each cluster
  cluster_cats = []
  for i in range(n_clusters):

    inst_name = 'MNIST-Clusters: ' + row_labels[i]
    num_in_clust_string =  'number in clust: '+ str(mbk_cluster_pop[i])

    # add category to majority digit in cluster
    ##############################################
    cat_values = digit_cats[i]

    max_cat_fraction = cat_values.max()
    max_cat_index = np.where(cat_values == max_cat_fraction)[0][0]
    max_cat_name = digit_types[max_cat_index]

    print(digit_types[max_cat_index])

    # add cat string
    cat_name_string = 'Majority Digit: ' + max_cat_name

    # reordering the labels
    inst_tuple = ( inst_name, cat_name_string )
    inst_tuple = inst_tuple + (num_in_clust_string,)

    # add cat fraction
    max_cat_fraction = np.round(max_cat_fraction, decimals=2) * 100
    fraction_string = 'Digit Pct: ' + str(max_cat_fraction)
    inst_tuple = inst_tuple + (fraction_string,)

    # add value categories for each number
    ########################################
    # for tmp_index in range(len(digit_types)):

    #   tmp_digit = digit_types[tmp_index]
    #   tmp_fraction = cat_values[tmp_index]

    #   fraction_string = str(tmp_digit) + ': ' + str(tmp_fraction)
    #   inst_tuple = inst_tuple + (fraction_string,)

    cluster_cats.append(inst_tuple)

  ds = mbk_clusters

  if axis == 0:
    cols = df.columns.tolist()
  else:
    cols = df.index.tolist()


  # ds_df = pd.DataFrame(data=ds, columns = cols, index=cluster_cats)

  # ds_df is always downsampling the rows, if the use wanted to downsample the
  # columns, the df will be switched back later
  ds_df = pd.DataFrame(data=ds, index=cluster_cats, columns=cols)

  # swap back for downsampled columns
  if axis == 1:
    ds_df = ds_df.transpose()

  # add center value-cat to pixels
  old_rows = ds_df.index.tolist()

  new_rows = []

  max_radius = np.sqrt( np.square(28) + np.square(28) )

  for inst_row in old_rows:

    # make name
    inst_name = 'Pixels: '+ inst_row

    # make radius category
    pos = inst_row.split('pos_')[1]
    inst_x = int(pos.split('-')[0]) - 14
    inst_y = int(pos.split('-')[1]) - 14
    inst_radius = (max_radius/2 - np.sqrt( np.square(inst_x) + np.square(inst_y) ))/19.79
    inst_cat = 'Center: '+ str(inst_radius)

    inst_tuple = ( inst_name, inst_cat )

    new_rows.append(inst_tuple)

  ds_df.index = new_rows


  return ds_df, mbk_labels