import sys
import subprocess


def main():
    for_range = sys.argv[1]
    threshold = sys.argv[2]
    pyfile ='make_vec_from_mapping_table2.py'
    
    for i in range(int(for_range)):
        snippet_file = '../../../../sample_data/data/camel_snippet_each_commit/commit_snippet_camel_'+str(i)+'.txt'
        vec_file = '../../../../sample_data/data/camel_txt_vec/txt_vec_camel_'+str(i)+'.txt'
        process = subprocess.Popen(['python', pyfile,  snippet_file, vec_file, threshold])
        # process.wait()

    sys.exit(0)
    
if __name__ == '__main__':
    main()
    