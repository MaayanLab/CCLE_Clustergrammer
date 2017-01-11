def main():

  proc_CCLE()

def proc_CCLE():
  print('processing CCLE from initial GCT file')

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

  # make tuple cell line names


  # loop through the file, save gene names and values
  for i in range(len(ccle_ini)):

    # skip the first two lines
    if i > 2:

      if i % 1000 == 0:
        print('i\t' + str(i))

      # get row
      inst_row = ccle_ini[i].split('\t')

      # # make sure that there is a gene name: check the first letter
      # if str.isalpha(inst_row[0]):

      #   pass

main()