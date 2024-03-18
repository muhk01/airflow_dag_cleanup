from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.bash_operator import BashOperator
from airflow.utils.task_group import TaskGroup
from datetime import datetime, timedelta
from airflow.models import Variable

# Base Airflow DAGs
BASE_LOG_FOLDER="/your-path-to/airflow/logs"
RETENTION=90

# Fetch Credential
airflow_creds = 'airflow_creds'
creds_val = Variable.get(airflow_creds)

# List Airflow known Hosts
LIST_HOST = [{"alias": "dev-airflow-1", "host": "172.172.172.1"}, 
            {"alias": "dev-airflow-2", "host": "172.172.172.2"}]

cleanup_command_template = """
SSH_COMMAND="/usr/bin/sshpass -p {creds_val} ssh -v your-hostname@{host}"
DELETE_LOG=$($SSH_COMMAND -t 'find {log_folder}/*/* -name '*.log' -type f -mtime +{retention_time} -delete')
echo "Log Deletion .."
echo "$DELETE_LOG"
DELETE_EMPTY_FOLDER=$($SSH_COMMAND -t 'find {log_folder}/*/ -empty -type d -delete')
echo "$DELETE_EMPTY_FOLDER"
echo "complete delete empty folder"
"""


# define the DAG
with DAG(
    "temp_DAG_Log_CleanUp",
    default_args = {
        'owner': 'airflow',
        'email_on_failure': False,
        'email_on_retry': False,
        'retries': 2,
        'retry_delay': timedelta(seconds=30)
    },

    start_date=datetime(2023, 12, 6, 0, 0, 0),
    schedule_interval='0 0 6 * *',
    max_active_runs=1,
    catchup=False,
    tags=['daily']
    #max_active_tasks=11,
    ) as dag:

    log_cleaning_start = DummyOperator(task_id="log_cleaning_start")

    with TaskGroup(group_id="group_airflow_log_cleaning") as group_airflow_log_cleaning:
        for host in LIST_HOST:
            dag_cleaning = BashOperator(
                task_id=f"dag_cleaning_of_{host['alias']}",
                bash_command=cleanup_command_template.format(creds_val=creds_val, host=host['host'], log_folder=BASE_LOG_FOLDER, retention_time=RETENTION),
                dag=dag,
            )

    log_cleaning_end = DummyOperator(task_id="log_cleaning_end")

log_cleaning_start >> group_airflow_log_cleaning >> log_cleaning_end
