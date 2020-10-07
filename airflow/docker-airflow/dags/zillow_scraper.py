"""
Code that goes along with the Airflow located at:
http://airflow.readthedocs.org/en/latest/tutorial.html
"""
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
from crawlers_file.zillow_crawl import ZillowCrawler 





default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(2020, 9, 20),
    "email": ["airflow@airflow.com"],
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
    # 'queue': 'bash_queue',
    # 'pool': 'backfill',
    # 'priority_weight': 10,
    # 'end_date': datetime(2016, 1, 1),
}


def zip_code_reader():
    file = open('dags/zip_codes.csv', 'r')
    zip_codes = [line.strip() for line in file.readlines()]
    return zip_codes

def zillow_scrape(zip_codes):
    crawl = ZillowCrawler(zip_codes)





dag = DAG("zillow", default_args=default_args, schedule_interval='07 7 * * *')

# t1, t2 and t3 are examples of tasks created by instantiating operators
starting_date = BashOperator(task_id="print_date", bash_command="date", dag=dag)

zillow_scrape_task = PythonOperator(task_id="hello", python_callable=zillow_scrape ,op_kwargs={'zip_codes':zip_code_reader()}, dag=dag )


zillow_scrape_task.set_upstream(starting_date)
