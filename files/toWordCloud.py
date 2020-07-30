from konlpy.tag import Okt
from tqdm import tqdm
from nltk import FreqDist
from wordcloud import WordCloud
from datetime import datetime
import pandas as pd
import matplotlib.pylab as plt

import pymongo

import requests, json


client = pymongo.MongoClient("mongodb://")
result_nate = client['nate'].article
result_daum = client['daum'].article
result_naver = client['naver'].article

df_nate = pd.DataFrame(list(result_nate.find()))
df_daum = pd.DataFrame(list(result_daum.find()))
df_naver = pd.DataFrame(list(result_naver.find()))

df = df_nate.append(df_daum)
df = df.append(df_naver).reset_index()

df = df.drop(['index', '_id'], axis=1)


def tokenize(doc):
    tagger = Okt()
    tokens = [t for t in tagger.nouns(doc)]
    return tokens

def towordcloud(df):
    df = df.dropna()
    docs = tuple([x for x in df.to_numpy()])
    sentences = []
    for d in tqdm(docs):
        tokens = [token for token in tokenize(d) if token.isalnum()]
        sentences.append(tokens)
    words = [word for sentence in sentences for word in sentence]
    words = [word for word in words if len(word) > 1]
    words_remove = ['으로', '에서', '에도', '했다', '있다', '이다', '무단', '배포', '위해', '대표', '때문', 
                    '그룹', '통해', '최근', '경우', '이번', '이후', '라며', '지난', '대해', '기자', '관련',
                   ]
    words_r = [word for word in words if word not in words_remove]
    fd = FreqDist(words_r)
#     print(fd.most_common(20))
    font_path = '/home/ubuntu/python3/Crawling/koverwatch.ttf'
    wc = WordCloud(width=1000, height=600, background_color="white", random_state=0,
                  font_path=font_path)
    plt.imshow(wc.generate_from_frequencies(fd))
    plt.axis("off")
#    str = "/home/ubuntu/python3/Crawling/wordcloud_" + datetime.now().strftime("%Y.%m.%d_%H.%M.%S") + ".png"
#    plt.savefig(str)
    plt.savefig('/home/ubuntu/python3/Crawling/wordcloud.png')
#    plt.show()

towordcloud(df['content'])
