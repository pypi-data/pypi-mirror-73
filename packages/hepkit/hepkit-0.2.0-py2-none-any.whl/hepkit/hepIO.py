import uproot, pickle
import numpy as np
import pandas as pd

def PrintKeys(fileName):
  '''
  Check what's inside a root file
  '''
  for k in uproot.open(fileName).allkeys():
    print(k)
        
def OpenRoot(fileName,tree):
  '''
  Open a root file with uproot (to pandas dataframe)
  '''
  rTree = uproot.open(fileName)[tree]
  df = rTree.pandas.df(['*'],flatten=False,namedecode='utf-8')
  return df

def FromPickle(filename):
  return pickle.load(open(filename,'rb'))

def ToPickle(data,filename):
  pickle.dump(data, open(filename,'wb'))