from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
import pandas as pd
import os
import hashlib
from scripts.data_cleaning_and_validation import data_cleaning_and_validation

from airflow.providers.docker.operators.docker import DockerOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.sensors.sql import SqlSensor

# define default arguments
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2022, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

# define DAG
dag = DAG(
    'membership_application_pipeline',
    default_args=default_args,
    description='A DAG to process membership applications submitted by users on an hourly interval',
    schedule_interval='@hourly',
    catchup=False
)

# define task
process_applications_task = PythonOperator(
    task_id='process_applications',
    python_callable=data_cleaning_and_validation,
    provide_context=True,
    dag=dag
)

create_database_container = DockerOperator(
    task_id='create_database_container',
    image='postgres',
    dockerfile='govtech/database/Dockerfile',
    command='postgres -c logging_collector=on',
    network_mode='bridge',
    auto_remove=True,
    tty=True,
    dag=dag,
)

initialize_database = PostgresOperator(
    task_id='initialize_database',
    postgres_conn_id='postgres_default',
    sql='govtech/database/init.sql',
    dag=dag,
)

wait_for_database = SqlSensor(
    task_id='wait_for_database',
    conn_id='postgres_default',
    sql='SELECT 1',
    dag=dag,
)

# set task dependencies
process_applications_task >> create_database_container
