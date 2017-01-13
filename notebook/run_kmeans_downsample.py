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
  mbk.fit(X)
  mbk_labels = mbk.labels_
  mbk_clusters = mbk.cluster_centers_

  mbk_cluster_names, mbk_cluster_pop = np.unique(mbk_labels, return_counts=True)

  print('mbk cluster names: ' + String(mbk_cluster_names))
  print('mbk cluster populations: ' + String(mbk_cluster_pop))

  row_numbers = range(n_clusters)
  row_labels = [ 'cluster-' + str(i) for i in row_numbers]

  # add number of points in each cluster
  cluster_info = []
  for i in range(n_clusters):

    inst_name = 'Cluster: ' + row_labels[i]

    cluster_info.append(inst_name)

  if axis == 0:
    cols = df.columns.tolist()
  else:
    cols = df.index.tolist()

  # ds_df is always downsampling the rows, if the use wanted to downsample the
  # columns, the df will be switched back later
  ds_df = pd.DataFrame(data=mbk_clusters, index=cluster_info, columns=cols)

  # swap back for downsampled columns
  if axis == 1:
    ds_df = ds_df.transpose()

  return ds_df, mbk_labels