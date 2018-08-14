import pandas as pd
import re

from gensim.models import Word2Vec
import tensorflow as tf
from flask import Flask, request
import konlpy


def get_score(text, word2idx, X, output):
    text = re.sub(r'[^\w,.!?\s]', '', text)
    pos = konlpy.tag.Mecab().pos(text)
    poses = ['-'.join(w8t) for w8t in pos]
    token = []
    for pos in poses:
        try:
            token.append(word2idx[pos])
        except:
            pass
    token = token+token_ph[len(token):]
    score = sess.run(output, feed_dict={X: [token]})
    score = str(score[0][0]**(4/3))
    return score


app = Flask(__name__)


sess=tf.Session()
saver = tf.train.import_meta_graph('./data/checkpoint/model.meta')
saver.restore(sess, tf.train.latest_checkpoint('./data/checkpoint'))
g = sess.graph


X = g.get_tensor_by_name('Placeholder:0')
output = g.get_tensor_by_name('dense_1/Sigmoid:0')


model = Word2Vec.load('./data/w2v_model')
words = model.wv.index2word
word2idx = {word: i for i, word in enumerate(words)}
token_ph = [len(words)]*150


@app.route('/', methods=['GET'])
def hello_world():
    text = request.args.get('text')
    score = get_score(text, word2idx, X, output)
    return score