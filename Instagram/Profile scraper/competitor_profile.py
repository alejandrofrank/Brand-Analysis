#!/usr/bin/env python
# coding: utf-8

# In[5]:


import instagram_scraper as insta
import sqlalchemy
from sqlalchemy import create_engine
import pandas as pd
import json
from datetime import date
import datetime
import time
import config

perfil_insta = ["cortefiel_official", 
                "scalperscompany", 
                "bluebananabrand", 
                "womensecretofficial", 
                "pedrodelhierro_official", 
                "fiftyoutlet_official", 
                "springfieldmw", 
                'goiko', 
                'sushiyakuza', 
                'goikobasics', 
                'zalando', 
                'zalando_man', 
                'superga_official', 
                'zara', 
                'pullandbear', 
                'massimodutti', 
                'oysho', 
                'silbon',
                'zarahome']
number_last_photos = 1
list_followers = []
list_fullname = []

dbtype = config.database_new['dbtype']
user = config.database_new['user']
password = config.database_new['password']
ip = config.database_new['ip']
port = config.database_new['port']
name = config.database_new['name']

engine = create_engine(f'{dbtype}://{user}:{password}@{ip}:{port}/{name}')

def get_metadata():
    imgScraper = insta.InstagramScraper(usernames=[perfil_insta[x]], maximum=number_last_photos, profile_metadata=True, media_metadata=True, latest=False, media_types=['none'])
    imgScraper.scrape()
    print ("scraped " + str(number_last_photos) + " from " + perfil_insta[x])
    
def scrape_data():
    with open(perfil_insta[x] + '/' + perfil_insta[x] + '.json', 'r', encoding = 'utf8') as data_file:    
        data = json.load(data_file)
    info = data['GraphProfileInfo']['info']
    list_followers.append(info['followers_count'])
    list_fullname.append(info['full_name'])
    return list_followers, list_fullname

def load_data(): 
    df = pd.DataFrame(list_followers, columns = ['followers']) 
    df['full_name'] = pd.Series(list_fullname)
    df['date'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    df.drop_duplicates(inplace = True)
    df_i = pd.read_sql_table('instagram_competitors', engine)
    df_bc = pd.concat([df_i, df], ignore_index=True)
    df_bc['date'] = pd.to_datetime(df_bc['date'])
    df_bc['date'] = pd.to_datetime(df_bc["date"].dt.strftime('%Y-%m-%d'))
    df['followers_difference'] = df.groupby('full_name')['followers'].diff()
    df['followers_difference'].fillna(0, inplace = True)
    df_bc.drop_duplicates(subset= ['date', 'full_name'], inplace = True, keep = 'last')
    df_bc.to_sql(name='instagram_competitors',con=engine, index=False, if_exists='replace', method='multi', chunksize=110)

def analyze_data():
    df = pd.read_sql_table('instagram_competitors', engine)
            
def main():
    get_metadata()
    scrape_data()
    load_data()
    
for x in range(len(perfil_insta)):
    main()
    time.sleep(1)

