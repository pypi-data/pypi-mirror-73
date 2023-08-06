import requests, os
import numpy as np
import pandas as pd

def SlackMe(text='',addtext='',channel='b',username='B.'):
  '''
  Notify me of terminated jobs
  '''
  url_hook = os.environ['SME_HOOKS']
  message = f"*~ {text}* notebook cell job in _{os.environ['PWD']}_ is now completed."
  if addtext!='':
    message = message+f"\n|_ Extra information:\n```{addtext}\n```"
    
  payload = f"{{\"text\": \"{message}\"}}"
  headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}
  r = requests.post(url_hook, data=payload, headers=headers)

def PrintPdColumns(df):
  '''
  Print all the columns of a pandas dataframe
  '''
  cols = [col for col in df.columns]
  print(cols)

def FlattenList(notflat_list):
  '''
  Pandas dataframs can contain array of arrays. Uncomfortable to create histograms from that. Flatten the column with this.
  '''
  flat_list = [item for sublist in notflat_list for item in sublist]
  return flat_list

def DecodeList(df,branch):
  '''
  Depending on the version of uproot some string might not be decoded (e.g., b'string'). If you want to decode a full panda column use this.
  '''
  df[branch] = [x.decode(encoding='UTF-8') for x in df[branch]]
  return df