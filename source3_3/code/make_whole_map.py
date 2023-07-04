import sys

def mapping(line, appear_dict):
    line = line.split('\t')
    for word in line[1:]:
        if word not in appear_dict.keys():
            appear_dict[word] = 1
        else:
            tmp = appear_dict.get(word) + 1
            appear_dict[word] = tmp

    return appear_dict


def des_sort(apper_dict):
    appear_list = sorted(apper_dict.items(), key= lambda word : word[1], reverse=True)
    return appear_list
    
def main():
    filepath = sys.argv[1]
    mapfile = sys.argv[2]
    appear_dict = {}
    with open(filepath, 'r', encoding='utf-8') as f_read:
        while True:
            line = f_read.readline().strip()
            if line == '':
                break
            appear_dict = mapping(line, appear_dict)
 
    appear_list = des_sort(appear_dict)
    
    with open(mapfile, 'w', encoding='utf-8') as f_map:
        for i in range(0, len(appear_list)):
            print(str(i+1) + '\t' + appear_list[i][0] + '\t' + str(appear_list[i][1]), file=f_map)
            
    sys.exit(0)
            
if __name__ == '__main__':
   main()  