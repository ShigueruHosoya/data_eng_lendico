#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
import json
import pandas as pd
from datetime import datetime
import time
from time import sleep
from itertools import chain
import sqlite3
import pytz

tz = pytz.timezone('America/Sao_Paulo')
date,date_db = datetime.now(tz=tz).strftime('%Y%m%d'),datetime.now(tz=tz).strftime('%Y-%m-%d')


# In[2]:


#Get api_key from file
try:
    with open('api.key','r') as api_file:
        api_key = api_file.read()
        api_file.close()
        if api_key == '':
            raise Exception('API_KEY does not exist.')
except FileNotFoundError as err:
    raise Exception('File or path is not specified.') from err


# In[3]:


#URLs and paths
queue_url = r"https://br1.api.riotgames.com/lol/league/v4/masterleagues/by-queue/RANKED_SOLO_5x5"
mastery_url = r"https://br1.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-summoner/"

path_daily = r'./masters_daily/'
path_ids = r'./masters_ids/'


# In[4]:


#Create sqlite connection
def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Exception as e:
        print(e)

    return conn


# In[5]:


# GET data
def get_urldata(url,summonerId=''):
    '''
    
    Get data from url based on queue_url or mastery_url (5x5 or summonerId)
       - summonerId: default is "", set a summonerId if data is from a specific summoner
       
    '''
    try:
        url = url + summonerId

        headers = {
          'X-Riot-Token': api_key
        }

        resp = requests.request("GET", url, headers=headers)
        data = json.loads(resp.text)

        if resp.status_code != 200:
            sleep(5)
            data = get_urldata(summonerId)
        
        return data
    except Exception as err:
        raise(err)


# In[6]:


# Data to .json
def export_rdata(path,date,data,summonerId='league'):
    '''
    
    Export data to .json files for 5x5 queue or summoner data(s).
    Will only return data if summonerId is not "league"
     - summonerId: default is "league", summonerId can be specified.
     - Specify a path for which type of data is being exported as .json.
    
    '''
    try:
        with open(path+f'masters_rankedsolo_{date}_{summonerId}.json','w+') as datafile:
            json.dump(data,datafile)
            datafile.close()
        if summonerId != 'league':
            return data
        else:
            return 0
    except Exception as err:
        raise(err)


# In[7]:


# Get 5x5 queue data 
queue_data = get_urldata(queue_url)

# Export 5x5 queue data into .json file 
export_rdata(path_daily,date,queue_data)

# Read queue data into dataframe 
queue_data = pd.read_json(json.dumps(queue_data))  


# In[8]:


# Exploded dict column values into columns 
exploded_data = pd.DataFrame(queue_data['entries'].values.tolist(), index=queue_data.index)

# Concatenate exploded data into queue_data to get tabular denormalized format 
tabular_data = pd.concat([queue_data,exploded_data],axis=1)
tabular_data.drop(columns='entries',inplace=True)

tabular_data['date'] = date_db

# Delete today's date and Insert into riot.db
conn = create_connection(r'.\db\riot.db')
cursor = conn.cursor()

cursor.execute("delete from masters_daily where date ='{}' ".format(date_db)) 

tabular_data.to_sql('masters_daily',con=conn,if_exists='append')

cursor.close()
conn.close()


# In[9]:


# List of only few summonerIds
test_data =tabular_data['summonerId'][0:5]


# In[10]:


# Get and store summonerId(s) data(s)
merged = [export_rdata(path_ids,date,get_urldata(mastery_url,_id),_id) for _index,_id in enumerate(test_data)]


# In[11]:


# Transform list of dict into dataframe
mastery_data = pd.DataFrame(list(chain.from_iterable(merged)))


# In[12]:


# Delete today's date and Insert into riot.db
conn = create_connection(r'.\db\riot.db')
cursor = conn.cursor()

cursor.execute("delete from summoner_table where date ='{}'".format(date_db)) 

mastery_data['date'] = date_db

mastery_data.to_sql('summoner_table',con=conn,if_exists='append')

cursor.close()
conn.close()


# In[13]:


# Get historical data from database and put as .csv for Power BI read (for no ODBC driver use)
conn = create_connection(r'.\db\riot.db')

stacked_data = pd.read_sql('select * from summoner_table',con=conn)

conn.close()

stacked_data.to_csv('pbix.csv',index=False)


# In[ ]:




