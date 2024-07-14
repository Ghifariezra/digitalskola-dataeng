from airflow.providers.postgres.hooks.postgres import PostgresHook
import pandas as pd
import os

def extract_func(**kwargs):
    showRecords = "SELECT * FROM {table}"
    conn = PostgresHook(
        postgres_conn_id="post_conn",
        supports_autocommit=True,
        supports_executemany=True
    ).get_conn()

    cur = conn.cursor()
    cur.execute(
        showRecords.format(table=kwargs.get('table_name'))
    )

    records = cur.fetchall()
    columns = [desc[0] for desc in cur.description]
    df = pd.DataFrame(records, columns=columns)

    cur.close()
    conn.close()

    return df