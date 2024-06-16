# Importing Libraries and Packages
from cosmos import DbtDag, ProjectConfig, ProfileConfig, ExecutionConfig
from cosmos.profiles import PostgresUserPasswordProfileMapping
from airflow.operators.dagrun_operator import TriggerDagRunOperator
from airflow.datasets import Dataset
from datetime import datetime

profile_config = ProfileConfig(
    profile_name="dbt_deel_task",
    target_name="dev",
    profile_mapping=PostgresUserPasswordProfileMapping(
        conn_id="postgres",
        profile_args={
            "dbname": "postgres",
            "schema": "public",
        },
    ),
)

my_dbt_dag = DbtDag(
    project_config=ProjectConfig(
        "/opt/airflow/dbt/dbt_deel_task",
    ),
    profile_config=profile_config,
    execution_config=ExecutionConfig(
        dbt_executable_path="/home/airflow/.local/bin/dbt",
    ),
    # normal dag parameters
    schedule_interval=None,
    start_date=datetime(2024, 6, 14),
    catchup=False,
    dag_id="dbt_deel_task",
    default_args={"retries": 2},
)

my_dbt_dag