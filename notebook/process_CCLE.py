def main():

  # # run once: save metadata to json
  # get_cell_line_metadata()

  # save CCLE data to pandas dataframe
  proc_CCLE()

def get_cell_line_metadata():

  import json_scripts

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
  import json_scripts
  import numpy as np
  import pandas as pd

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

    inst_tuple = inst_tuple + ('cat: ' + cl_meta[inst_cl]['tissue'],)
    inst_tuple = inst_tuple + ('cat: ' + cl_meta[inst_cl]['hist'],)
    inst_tuple = inst_tuple + ('cat: ' + cl_meta[inst_cl]['hist_sub'],)

    inst_gender = cl_meta[inst_cl]['gender']
    if inst_gender == '':
      inst_gender = 'NA'

    inst_tuple = inst_tuple + ('cat: '+ inst_gender,)

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

          # # get data
          # inst_data = np.asarray( inst_row[data_start:] )

          # # save data
          # ################
          # # initialize array
          # if i == 3:
          #   mat = inst_data

          # # append more data
          # else:
          #   mat = np.vstack([mat, inst_data])

          # # check that there are the correct number of data points
          # if len(inst_data) != num_cl:
          #   print('missing data in row')

  print('size before unique')
  print(len(row_names))
  print(len(col_names))

  u_row_names = list(set(row_names))
  u_col_names = list(set(col_names))

  print('size after unique')
  print(len(u_row_names))
  print(len(u_col_names))

  # df = pd.DataFrame(data=mat, columns=col_names, index=row_names)

  # df.to_csv('../original_data/CCLE.txt', sep='\t')

main()