
import pandas as pd
import sqlite3
from datetime import datetime
from random import randint, random,choice


def read_patients():
  # Create SQLite connection
  conn = sqlite3.connect('patients.db')
  
  # Read CSV file
  df = pd.read_csv('patients_data.csv')
  
  # Create patients table and insert data
  df.to_sql('patients', conn, if_exists='replace', index=False)
  
  # Close connection
  conn.close()
  
  return df


