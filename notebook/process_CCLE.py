def main():

  # # run once: save metadata to json
  # get_cell_line_metadata()

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

  cl_meta = json_scripts.load_to_dict('../proc_data/CCLE_CL_meta.json')

  # open file
  filename = '../original_data/CCLE_Expression_Entrez_2012-09-29.gct'
  f = open(filename, 'r')
  ccle_ini = f.readlines()
  f.close()

  # get all cell lines
  row_cl = 2
  cell_lines_long = ccle_ini[row_cl].split()[2:]

  cell_lines = [d.split('_')[0] for d in cell_lines_long]

  # gene symbols are on the second column
  row_gs = 1
  # the data starts on the third column
  data_start = 2

  # number of cell lines
  num_cl = len(cell_lines)

  row_names = []
  col_names = []

  # add meta-data to cell lines
  # tissue, histology, sub-histology, gender
  for inst_cl in cell_lines_long:

    cell_line_short_name = inst_cl.split('_')[0]
    inst_tuple = (cell_line_short_name,)

    inst_tuple = inst_tuple + (cl_meta[inst_cl]['tissue'],)
    inst_tuple = inst_tuple + (cl_meta[inst_cl]['hist'],)
    inst_tuple = inst_tuple + (cl_meta[inst_cl]['hist_sub'],)

    inst_gender = cl_meta[inst_cl]['gender']
    if inst_gender == '':
      inst_gender = 'NA'

    inst_tuple = inst_tuple + (inst_gender,)

    col_names.append(inst_tuple)



  # # loop through the file, save gene names and values
  # for i in range(len(ccle_ini)):

  #   # skip the first two lines
  #   if i > 2:

  #     if i % 1000 == 0:
  #       print('i\t' + str(i))

  #     # get row
  #     inst_row = ccle_ini[i].split('\t')

  #     # # make sure that there is a gene name: check the first letter
  #     # if str.isalpha(inst_row[0]):

  #     #   pass

main()