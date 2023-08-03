import sys
import subprocess
from make_data import *

def main():
    threshold = 2001
    
    for i in range(31):
        vec_file = '../../../../sample_data/data/camel_txt_vec/txt_vec_camel_'+str(i)+'.txt'
        label_file = '../label/label_camel.csv'
        data_file = '../../../../sample_data/data/camel_txt_vec_and_label/txt_vec_and_label_camel_'+str(i)+'.csv'
        assign_label(vec_file, label_file, data_file, threshold)
        # process.wait()

    sys.exit(0)
    
if __name__ == '__main__':
    main()
    