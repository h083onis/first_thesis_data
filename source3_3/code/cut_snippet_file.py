import sys

def cut_threshold(filename, cut_filename, threshold):
    with open(filename, 'r', encoding='utf-8') as f_origin, open(cut_filename, 'a', encoding='utf-8') as f_cut:
        while True:
            line = f_origin.readline()
            if line == '':
                break
            tmp_list = line.split('\t')    
            if len(tmp_list[1:]) > threshold:
                tmp_list2 = tmp_list[0:threshold+1]
                tmp = '\t'.join(tmp_list2)
            else:
                tmp = '\t'.join(tmp_list)
            print(tmp, file=f_cut)
            
def main():
    snippet_filename = sys.argv[1]
    cut_snippet_filename = sys.argv[2]
    threshold = int(sys.argv[3])
    
    cut_threshold(snippet_filename, cut_snippet_filename, threshold)
    
if __name__ == '__main__':
    main()