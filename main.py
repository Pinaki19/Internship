
import pandas as pd
import sqlite3
from datetime import datetime
from random import randint, random,choice
# Create SQLite connection
conn = sqlite3.connect('patients.db')
df_from_db = pd.read_sql_query("SELECT * FROM patients", conn)
df_from_db['patient_id'] = range(1, len(df_from_db) + 1)

# Save to CSV
df_from_db.to_csv('MOCK_DATA_PR6_new.csv', index=False)

print("Data has been saved back to MOCK_DATA_PR6.csv")
conn.close()

