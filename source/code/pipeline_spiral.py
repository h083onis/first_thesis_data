from git import Repo
import sys
import subprocess
import site
import os


def is_auth_ext(file_path, auth_ext):
    splited_file = file_path.split('.')
    if len(splited_file) == 2 and splited_file[1] in auth_ext:
        return True
    else:
        return False


def pipe_process(cnt, repo_path, commit, hexsha, auth_ext, f_each_commit_file_inf):
    error_ctx = ''
    command1 = 'git -C ' + repo_path + ' show '
    command2 = 'java -jar ../../package/tokenizer.jar'
    command3_1 = 'python out_txt.py ../resource/before2.txt'
    command3_2 = 'truncate -s 0 ../resource/before2.txt'
    command4 = 'python out_txt.py ../resource/after2.txt'
    command5 = 'diff -u -3 ../resource/before2.txt ../resource/after2.txt'
    command6 = 'python out_piece_snippet.py'
    command7 = 'python out_snippet_to_txt.py ../resource/snippet2.txt'
    
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
                with open('../resource/error_log2.txt', 'a', encoding='utf-8') as f_error:
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
                with open('../resource/error_log2.txt', 'a', encoding='utf-8') as f_error:
                    print(error_ctx, f_error)
                    continue
                
        cnt += 1
        each_commit_cnt +=1
        process7 = subprocess.Popen(command5.split(), stdout=subprocess.PIPE)
        process8 = subprocess.Popen(command6.split(), stdin=process7.stdout, stdout=subprocess.PIPE)
        process8.wait()
        output = process8.communicate()[0]
        snippet = str(cnt) + '\n' + output.decode('utf-8')
        process9 = subprocess.Popen(command7.split(), stdin=subprocess.PIPE)
        process9.stdin.write(snippet.encode())
        process9.stdin.close()
        print(str(cnt)+','+hexsha+','+item.a_path+','+item.b_path +','+ch_type, file=f_each_commit_file_inf)
        
    return cnt, each_commit_cnt   
  
def excute(repo_path, repo, auth_ext,branch_name,f_cnt, f_each_commit_file_inf):
    cnt = 0
    # for i, item in enumerate(repo.iter_commits(branch_name)):
    #     print(i)
    #     commit = repo.commit(item.hexsha+'~1')
    #     cnt , each_commit_cnt = pipe_process(cnt, repo_path, commit, item.hexsha, auth_ext, f_each_commit_file_inf)
    #     print(str(each_commit_cnt)+','+item.hexsha,file=f_cnt)
    #     if i >= 10000:
    #         break
    # hexsha = 'd80f93cca26f82126f408179fdc8c3c6c1ccbc7f' #参考論文記載
    # hexsha2 = '7597d063c5d389ea581f00143ed432c799a07bbe' #
    hexsha3 = '366c79fc8ff0bcec1166add80ef9654fd657d0ce' #javaソース３つ（名前変更あり）
    # hexsha4 = '96b11876eda0a2493d2ab62149ad3c468c437fd7' #鍵ファイルあり
    # hexsha5 = '14da5036ee1792830b2c9892e5c59268141fbacd'
    # hexsha6 = 'e77eedef0ba5250b8a460f38f53e1849892e6919'　#ADDED変更あり
    # hexsha7 = '2e0730f26f70e6ddabb9b504e0c186ba0cb9b637'  # __name__Endpoint.java
    commit = repo.commit(hexsha3+'~1')
    cnt , each_commit_cnt = pipe_process(cnt, repo_path, commit, hexsha3, auth_ext, f_each_commit_file_inf)
    print(str(each_commit_cnt)+','+hexsha3,file=f_cnt)


def main():
    # print(site.getsitepackages())
    # print(spiral.__version__)

    # print(pure_camelcase_split('TestString'))
    # if len(sys.argv) != 3:
    #     print(f'Usage: python repo_path:{sys.argv[0]}')
    #     sys.exit(0)
    # auth_ext = ['java','c','h','cpp','hpp','cxx','hxx']
    auth_ext = ['java']
    repo_path = '../../../../sample_data/camel/'
    branch_name = 'main'
    repo = Repo(repo_path)
    with open('../resource/cnt_sorce_file2.txt', 'a', encoding='utf-8') as f_cnt, \
            open('../resource/hexsha_filename2.txt', 'a', encoding='utf-8') as f_each_commit_file_inf:
        excute(repo_path, repo, auth_ext, branch_name, f_cnt, f_each_commit_file_inf)
    sys.exit(0)


if __name__ == '__main__':
    main()
