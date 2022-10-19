# -*- coding: utf-8 -*-
"""
Created on Sat Jun 19 23:45:49 2021

@author: emin
"""

import os
import re
import numpy as np
import pandas as pd
from string import digits
from collections import Counter
from nltk.corpus import stopwords

# türkçe STOPWORDS'ler dosyadan alınıyor.
with open('../stop-words/turkish.txt', mode='r', encoding='utf-8') as f:
    STOPWORDS = f.read().splitlines()

remove_digits = str.maketrans('', '', digits)

# html dosyalarından çıkartılmış metinler dosyadan alınıyor.
lst = []
for filename in os.listdir('../contents'):
    with open(f'../contents/{filename}', mode='r', encoding='utf-8') as f:
        lst.append(f.read())

df = pd.DataFrame(pd.Series(lst), columns=['text'])


# sayfa içeriklerindeki sözcüklerin çıkartılması için bir fonksiyon tanımlanıyor.
def text_process(content: str) -> list:
    content = content.lower()
    content = content.translate(remove_digits)
    content = re.sub(r'[^\w\s]', '', content)
    words = [word for word in content.split() if word not in STOPWORDS
             and len(word) > 2 and word not in stopwords.words('english')]
    return words


# tüm sayfa içerikleri text_process fonksiyonuna gönderilip sözcükler listesi haline getirtiliyor.
df['content'] = df['content'].apply(text_process)

# tüm sözcükler bir kümeye alınıyor.
all_words = set()
for content in df['content']:
    for word in content:
        all_words.add(word)

all_words = list(all_words)

# her sözcüğün her içerik için frekansı hesaplanıyor.
sparse = pd.DataFrame(data=np.zeros((len(df), len(all_words))), columns=all_words)

for text_i in range(len(df)):
    words = set(df['content'][text_i])
    for word in words:
        sparse[word][text_i] += Counter(df['content'][text_i])[word]

del df

# her sözcüğün toplam frekansı ve web sayfası frekansı tablosu daha sonra
# datavisu.al sitesinde grafik oluşturmak için dosyaya yazdırılıyor
lst = []
for word in all_words:
    freq = sum(sparse[word])
    if freq >= 5:
        web_page = len(sparse[sparse[word] > 0][word])
        lst.append([word, freq, web_page])

df = pd.DataFrame(data=lst, columns=['Word', 'Frequency', 'Web Page'])
df.sort_values(by=['Frequency'], ascending=False, inplace=True)
df.set_index('Word', inplace=True)

del sparse
df.to_csv('../graphs/words/words.csv')
