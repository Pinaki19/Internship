
import pandas as pd
import sqlite3
from datetime import datetime

# Read CSV file
df = pd.read_csv('MOCK_DATA_PR6.csv')

# Convert enrollment_date to datetime
df['enrollment_date'] = pd.to_datetime(df['enrollment_date'], format='%d-%m-%Y')

# Create SQLite connection
conn = sqlite3.connect('patients.db')

# Write to SQLite
df.to_sql('patients', conn, if_exists='replace', index=False)

# Verify the data
cursor = conn.cursor()
result = cursor.execute("SELECT * FROM patients LIMIT 5").fetchall()
print("First 5 records:")
for row in result:
    print(row)

conn.close()
