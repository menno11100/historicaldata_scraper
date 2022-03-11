import pickle
import json
dict_ = dict()

def start_over():
  dates_retrieved = []
  with open('data/price.pkl', 'wb') as handle:
      pickle.dump(dict_, handle, protocol=pickle.HIGHEST_PROTOCOL)
  with open('data/volume.pkl', 'wb') as handle:
      pickle.dump(dict_, handle, protocol=pickle.HIGHEST_PROTOCOL) 
  with open('data/supply.pkl', 'wb') as handle:
      pickle.dump(dict_, handle, protocol=pickle.HIGHEST_PROTOCOL)   
  with open('data/marketcap.pkl', 'wb') as handle:
      pickle.dump(dict_, handle, protocol=pickle.HIGHEST_PROTOCOL)   
  with open('data/index.pkl', 'wb') as handle:
      pickle.dump(dict_, handle, protocol=pickle.HIGHEST_PROTOCOL)  
      
  with open('data/dates_retrieved.json', 'w') as fp:
      json.dump(dates_retrieved, fp,  indent=4)