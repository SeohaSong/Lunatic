import pandas as pd
import numpy as np


if __name__ == '__main__':

    df = pd.read_pickle('./data/df')

    total_size = len(df)
    batch_size = 8192
    batch_n = (total_size // batch_size)+([0, 1][total_size % batch_size > 0])

    idxs = np.random.choice(range(total_size), total_size, replace=False)
    df = df.loc[idxs]
    tokens, trues = np.array(df['token'].tolist()), np.array(df['true']).reshape(-1, 1)

    batches = [
        {
            'X': tokens[i*batch_size:(i+1)*batch_size],
            'Y': trues[i*batch_size:(i+1)*batch_size]
        } for i in range(batch_n)
    ]

    pd.to_pickle(batches, './data/batches')