import sys

def out_snippet_to_txt(filename, idx, snippet_list):
    integrate_txt = ''
    cnt = 0
    with open(filename, 'a', encoding='utf-8') as f_snippet:
        for snippet in snippet_list:
            cnt += 1
            integrate_txt = idx + '-'+str(cnt) +'\t' + snippet
            print(integrate_txt, file=f_snippet)
