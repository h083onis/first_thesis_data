import sys

def mapping(line, appear_dict):
    for word in line[1:]:
        if word not in appear_dict.keys():
            appear_dict[word] = 1
        else:
            tmp = appear_dict.get(word) + 1
            appear_dict[word] = tmp

    return appear_dict

def des_sort(apper_dict):
    #出現回数が同じ場合は最初に出現した単語のほうが上にくる
    appear_list = sorted(apper_dict.items(), key= lambda word : word[1], reverse=True)
    return appear_list

    
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
                    vec_list.append(str(threshold+1))
                    
            while True:
                if len(vec_list) > threshold:
                    break
                vec_list.append(str(0))
            vec_list = vec_list[:threshold]
            txt_vec = ','.join(vec_list)
            print(line[0] + ',' + txt_vec, file=f_vec)

def main():
    snippet_file = sys.argv[1]
    vec_file = sys.argv[2]
    threshold = int(sys.argv[3])
    appear_dict = {}
    with open(snippet_file, 'r', encoding='utf-8') as f_read:
        while True:
            line = f_read.readline().strip()
            if line == '':
                break
            line = line.split('\t')
            if len(line[1:]) > threshold:
                line = line[:threshold+1]
            appear_dict = mapping(line, appear_dict)
 
    appear_list = des_sort(appear_dict)
    
    word_dict = {word[0] : str(i) for i , word in enumerate(appear_list[:threshold], 1)}
    make_txt_vec(snippet_file, vec_file, word_dict, threshold)
   
    sys.exit(0)
    
if __name__ == '__main__':
    main()