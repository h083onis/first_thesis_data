from git import Repo
import sys
import subprocess


def is_auth_ext(file_path, auth_ext):
    splited_file = file_path.split('.')
    if len(splited_file) == 2 and splited_file[1] in auth_ext:
        return True
    else:
        return False

def pipe_process_first(cnt, repo_path ,commit, hexsha, auth_ext, f_each_commit_file_inf ,f_error, diff_line, snippet_filename):
    error_ctx = ''
    command1 = 'git -C ' + repo_path + ' show '
    command2 = 'java -jar ../../package/tokenizer.jar'
    command3 = 'truncate -s 0 ../resource/before.txt'
    command4 = 'python out_txt.py ../resource/after.txt'
    command5 = 'diff -u -'+ diff_line +' ../resource/before.txt ../resource/after.txt'
    command6 = 'python out_piece_snippet.py'
    command7 = 'python out_snippet_to_txt.py ../resource/' + snippet_filename
    
    each_commit_cnt = 0
    ch_type = 'A'
    for filepath in commit.stats.files:
        if is_auth_ext(filepath, auth_ext) == False:
            continue
        process1 = subprocess.Popen(command3.split())
        process2 = subprocess.Popen(command1+hexsha+":"+filepath, stdout=subprocess.PIPE)
        process3 = subprocess.Popen(command2.split(), stdin=process2.stdout, stdout=subprocess.PIPE)
        process4 = subprocess.Popen(command4.split(), stdin=process3.stdout)
        process1.wait()
        process4.wait()
        process3.wait()
        if process3.returncode != 0:
            error_ctx = hexsha+','+ch_type+','+filepath
            print(error_ctx, f_error)
            continue
        cnt += 1
        each_commit_cnt +=1
        process5 = subprocess.Popen(command5.split(), stdout=subprocess.PIPE)
        process6 = subprocess.Popen(command6.split(), stdin=process5.stdout, stdout=subprocess.PIPE)
        output = process6.communicate()[0]
        snippet = str(cnt) + '\n' + output.decode('utf-8')
        process7 = subprocess.Popen(command7.split(), stdin=subprocess.PIPE)
        process7.stdin.write(snippet.encode())
        process7.stdin.close()
        print(str(cnt)+','+hexsha+','+filepath+','+filepath +','+ch_type, file=f_each_commit_file_inf)
        
    return cnt, each_commit_cnt   
    
    
def pipe_process(cnt, repo_path, commit, hexsha, auth_ext, f_each_commit_file_inf, f_error, diff_line, snippet_filename):
    error_ctx = ''
    command1 = 'git -C ' + repo_path + ' show '
    command2 = 'java -jar ../../package/tokenizer.jar'
    command3_1 = 'python out_txt.py ../resource/before.txt'
    command3_2 = 'truncate -s 0 ../resource/before.txt'
    command4 = 'python out_txt.py ../resource/after.txt'
    command5 = 'diff -u -' + diff_line + ' ../resource/before.txt ../resource/after.txt'
    command6 = 'python out_piece_snippet.py'
    command7 = 'python out_snippet_to_txt.py ../resource/'+ snippet_filename
    
    diff = commit.diff(hexsha)
    each_commit_cnt = 0
    for item in diff:
        if is_auth_ext(item.b_path, auth_ext) == False:
            continue
        ch_type = item.change_type
        print(ch_type)
        print(hexsha)
        print(item.b_path)
        if ch_type != 'M' and ch_type !='R' and ch_type != 'A':
            continue
        
        if ch_type == 'M' or ch_type == 'R':
            process1 = subprocess.Popen(command1+hexsha+"~1:"+item.a_path, stdout=subprocess.PIPE)
            process2 = subprocess.Popen(command2.split(), stdin=process1.stdout, stdout=subprocess.PIPE)
            process3 = subprocess.Popen(command3_1.split(), stdin=process2.stdout)
            process4 = subprocess.Popen(command1+hexsha+":"+item.b_path, stdout=subprocess.PIPE)
            process5 = subprocess.Popen(command2.split(), stdin=process4.stdout, stdout=subprocess.PIPE)
            process6 = subprocess.Popen(command4.split(), stdin=process5.stdout)
            process3.wait()
            process6.wait()
            process2.wait()
            process5.wait()
            if process2.returncode != 0 or process5.returncode != 0:
                error_ctx = hexsha+','+ch_type+','+item.b_path
                print(error_ctx, file=f_error)
                continue
      
        elif ch_type == 'A':
            process3 = subprocess.Popen(command3_2.split())
            process4 = subprocess.Popen(command1+hexsha+":"+item.b_path, stdout=subprocess.PIPE)
            process5 = subprocess.Popen(command2.split(), stdin=process4.stdout, stdout=subprocess.PIPE)
            process6 = subprocess.Popen(command4.split(), stdin=process5.stdout)
            process3.wait()
            process6.wait()
            process5.wait()
            if process5.returncode != 0:
                error_ctx = hexsha+','+ch_type+','+item.b_path
                print(error_ctx, f_error)
                continue
            
        cnt += 1
        each_commit_cnt +=1
        process7 = subprocess.Popen(command5.split(), stdout=subprocess.PIPE)
        process8 = subprocess.Popen(command6.split(), stdin=process7.stdout, stdout=subprocess.PIPE)
        output = process8.communicate()[0]
        snippet = str(cnt) + '\n' + output.decode('utf-8')
        process9 = subprocess.Popen(command7.split(), stdin=subprocess.PIPE)
        process9.stdin.write(snippet.encode())
        process9.stdin.close()
        print(str(cnt)+','+hexsha+','+item.a_path+','+item.b_path +','+ch_type, file=f_each_commit_file_inf)
        
    return cnt, each_commit_cnt   
  
  
def excute(repo_path, repo, auth_ext,branch_name,f_cnt, f_each_commit_file_inf, f_error, diff_line, snippet_filename):
    cnt = 0
    commits = list(repo.iter_commits(branch_name))
    commits.reverse()
    for i, item in enumerate(commits):
        print(i)
        print(item.hexsha)
        target_hexsha = item.hexsha
        if not item.parents:
            commit = repo.commit(target_hexsha)
            cnt, each_commit_cnt = pipe_process_first(cnt, repo_path, commit, target_hexsha, auth_ext, f_each_commit_file_inf, f_error, diff_line, snippet_filename)
        else:
            commit = repo.commit(target_hexsha+'~1')
            cnt , each_commit_cnt = pipe_process(cnt, repo_path, commit, target_hexsha, auth_ext, f_each_commit_file_inf, f_error, diff_line, snippet_filename)
        print(str(each_commit_cnt)+','+target_hexsha,file=f_cnt)

def main():
    # print(pure_camelcase_split('TestString'))
    # if len(sys.argv) != 3:
    #     print(f'Usage: python repo_path:{sys.argv[0]}')
    #     sys.exit(0)
    auth_ext = ['java']
    branch_name = 'main'
    repo_path = sys.argv[1]
    diff_line = sys.argv[2]
    cnt_source_filename = sys.argv[3]
    hexhsa_filename = sys.argv[4]
    error_log_filename = sys.argv[5]
    snippet_filename = sys.argv[6]
    repo = Repo(repo_path)
    with open('../resource/'+cnt_source_filename, 'a', encoding='utf-8') as f_cnt, \
            open('../resource/'+hexhsa_filename, 'a', encoding='utf-8') as f_each_commit_file_inf, \
            open('../resource/'+error_log_filename, 'a', encoding='utf-8') as f_error:
        excute(repo_path, repo, auth_ext, branch_name, f_cnt, f_each_commit_file_inf, f_error, diff_line, snippet_filename)
    sys.exit(0)


if __name__ == '__main__':
    main()
