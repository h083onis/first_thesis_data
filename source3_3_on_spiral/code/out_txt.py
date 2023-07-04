import sys

def out_txt(filename, text):
    with open(filename, 'w', encoding='utf-8') as f:
        f.truncate(0)
        f.seek(0)
        text_list = text.split('\r\n')
        for text in text_list:
            print(text, file=f)
    
        