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



@task(task_id="print_the_context", trigger_rule="all_success") 
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

# @task(task_id="delayed_task")
# def run_delayed(execution_date):
#     #trigger_date = execution_date + datetime.timedelta(minutes=3)
#     print(f"task now: {datetime.now()}")
    
    

from airflow.providers.ssh.operators.ssh import SSHOperator
from airflow.providers.sftp.sensors.sftp import SFTPSensor

#Use Admin / Connection to create a new ssh sftp connection using in extras { "key_file" : "/path/tp/keyfile"}

with DAG(dag_id="mv1",schedule=None,start_date=datetime(2024,1,1),catchup=False,tags=["examplemv"]) as dag:
    run_this = print_context()
    run_other = print_context()

    ssh_task = SSHOperator(
    task_id='ssh_task',
    ssh_conn_id='ssh2aws',
    command='/home/cloud_user/bin/job_success'
    )
    
    ssh_task_error = SSHOperator(
    task_id='ssh_task_error',
    ssh_conn_id='ssh2aws',
    command='/home/cloud_user/bin/job_error'
    )

    #FileSniffer
    sftp_with_operator = SFTPSensor(task_id="sftp_operator", path="/home/cloud_user/bin/touchfile", poke_interval=10, timeout=30,sftp_conn_id="sftp2aws")
    
    #execution_date.tomorrow()
    #DateTimeSniffer
    #sensor=DateTimeSensor(task_id="datetime_sensor",target_time="{{ execution_date.replace(minute=45) }}",mode="poke")
    
    
    all_start = [run_this, ssh_task, ssh_task_error]
    sftp_with_operator >> all_start
    
    
    all_start >> run_other
    
    