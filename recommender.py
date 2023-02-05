import pandas as pd
import numpy as np
import statistics
from scipy.spatial import distance
from surprise import Dataset
from surprise import Reader

#-------------------------------------------------------------------------------
# Ajeitando os dados
dados = pd.read_csv("algoritmo - Base.csv")
dados.dropna(axis=0, inplace=True, how='all')
dados_livros = dados.query('read == 1')[['book_cod', 'q1', 'q2', 'q3', 'q4', 'q5', 'rank']]

# Calculando os centros
def weighted_average(dataframe, value, weight):
    val = dataframe[value]
    wt = dataframe[weight]
    return (val * wt).sum() / wt.sum()

df1 = dados_livros.groupby('book_cod').apply(weighted_average, 'q1', 'rank')
df2 = dados_livros.groupby('book_cod').apply(weighted_average, 'q2', 'rank')
df3 = dados_livros.groupby('book_cod').apply(weighted_average, 'q3', 'rank')
df4 = dados_livros.groupby('book_cod').apply(weighted_average, 'q4', 'rank')
df5 = dados_livros.groupby('book_cod').apply(weighted_average, 'q5', 'rank')
centro_livros = pd.concat([df1, df2, df3, df4, df5], axis=1, ignore_index=True).reset_index().to_numpy()

# Funções de recomendação bruta
def distance_weight(vector1, vector2, weight):
  s = 0
  p = 0
  while p < len(vector1):
    _ = ((vector1[p] - vector2[p]) ** 2) * weight[p]
    s += _
    p += 1
  return np.sqrt(s) / sum(weight)

def rec_w(context, weight=None):
  w = [1/2] * 5
  if weight != None:
    w[weight] = 2
  else:
    pass
  R = []
  for cent in centro_livros:
    if context[-1] == 0:
      d = distance_weight(context, cent[1:], w)
    else:
      d = distance_weight(context[:-1], cent[1:-1], w[:-1])
    t = (cent[0], d)
    R.append(t)
  dt = np.dtype([('book_cod', int), ('center', float)])
  return np.array(R, dtype=dt)
#-------------------------------------------------------------------------------
# Montando o modelo de recomendação CF
from surprise import Dataset
from surprise import Reader

df = dados.query('read == 1')[['name_cod', 'book_cod', 'rank']]
reader = Reader(rating_scale=(1, 5))

data = Dataset.load_from_df(df, reader)
from surprise import KNNWithMeans
from surprise import KNNWithZScore
from surprise import KNNBaseline

# To use item-based cosine similarity
sim_options = {
    "name": "cosine",
    "user_based": False,  # Compute  similarities between items
}

algo = KNNBaseline(k = 30, min_k = 3, sim_options=sim_options, random_state = 42, verbose=False)
trainset = data.build_full_trainset()
algo.fit(trainset)

def rating(name_cod, book_cod):
  prediction = algo.predict(name_cod, book_cod)
  return prediction.est
#-------------------------------------------------------------------------------
def reccomendation_list(name_cod, context, weight=None, repeat = 0):
  # Separando as listas com poucas e muitas avaliações
  amount = dados.query('read == 1').pivot_table(index=['book_cod', 'book_name'], values='read', aggfunc='sum').sort_values('read', ascending=False)
  amount.reset_index(inplace=True)
  amount.rename(columns = {'read': 'notes'}, inplace=True)
  avg_notes = amount['notes'].median()
  high_valuations = amount.query('notes >= @avg_notes')
  low_valuations = amount.query('notes < @avg_notes')

  # Fazendo a recomendação bruta
  c = np.array(context)
  w = weight
  Distances = pd.DataFrame(rec_w(c, w)).sort_values(by='book_cod', ascending=True)

  # Atribuindo as distâncias para cada uma das listas
  high_valuations = high_valuations.set_index('book_cod').join(Distances.set_index('book_cod'), lsuffix='_caller').sort_values(by='center')
  low_valuations = low_valuations.set_index('book_cod').join(Distances.set_index('book_cod'), lsuffix='_caller').sort_values(by='center')

  # Consolidando o output de recomendação com base na média
  metric_centers = high_valuations['center'].min()
  newlow_valuations = low_valuations.query('center <= @metric_centers')
  context_output = pd.concat([high_valuations, newlow_valuations]).sort_values(by='center')

  if repeat == 0:
    lista = dados.query('name_cod == @name_cod and read == 0').set_index('book_cod').join(context_output, how='inner', lsuffix='_caller').sort_values(by='center').reset_index()[['name_cod', 'name', 'book_cod', 'book_name', 'book_author', 'center']]
  else:
    lista = dados.query('name_cod == @name_cod').set_index('book_cod').join(context_output, how='inner', lsuffix='_caller').sort_values(by='center').reset_index()[['name_cod', 'name', 'book_cod', 'book_name', 'book_author', 'center']]
  L = []
  for i, X in lista.iterrows():
    _ = rating(lista['name_cod'][i], lista['book_cod'][i])
    L.append(_)
  lista['rating'] = L
  lista['score'] = lista['rating'] / lista['center']
  return lista.sort_values(by='score', ascending=False).head(5)
#-------------------------------------------------------------------------------