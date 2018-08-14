import pandas as pd
import sys

import konlpy


def get_df1(df, iter_=0):

    len_ = len(df)
    
    def get_pos(text):
        
        pos = konlpy.tag.Mecab().pos(text)
        pos = ['-'.join(w8t) for w8t in pos]
        
        nonlocal iter_
        iter_ += 1
        sys.stdout.write("\r% 5.2f%%" % (iter_/len_*100))
        
        return pos

    poses = [get_pos(text) for text in df['text']]
    df = df.drop(['text'], axis=1)
    df['pos'] = poses
    print()
    
    return df


if __name__ == '__main__':

    df = pd.read_pickle('./data/df0')
    df = get_df1(df)

    pd.to_pickle(df, './data/df1')
