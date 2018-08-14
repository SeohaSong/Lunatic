import pandas as pd
import numpy as np
import sys
import os

from gensim.models import Word2Vec


def save_model(df):
        
    model = Word2Vec(
        df['pos'].tolist(),
        size=128,
        window=4,
        min_count=1,
        workers=(os.cpu_count()//2),
        iter=4
    )

    model.save("./data/w2v_model")
    
    return model


def get_df(df, model):
    
    len_ = len(df)

    words = model.wv.index2word
    word2idx = {word: i for i, word in enumerate(words)}

    token_ph = [len(words)]*max(len(pos) for pos in df['pos'])
    
    tokens = []
    for iter_, pos in enumerate(df['pos']):
        token = [word2idx[word] for word in pos]
        tokens.append(token+token_ph[len(token):])
        iter_ += 1
        sys.stdout.write("\r% 5.2f%%" % (iter_/len_*100))
    print()

    df = df.drop(['pos'], axis=1)
    df['token'] = tokens
    df['true'] = df['point']/max(df['point'])
    df = df.drop(['point'], axis=1)
    
    return df


def get_lookup(df, model):
        
    words = model.wv.index2word
    iter_, len_ = 0, len(words)
    
    lookup = np.zeros([len(words)+1, len(model.wv.word_vec(words[0]))])

    for word in words:
        lookup[iter_] = model.wv.word_vec(word)
        iter_ += 1
        sys.stdout.write("\r% 5.2f%%" % (iter_/len_*100))
    print()

    return lookup
    
    
if __name__ == '__main__':
    
    df = pd.read_pickle('./data/df1')

    model = save_model(df)
    df = get_df(df, model)
    lookup = get_lookup(df, model)
    
    pd.to_pickle(df, './data/df')
    pd.to_pickle(lookup, './data/lookup')
