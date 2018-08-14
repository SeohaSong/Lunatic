import pandas as pd
import numpy as np
import sys
import re


def get_df0(df, iter_=0):

    len_ = len(df)
    
    def process(text, skip=False):
        text = str(text)
        if not 20 < len(re.sub(r'\s+', '', text)) <= 200:
            skip = True
        if not skip and re.compile(r'[^\w,.!?\s]').search(text):
            skip = True
        if not skip and re.compile(r'[a-zA-Zㄱ-ㅎㅏ-ㅣ]').search(text):
            skip = True
        if not skip and re.compile(r'(.+?)\1{3}').search(text):
            skip = True
        if not skip:
            text = re.sub(r'\s+', ' ', text)
            text = re.sub(r'^\s', '', text)
            text = re.sub(r'\s$', '', text)
        else:
            text = ''
            
        nonlocal iter_
        iter_ += 1
        sys.stdout.write("\r% 5.2f%%"%(iter_/len_*100))
        
        return text

    texts = [process(t) for t in df['text']]
    print()

    df['text'] = texts
    df = df[df['text'] != '']
    df = df.reset_index(drop=True)
    
    return df
    

if __name__ == '__main__':
    
    df = pd.read_csv('./data/watcha_movie_review.csv')
    df = df[df['point'] > 0]

    df = get_df0(df)

    pd.to_pickle(df, './data/df0')
