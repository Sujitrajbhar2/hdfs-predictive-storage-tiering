from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

default_args = {
    "owner": "Sujit",
    "start_date": datetime(2026, 8, 1)
}

with DAG(
    dag_id="DataTierAI_Enterprise_Pipeline",
    default_args=default_args,
    schedule=None,
    catchup=False,
    description="Enterprise Data Pipeline Automation"
) as dag:

    etl = BashOperator(
        task_id="ETL",
        bash_command="python /opt/airflow/scripts/run_etl.py"
    )

    preprocessing = BashOperator(
        task_id="Preprocessing",
        bash_command="python /opt/airflow/scripts/run_preprocessing.py"
    )

    feature_engineering = BashOperator(
        task_id="Feature_Engineering",
        bash_command="python /opt/airflow/scripts/run_feature_eng.py"
    )

    spark = BashOperator(
        task_id="Spark_Processing",
        bash_command="python /opt/airflow/scripts/run_spark.py"
    )

    ml = BashOperator(
        task_id="Machine_Learning",
        bash_command="python /opt/airflow/scripts/run_ml.py"
    )
    generate_reports = BashOperator(
        task_id="Generate_Reports",
        bash_command="python /opt/airflow/scripts/generate_reports.py"
    )

    deploy_model = BashOperator(
        task_id="Deploy_Model",
        bash_command="python /opt/airflow/scripts/deploy_model.py"
    )

    etl >> preprocessing >> feature_engineering >> spark >> ml >> generate_reports >> deploy_model