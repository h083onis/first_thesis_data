from git import Repo
import sys
import subprocess
from out_txt import out_txt
from out_snippet_to_txt import out_snippet_to_txt
from out_piece_snippet import out_piece_snippet
from out_piece_snippet import out_piece_snippet_spiral


def is_auth_ext(file_path, auth_ext):
    splited_file = file_path.split('.')
    if len(splited_file) == 2 and splited_file[1] in auth_ext:
        return True
    else:
        return False

def pipe_process_first(cnt, repo,commit, hexsha, auth_ext, diff_range, snippet_filename):
    error_ctx = ''
    command1 = 'java -jar ../../package/tokenizer.jar'
    
    ch_type = 'A'
    for filepath in commit.stats.files:
        if is_auth_ext(filepath, auth_ext) == False:
            continue

        with open('../resource/before.txt','w', encoding='utf-8') as f:
            f.truncate(0)
        process1 = subprocess.Popen(command1.split(), stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        output = repo.git.show(hexsha+':'+filepath)
        process1.stdin.write(output.encode(errors='ignore'))
        process1.stdin.close()
        output = process1.communicate()[0]
        out_txt('../resource/after.txt', output.decode('utf-8'))
        process1.wait()
        if process1.returncode != 0:
            # error_ctx = hexsha+','+ch_type+','+filepath
            # print(error_ctx, file=f_error)
            continue
        cnt += 1

        for i in range(int(diff_range[0]), int(diff_range[1])+1):
            command2 = 'diff -u -'+ str(i) +' ../resource/before.txt ../resource/after.txt'
            process2 = subprocess.Popen(command2.split(), stdout=subprocess.PIPE)
            output = process2.communicate()[0]
            # snippet_list = out_piece_snippet(output.decode('utf-8'))
            snippet_list = out_piece_snippet_spiral(output.decode('utf-8'))
            out_snippet_to_txt('../resource/' + snippet_filename + '_' + str(i) + '.txt', str(cnt), snippet_list)
        
    return cnt
    
    
def pipe_process(cnt, repo, commit, hexsha, auth_ext, diff_range, snippet_filename):
    error_ctx = ''
    command1 = 'java -jar ../../package/tokenizer.jar'

    diff = commit.diff(hexsha)
    
    for item in diff:
        if is_auth_ext(item.b_path, auth_ext) == False:
            continue
        ch_type = item.change_type
        
        if ch_type != 'M' and ch_type !='R' and ch_type != 'A':
            continue
        
        if ch_type == 'M' or ch_type == 'R':
            process1 = subprocess.Popen(command1.split(), stdin=subprocess.PIPE, stdout=subprocess.PIPE)
            output = repo.git.show(hexsha+"~1"+':'+item.a_path)
            process1.stdin.write(output.encode(errors='ignore'))
            process1.stdin.close()
            output = process1.communicate()[0]
            out_txt('../resource/before.txt', output.decode('utf-8'))
            
            process2 = subprocess.Popen(command1.split(), stdin=subprocess.PIPE, stdout=subprocess.PIPE)
            output = repo.git.show(hexsha+':'+item.b_path)
            process2.stdin.write(output.encode(errors='ignore'))
            process2.stdin.close()
            output = process2.communicate()[0]
            out_txt('../resource/after.txt', output.decode('utf-8'))
            
            process1.wait()
            process2.wait()
            if process1.returncode != 0 or process2.returncode != 0:
                # error_ctx = hexsha+','+ch_type+','+item.b_path
                # print(error_ctx, file=f_error)
                continue
      
        elif ch_type == 'A':
            with open('../resource/before.txt','w', encoding='utf-8') as f:
                f.truncate(0)
            
            process2 = subprocess.Popen(command1.split(), stdin=subprocess.PIPE, stdout=subprocess.PIPE)
            output = repo.git.show(hexsha+':'+item.b_path)
            process2.stdin.write(output.encode(errors='ignore'))
            process2.stdin.close()
            output = process2.communicate()[0]
            out_txt('../resource/after.txt', output.decode('utf-8'))
            
            process2.wait()
            if process2.returncode != 0:
                # error_ctx = hexsha+','+ch_type+','+item.b_path
                # print(error_ctx, file=f_error)
                continue
        
        cnt += 1
        for i in range(int(diff_range[0]), int(diff_range[1])+1):
            command2 = 'diff -u -'+ str(i) +' ../resource/before.txt ../resource/after.txt'
            process3 = subprocess.Popen(command2.split(), stdout=subprocess.PIPE)
            output = process3.communicate()[0]
            # snippet_list = out_piece_snippet(output.decode('utf-8'))
            snippet_list = out_piece_snippet_spiral(output.decode('utf-8'))
            out_snippet_to_txt('../resource/' + snippet_filename + '_' + str(i) + '.txt', str(cnt), snippet_list)
        
    return cnt   
  
  
def excute(repo, auth_ext , diff_range, snippet_filename):
    cnt = 0
    head = repo.head
    
    if head.is_detached:
        pointer = head.commit.hexsha
    else:
        pointer = head.reference
        
    commits = list(repo.iter_commits(pointer))
    commits.reverse()
    for i, item in enumerate(commits):
        print(i)
        print(item.hexsha)
        target_hexsha = item.hexsha
        if not item.parents:
            commit = repo.commit(target_hexsha)
            cnt = pipe_process_first(cnt, repo, commit, target_hexsha, auth_ext, diff_range, snippet_filename)
        else:
            commit = repo.commit(target_hexsha+'~1')
            cnt = pipe_process(cnt, repo, commit, target_hexsha, auth_ext, diff_range, snippet_filename)
        

def main():
    # print(pure_camelcase_split('TestString'))
    # if len(sys.argv) != 3:
    #     print(f'Usage: python repo_path:{sys.argv[0]}')
    #     sys.exit(0)
    auth_ext = ['java']
    repo_path = sys.argv[1]
    diff_range = sys.argv[2].split('-')
    print(diff_range)
    snippet_filename = sys.argv[3]
    repo = Repo(repo_path)
    excute(repo, auth_ext, diff_range, snippet_filename)
    sys.exit(0)


if __name__ == '__main__':
    main()
