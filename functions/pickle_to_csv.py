import pickle
import json
import pandas as pd

def pickle_to_csv():
  cat = ['price', 'volume', 'supply', 'marketcap', 'index']
  for c in cat:
      with open(f'data/{c}.pkl', 'rb') as f:
              dict_ = pickle.load(f)
      print(c)
      dates_retrieved = json.load(open('data/dates_retrieved.json'))


      columns_ = []
      data_ = []
      data_.append(dates_retrieved)
      columns_.append('date')
      for i in dict_:
          data_.append(dict_[i])
          columns_.append(i)

      df = pd.DataFrame(data_,index=columns_).T.set_index('date')
      df.to_csv(F'data/{c}.csv')