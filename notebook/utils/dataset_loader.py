import pandas as pd

def load_raw_dataset(path: str = '../data/blog_authorship_corpus.csv'):
    df = pd.read_csv(path)
    
    df = df.dropna()
    df['tokens'] = df.text.str.split(' ').apply(lambda s: len(s))
    df = df[(df['tokens'] > 2) & (df['tokens'] <= 1000)]
    df = df[~df['text'].str.contains(r'[^\x00-\x7F]')]
    df = df.rename(columns={'id': 'user_id'})
    df = df[['gender', 'text', 'user_id']]
    df['text'] = df['text'].str.replace('&nbsp;', ' ', case=False, regex=False)
    
    return df