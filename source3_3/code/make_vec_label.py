import pandas as pd

def make_vec_label(hexshafile, labelfile, vecfile):
    hexsha_df = pd.read_text(hexshafile)
    label_df = pd.read_csv(labelfile)
    vec_df = pd.read_text(vecfile)
    
    hexsha_df = hexsha_df['']
    
    
    