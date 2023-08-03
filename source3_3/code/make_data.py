import sys
import pandas as pd

def assign_label(vec_file, label_file, data_file, threshold):
    column_list = ['commit_hash']
    column_list.extend([i for i in range(0, threshold)])
    vec_df = pd.read_csv(vec_file,
                         header=None,
                         names=column_list)
    label_df = pd.read_csv(label_file)
    data_df = pd.merge(vec_df, label_df, on='commit_hash', how='left')
    data_df = data_df[data_df['contains_bug'].notna()]
    print(data_df.shape[0])
    data_df['contains_bug'] = data_df['contains_bug'].astype(int)
    data_df.to_csv(data_file, index=False)
    
if __name__ == '__main__':
    vec_file = sys.argv[1]
    label_file = sys.argv[2]
    data_file = sys.argv[3]
    threshold = int(sys.argv[4])
    assign_label(vec_file, label_file, data_file, threshold)