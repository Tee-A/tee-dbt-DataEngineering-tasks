import requests
import time
import random
import json
import pandas as pd
from datetime import datetime, timedelta
from dotenv import load_dotenv
from airflow import DAG
import os
from datetime import datetime
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.operators.dagrun_operator import TriggerDagRunOperator
from airflow.utils.trigger_rule import TriggerRule
from sqlalchemy import create_engine
from pathlib import Path

 


load_dotenv(Path("/opt/airflow/config/.env"))
base_url = "https://api.nytimes.com/svc/books/v3/lists/overview.json"

results = {'published_date': [], 'list_id': [], 'list_name': [], 'display_name': [], 'age_group': [], 'author': [],
          'contributor': [], 'contributor_note': [], 'created_date': [], 'description': [], 'price': [], 'primary_isbn10': [], 
           'primary_isbn13': [], 'publisher': [], 'rank': [], 'title': [], 'updated_date': [], 'weeks_on_list': []}

     
def fetch_nyt_data(published_date):
    API_KEY = os.getenv('API_KEY')
    r = requests.get(f'{base_url}?published_date={published_date}&api-key={API_KEY}')
    data_fetched = r.json()

    return data_fetched


def fetch_nyt_rangeData(start_date, end_date):
    start_date = os.getenv('start_date')
    end_date = os.getenv('end_date')
    start = datetime.strptime(start_date, '%m-%d-%Y').date()
    end = datetime.strptime(end_date, '%m-%d-%Y').date()
    weeks_counter = (end-start).days//7
    for i in range(weeks_counter):
        print(i)
        n =random.randint(3,10) 
        time.sleep(n)
        print(start)
        start = start +timedelta(7)
        data = fetch_nyt_data(start)
        n =random.randint(8,12)
        time.sleep(n)
        result = data['results']
        published_date_extract = result['published_date']
        for list_ in data['results']['lists']:
            print(len(list_['books']))
            list_len = len(list_['books'])
            results['published_date'].extend([published_date_extract]*list_len)
            results['list_id'].extend([list_['list_id']]*list_len)
            results['list_name'].extend([list_['list_name']]*list_len)
            results['display_name'].extend([list_['display_name']]*list_len)
            results['age_group'].extend([list_data['age_group'] for list_data in list_['books']])
            results['author'].extend([list_data['author'] for list_data in list_['books']])
            results['contributor'].extend([list_data['contributor'] for list_data in list_['books']])
            results['contributor_note'].extend([list_data['contributor_note'] for list_data in list_['books']])
            results['created_date'].extend([list_data['created_date'] for list_data in list_['books']])
            results['description'].extend([list_data['description'] for list_data in list_['books']])
            results['price'].extend([list_data['price'] for list_data in list_['books']])
            results['primary_isbn10'].extend([list_data['primary_isbn10'] for list_data in list_['books']])
            results['primary_isbn13'].extend([list_data['primary_isbn13'] for list_data in list_['books']])
            results['publisher'].extend([list_data['publisher'] for list_data in list_['books']])
            results['rank'].extend([list_data['rank'] for list_data in list_['books']])
            results['title'].extend([list_data['title'] for list_data in list_['books']])
            results['updated_date'].extend([list_data['updated_date'] for list_data in list_['books']])
            results['weeks_on_list'].extend([list_data['weeks_on_list'] for list_data in list_['books']])
            #result_df = pd.DataFrame(results)
            #engine = create_engine('postgresql://postgres:postgres@host.docker.internal:5433/postgres')
            #result_df.to_sql('nyt_books', engine, schema='public', index=False, if_exists='append')
             
             
    result_df = pd.DataFrame(results)

    engine = create_engine('postgresql://postgres:postgres@localhost:5433/postgres') 

    result_df.to_sql('nyt_books', engine, schema='public', index=False, if_exists='replace')



with DAG('nyt_books_loader', start_date=datetime(2024,6,14), schedule_interval='@weekly',
         catchup=False) as dag:

        nyt_extract = PythonOperator(
               task_id="extract_books",
               python_callable=fetch_nyt_rangeData,
               op_args=["{{ ti.xcom_pull(task_ids='query_github_stats') }}",
                        "{{ ti.xcom_pull(task_ids='get_date') }}"]
               )

        my_dbt_dag = TriggerDagRunOperator(
                task_id='trigger_dbt_deel_task',
                trigger_dag_id='dbt_deel_task',
                trigger_rule=TriggerRule.ALL_SUCCESS,
                dag=dag
                )
        

nyt_extract >> my_dbt_dag
















