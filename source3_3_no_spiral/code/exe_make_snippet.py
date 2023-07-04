import sys
import subprocess


def main():
    repo_path = sys.argv[1]
    repo_name = repo_path.split('/')[-1]
    diff_range = sys.argv[2]
    pyfile ='pipeline_spiral4.py'
    
    cnt_srcfile = 'cnt_source_file_'+repo_name+'_.txt'
    hexsha_filename = 'hexsha_filename_'+repo_name+'_.txt'
    error_log = 'error_log_'+repo_name+'_.txt'
    snippet = 'snippet_'+repo_name
    process = subprocess.Popen(['python', pyfile, repo_path, diff_range , cnt_srcfile, hexsha_filename, error_log, snippet])
    process.wait()

    sys.exit(0)
    
if __name__ == '__main__':
    main()
