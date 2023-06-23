import sys

def out_snippet_to_txt(txt_name):
    integrate_txt = ''
    cnt = 0
    with open(txt_name, 'a', encoding='utf-8') as f_snippet:
        lines = sys.stdin.readlines()
        idx = lines[0].strip()
        for line in lines[1:]:
            cnt += 1
            integrate_txt = idx + '-'+str(cnt) +'\t' + line
            f_snippet.write(integrate_txt)
        if not sys.stdin.isatty():
            return
            
            
def main():
    # if len(sys.argv) != 2:
    #     print(f'Usage: python txt_name:{sys.argv[0]}')
    #     sys.exit(0)
    out_snippet_to_txt(sys.argv[1])
    sys.exit(0)
    
if __name__ == '__main__':
    main()