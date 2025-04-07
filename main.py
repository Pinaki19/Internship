
import pandas as pd
import sqlite3
from datetime import datetime
from random import randint, random,choice


def read_data(file_name):
  # Create SQLite connection
  conn = sqlite3.connect('patients.db')
  
  # Read CSV file
  df = pd.read_csv(f'{file_name}.csv')
  
  # Create patients table and insert data
  df.to_sql('patients', conn, if_exists='replace', index=False)
  
  # Close connection
  conn.close()
  print(df)
  return df


if __name__ == '__main__':
  read_data('trial_results')

