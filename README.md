# airflow_dag_cleanup
DAG Cleanup Scheduler to clean logging files created by Airflow DAG

Setup
1. Set BASE_LOG_FOLDER and RETENTION based on your needs.
2. create variable to hold credential, unless your remote airflow host/worker is passwordless you can remove sshpass from the provided bash script command
3. define a number of airflow worker hostname
```
LIST_HOST = [{"alias": "dev-airflow-1", "host": "172.172.172.1"}, 
            {"alias": "dev-airflow-2", "host": "172.172.172.2"}]
```
  this example will create dynamic task with to task to clean on hosts 172.172.172.1, and 172.172.172.2

Result
![Result](https://raw.githubusercontent.com/muhk01/airflow_dag_log_cleanup/main/img/DAG.PNG)
