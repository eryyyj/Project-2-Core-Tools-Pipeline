from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator

# making a list  of default arguments for the DAG
default_args = {
    "owner": "eryyy",
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

# defining the DAG
with DAG(
    dag_id="netflix_elt_pipeline",
    default_args=default_args,
    schedule_interval="@daily",      
    start_date=datetime(2026, 1, 1), 
    catchup=False,
) as dag:

    # this task for extracting the netflix dataset in the raw data folder using the kaggle API
    extract = BashOperator(
        task_id="extract",
        bash_command="bash /app/scripts/download_data.sh ",
    )

    # this task is for pushing the data into the staging_raw table in the database using Spark
    load = BashOperator(
        task_id="load",
        bash_command="python /app/scripts/load_data.py",
    )

    # this task is for transforming the data using dbt models to ensure that the data is in the correct format and structure
    transform = BashOperator(
        task_id="transform",
        bash_command="dbt run --project-dir /app/week34_project --profiles-dir /app/week34_project",
    )

    # this task is for  testing the dbt models to ensure they are working as expected
    test = BashOperator(
        task_id="test",
        bash_command="dbt test --project-dir /app/week34_project --profiles-dir /app/week34_project",
    )

    # defining the dependencies
    extract >> load >> transform >> test