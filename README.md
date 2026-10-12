# Temilola-Onaneye-de-task
Temilola Onaneye Data Engr Task
DBT Based Project

Follow the steps below to run this Project
1. After Clonning this Repo, change working directory to Repo Folder.
2. Build the Docker Container images using - [docker compose up --build]
3. After a Successful build, You can access Airflow on http://localhost:8080/home (Access Airflow using the Following Credentials - USERNAME - airflow  PASSWORD - airflow)
4. Trigger the nyt_books_loader dag, this will commence the ETL Process of fetching the Data from New York Times API
5. After the above DAG is successful and done, dbt_deel_task DAG will trigger automatically
6. Initial Staging Table or loaded data from the API can be explored using PgAdmin or any postgresql client using the following connection. (HOSTNAME - localhost , PORT - 5433 , USERNAME -postgres , PASSWORD - postgres)
7. The results or output CSV for SQL Questions can be found in the Questions Folder
