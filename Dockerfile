FROM apache/airflow:2.8.4-python3.10
USER root
RUN apt update
RUN apt install git -y
RUN apt update -y && sudo apt install -y build-essential libpq-dev
RUN apt-get update \
  && apt-get install -y --no-install-recommends \
         gcc \
         heimdal-dev \
  && apt-get autoremove -yqq --purge \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*
USER airflow

ENV PYTHON_VERSION=3.10
ENV CONSTRAINT_URL="https://raw.githubusercontent.com/apache/airflow/constraints-${AIRFLOW_VERSION}/constraints-${PYTHON_VERSION}.txt"
RUN pip install "apache-airflow[async,postgres]==${AIRFLOW_VERSION}" --constraint "${CONSTRAINT_URL}"

RUN pip uninstall -y argparse
RUN pip install dbt-core
RUN pip install dbt-postgres
RUN pip install astronomer-cosmos[dbt.all]
RUN pip install python-dotenv
RUN pip install pandas
RUN pip install requests 
RUN pip install psycopg2-binary
RUN pip install sqlalchemy

USER root
RUN mkdir -p -m 777 /opt/airflow/dbt
RUN mkdir -p -m 777 /opt/airflow/dbt/logs
RUN mkdir -p -m 777 /opt/airflow/dbt/build
RUN mkdir -p -m 777 /opt/airflow/logs
RUN mkdir -p -m 777 /opt/airflow/dags
RUN mkdir -p -m 777 /opt/airflow/plugins
RUN mkdir -p -m 777 /opt/airflow/logs/scheduler
RUN mkdir -p -m 777 /dbt

RUN chmod a+x /usr/bin/git
