from __future__ import annotations
from airflow import DAG
from datetime import datetime, timedelta


import logging
import sys
import time
from pprint import pprint

import pendulum

from airflow.decorators import dag, task
from airflow.operators.python import is_venv_installed
from airflow.sensors.date_time import DateTimeSensor



@task(task_id="print_the_context")
def print_context(ds,execution_date, **kwargs):
    """Print the Airflow context and ds variable from the context."""
    pprint(kwargs)
    
    #if "execution_date" in kwargs:
    #    edate=kwargs["execution_date"]
    print(f"Got execution_date: {execution_date}")
    #print(f"Got execution_date: {next_execution_date}")
    tomorrow = kwargs['next_execution_date'] + timedelta(days=1)
    print(f"Gotot tomorrow execution_date: {tomorrow}")
    
    
    #print("{{ execution_date }}: {ds}")
    #print(ds)
    print(f"task now: {datetime.now()}")
    return "Whatever you return gets printed in the logs {{execution_date}}"

@task(task_id="delayed_task")
def run_delayed(execution_date):
    #trigger_date = execution_date + datetime.timedelta(minutes=3)
    print(f"task now: {datetime.now()}")
    
    




with DAG(dag_id="mv1",schedule=None,start_date=datetime(2024,1,1),catchup=False,tags=["examplemv"]) as dag:
    run_this = print_context()
    run_other = print_context()
    
    #execution_date.tomorrow()
    #DateTimeSniffer
    #sensor=DateTimeSensor(task_id="datetime_sensor",target_time="{{ execution_date.replace(minute=45) }}",mode="poke")
    
    run_this >>  run_other
    
    