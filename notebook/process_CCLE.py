def main():

  proc_CCLE()

def proc_CCLE():
  print('processing CCLE from initial GCT file')

  # open file
  filename = '../original_data/CCLE_Expression_Entrez_2012-09-29.gct'
  f = open(filename, 'r')
  ccle_ini = f.readlines()
  f.close()

  print(len(ccle_ini))



main()