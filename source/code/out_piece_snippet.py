import sys

def out_piece_snippet():
    lines_extraction = []
    integrate_text = ''
    idx_list1 = []
    is_start = False
    cnt = 0
    
    lines = sys.stdin.readlines()
    
    for line in lines:
        if line[0:2] == '@@':
            is_start = True
            idx_list1.append(cnt)
        if is_start == True and(line[0] == '+' or line[0] == ' '):
            lines_extraction.append(line[1:].strip())
            cnt += 1
            
    if not sys.stdin.isatty():
        n = 1
        idx_list1.append(len(lines_extraction))
        idx_list2 = idx_list1[n:] + idx_list1[:n]
        for idx1, idx2 in zip(idx_list1[:-1], idx_list2[:-1]):
            integrate_text = ' '.join(lines_extraction[idx1:idx2])
            print(integrate_text)
        return
        
           
def main():
    # if len(sys.argv) != 3:
    #     print(f'Usage: python repo_path:{sys.argv[0]}')
    #     sys.exit(0)
    out_piece_snippet()
    sys.exit(0)
    
    
if __name__ == '__main__':
    main()