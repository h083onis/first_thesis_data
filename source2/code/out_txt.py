import sys

def make_before_after_txt(text_name):
    with open(text_name, 'w', encoding='utf-8') as f:
        f.truncate(0)
        f.seek(0)
        while True:
            try :
                line = input()
                print(line, file=f)
                 
            except EOFError:
                break
        
        
           
def main():
    # if len(sys.argv) != 3:
    #     print(f'Usage: python repo_path:{sys.argv[0]}')
    #     sys.exit(0)
    make_before_after_txt(sys.argv[1])
    sys.exit(0)
    
    
if __name__ == '__main__':
    main()