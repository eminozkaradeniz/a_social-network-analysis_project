# -*- coding: utf-8 -*-
"""
Created on Sat Jun 26 00:26:02 2021

@author: emin
"""
import pandas as pd
import networkx as nx

# https://networkx.org/documentation/stable/reference/algorithms/centrality.html

edges = pd.read_csv('../graphs/gephi/edges.csv')
nodes = pd.read_csv('../graphs/gephi/nodes.csv')

# Graf oluşturulup düğümler ve kenarlar grafa ekleniyor.
G = nx.Graph()

for n_id in nodes['id']:
    G.add_node(n_id)

for i in range(len(edges)):
    G.add_edge(edges['Source'][i], edges['Target'][i])

# Degree Centrality tablosu hesaplatılıp dosyaya yazdırılıyor.
dc = nx.degree_centrality(G)

lst = []
for i in range(len(nodes)):
    lst.append([nodes['label'][i], dc[i]])

df = pd.DataFrame(data=lst, columns=['Web Page', 'Degree Centrality'])
df.sort_values(by='Degree Centrality', ascending=False, inplace=True)
df.to_csv('../Centrality_Tables/degree_centrality.csv', index=False)

# Betweenness Centrality tablosu hesaplatılıp dosyaya yazdırılıyor.
bc = nx.betweenness_centrality(G)

lst = []
for i in range(len(nodes)):
    lst.append([nodes['label'][i], bc[i]])

df = pd.DataFrame(data=lst, columns=['Web Page', 'Betweenness Centrality'])
df.sort_values(by='Betweenness Centrality', ascending=False, inplace=True)
df.to_csv('../Centrality_Tables/betweenness_centrality.csv', index=False)

# Closeness Centrality tablosu hesaplatılıp dosyaya yazdırılıyor.
cc = nx.closeness_centrality(G)

lst = []
for i in range(len(nodes)):
    lst.append([nodes['label'][i], cc[i]])

df = pd.DataFrame(data=lst, columns=['Web Page', 'Closeness Centrality'])
df.sort_values(by='Closeness Centrality', ascending=False, inplace=True)
df.to_csv('../Centrality_Tables/closeness_centrality.csv', index=False)
