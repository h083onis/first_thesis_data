import sys

def make_txt_vec(snippet_file, vec_file, word_dict, threshold):

    with open(snippet_file,'r', encoding='utf-8') as f_snippet, open(vec_file, 'w', encoding='utf-8') as f_vec: 
        while True:
            vec_list = []
            line = f_snippet.readline()
            if line == '':
                break
            line = line.split('\t')
       
            for word in line[1:]:
                word = word.strip()
                if word in word_dict.keys():
                    vec_list.append(word_dict[word])
                else:
                    vec_list.append(str(0))
                    
            while True:
                if len(vec_list) >= threshold:
                    break
                vec_list.append(str(0))
                
            vec_list = vec_list[:threshold]
            
            txt_vec = ','.join(vec_list)
            print(line[0] + ',' + txt_vec, file=f_vec)
            


def make_dict(map_file, threshold):
    word_dict = {}
    with open(map_file, 'r', encoding='utf-8') as f_read:
        for _ in range(threshold):
            line = f_read.readline()
            if line == '':
                break
            line = line.split('\t')
            word_dict[line[1]] = line[0].strip()
    return word_dict
        

        
def main():
    map_file = sys.argv[1]
    snippet_file = sys.argv[2]
    vec_file = sys.argv[3]
    threshold = int(sys.argv[4])
    
    word_dict = make_dict(map_file, threshold)
    make_txt_vec(snippet_file, vec_file, word_dict, threshold)
    sys.exit(0)
    
    
if __name__ == '__main__':
    main()