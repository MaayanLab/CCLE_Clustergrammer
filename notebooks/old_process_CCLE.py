def transfer_CCLE_from_GCT_to_TSV():
  # import json_scripts
  import numpy as np

  print('transfer CCLE from GCT to TSV\n')

  # open file
  filename = '../original_data/CCLE_Expression_Entrez_2012-09-29.gct'
  f = open(filename, 'r')
  ccle_ini = f.readlines()
  f.close()

  print(len(ccle_ini))

  # save data into ccle array
  ccle = {}
  ccle['gene'] = []

  # get all cell lines - they are on the third row
  row_cl = 2
  cell_lines_long = ccle_ini[row_cl].split()[2:]

  cell_lines = [d.split('_')[0] for d in cell_lines_long]

  print(cell_lines)

  # save cell lines in ccle
  ccle['cell_lines'] = cell_lines
  ccle['cell_lines_long'] = cell_lines_long

  # # skip the first two columns:
  # print( str(len(ccle_ini[1].split()[2:])) + '\n')

  # the gene symbols are in the second column: Description (name is *_at)
  row_gs = 1

  # the data starts in column 3
  data_start = 2

  # number of cell lines
  num_cl = 1037

  # loop throgh file, save gene names and values
  for i in range(len(ccle_ini)):

    # skip the first two lines
    if i > 2:

      if i % 1000 == 0:
        print('i\t' + str(i))

      # get the inst line
      inst_line = ccle_ini[i]

      # make sure that there is a gene name: check first letter
      if str.isalpha(inst_line.split()[row_gs][0]):

        # collect gene names
        ccle['gene'].append( inst_line.split()[row_gs])

        # collect measurements
        inst_meas = np.asarray( inst_line.split()[data_start:] )

        # save measurements
        if i == 3:
          # initialize array
          ccle['data'] = inst_meas
          print(ccle['data'])
        else:
          # append additional measurements
          ccle['data'] = np.vstack([ccle['data'], inst_meas])


        # check that there are the correct number of data points
        if len(inst_meas) != num_cl:
          print('missing value')
          print(len(inst_meas))
          print('\n')

  # save as json
  ###################
  # convert data to list
  ccle['data'] = np.array(ccle['data']).tolist()

  json_scripts.save_to_json( ccle, 'ccle_all.json', 'no indent' )