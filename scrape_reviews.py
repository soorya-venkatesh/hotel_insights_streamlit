from outscraper import ApiClient
import time
import os
import pandas as pd
import datetime


try:
    client = ApiClient(api_key=os.environ['OUTSCRAPPER_KEY'])
except KeyError:
    raise('Loading secret outscrapper failed.')

df=pd.read_csv('sadhabishegam_reviews1.csv')
df['review_date']=pd.to_datetime(df['review_date'])
df=df.sort_values('review_date',ascending=False).reset_index(drop=True)
latest_date=int(df['review_date'].loc[0].timestamp())

client = ApiClient(api_key=os.environ['OUTSCRAPPER_KEY'])

results = client.google_maps_reviews(['ChIJ6arCErzfVDoRvcoVZwi9Tvk'], reviews_limit=25,cutoff=latest_date,language='en',sort='newest',async_request=True)
attempts = 5 # retry 5 times
while attempts: # stop when no more attempts are left or when no more running request ids
    attempts -= 1
    time.sleep(60)

    
    outscrapper_result = client.get_request_archive(results['id'])
    # result = client.get_request_archive('a-22b81a6f-fbec-4f62-87b6-66ad431cec5f')
    print(outscrapper_result['status'])

    if outscrapper_result['status'] == 'Success':
        break

new_df=pd.DataFrame(columns=['review_rating','review_date'],index=range(len(outscrapper_result['data'][0]['reviews_data'])))
for id,element in enumerate(outscrapper_result['data'][0]['reviews_data']):
    # new_df.loc[id,'review_id']=element['review_id']
    new_df.loc[id,'review_rating']=element['review_rating']
    new_df.loc[id,'review_date']=element['review_datetime_utc']
    # new_df.loc[id,'review_text']=element['review_text']

df=pd.concat([df, new_df], ignore_index=True, sort=False)
df.to_csv('sadhabishegam_reviews1.csv',index=False)