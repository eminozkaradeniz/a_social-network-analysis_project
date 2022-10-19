# -*- coding: utf-8 -*-
"""
Created on Thu Jun 17 23:44:30 2021

@author: emin
"""
import pandas as pd
from bs4 import BeautifulSoup
import requests
import time


# uygun formatta olmayan linkleri temizleme fonksiyonu
def del_links(d, urls=None, name=''):
    if urls is None:
        urls = []
    lst = []
    for url in d:
        if ('.pdf' in url or f'{name}/#' in url or '.php' in url or '.mp4' in url
                or '.xls' in url or '.doc' in url or '.jpg' in url):
            continue
        elif name == url or 'deu.edu.tr' not in url:
            continue
        elif url in urls:
            continue
        elif 'wp-content' in url:
            continue
        else:
            lst.append(url)
    return lst


# bir html dosyasının içindeki tüm linkleri bulan fonksiyon
def get_all_links(content):
    soup = BeautifulSoup(content, 'lxml')
    links = list()
    for link in soup.findAll('a'):
        links.append(link.get('href'))
    links = list(set(links))
    if None in links:
        links.remove(None)
    return links


# html dosyasında tagler dışındaki tüm içerikleri çıkartan fonksiyon
def extract_words(content):
    soup = BeautifulSoup(html)
    for script in soup(['script', 'style']):
        script.decompose()
    strips = list(soup.stripped_strings)
    return ' '.join(strips)


# html dosyaları internetten çekilip dosyalara yazdırılıyor.
with open('../html_files/0.html', 'r', encoding='utf8') as f:
    html = f.read()

df_list = [['https://www.deu.edu.tr/', html]]
links = get_all_links(html)
links = del_links(links)

for link in links:
    start = time.time()
    try:
        res = requests.get(link)
    except:
        continue

    if res.status_code == 200:
        df_list.append([link, res.text])
        print(f'{link}: \t\t\t {time.time() - start} sec.')
    time.sleep(0.25)

df = pd.DataFrame(data=df_list, columns=['url', 'html'])

# 2
htmls = list(df['html'])

for i in range(1, len(htmls)):
    urls = list(df['url'])[1:]
    links = get_all_links(htmls[i])
    links = del_links(links, urls, name=urls[i])

    df_list = []
    for link in links:
        start = time.time()

        try:
            res = requests.get(link)
        except:
            continue

        if res.status_code == 200:
            stop = time.time() - start
            if stop < 3.0:
                print(f'{link}:\t take {stop} sec.')
                df_list.append([link, res.text])

        time.sleep(0.25)
    df_new = pd.DataFrame(df_list, columns=df.columns)
    df = pd.concat([df, df_new], axis=0, ignore_index=True)

########################


# 3
n = len(htmls)
htmls = df['html']

for i in range(n, len(htmls)):
    urls = df['url'][n:]
    links = get_all_links(htmls[i])
    links = del_links(links, urls, name=urls[i])

    df_list = []
    for link in links:
        start = time.time()

        try:
            res = requests.get(link)
        except:
            continue

        if res.status_code == 200:
            stop = time.time() - start

        if stop < 3.01:
            print(f'{link}:\t take {stop} sec.')
            df_list.append([link, res.text])

    df_new = pd.DataFrame(df_list, columns=df.columns)
    df = pd.concat([df, df_new], axis=0, ignore_index=True)

    time.sleep(0.25)

# html'lerin içindeki tüm içerik çıkartılıyor.
df['content'] = df['html'].apply(extract_words)

# tüm url ler dosyaya yazdırılıyor.
urls = df['url']
urls.to_csv('../urls.csv', index=False)

# tüm html ler dosyaya yazdırılıyor.
for i in range(1, len(df)):
    with open(f'../html_files/{i}.html', mode='w') as f:
        f.write(df['html'][i])

# çıkartılan metinler dosyaya yazdırılıyor.
for i in range(0, len(df)):
    with open(f'../contents/{i}.txt', mode='w') as f:
        f.write(df['content'][i])

# ağ için düğümler ve kenarlar belirleniyor ve Gephi programında
# kullanılmak üzere dosyaya yazdırılıyor..

lst = []
urls = list(urls)
for i in range(len(df)):
    html = df.iloc[i]['html']
    links = get_all_links(html)
    links = del_links(links, urls)

    for link in links:
        try:
            index = urls.index(f'{link}')
            lst.append([i, index])
        except ValueError:
            continue

df2 = pd.DataFrame(data=lst, columns=['Source', 'Target'])

df3 = df['url'].reset_index()
df3.columns = ['id', 'label']

df2.to_csv('../graphs/gephi/edges.csv', index=False)
df3.to_csv('../graphs/gephi/nodes.csv', index=False)
