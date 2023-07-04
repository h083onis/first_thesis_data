import pandas as pd
import sys

def main():
    csv_path = sys.argv[1]
    project_name = csv_path.split('/')[-1].split('.')[0]
    df = pd.read_csv(csv_path, converters={'commit_hash':str, 'contains_bug':str}, low_memory=False)
    df = df[['commit_hash', 'contains_bug']]
    df.to_csv('../label/label_'+project_name+'.csv', index=None)
    sys.exit(0)
    
    
if __name__ == '__main__':
    main()
