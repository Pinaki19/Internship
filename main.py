
import pandas as pd
import sqlite3
from datetime import datetime
from random import randint, random, choice

def process_regions_data():
  # Read regions data
  df = pd.read_csv('regions_data.csv')
  all='ABCDEFGHIJKLMNOPQRSTUVWXYZ'
  alpha=[char for char in all]
  codes=[choice(alpha)+choice(alpha) for i in range(len(df))]
  seen=set()
  for row in df:
    # print(df[row])
   
    new_code=choice(codes)
    while new_code in seen:
        new_code=choice(codes)
    df['region_code']=new_code
    seen.add(new_code)
  # Save processed data back to CSV
  df.to_csv('regions_data.csv', index=False)
  return df

def read_data(file_name):
    # Read CSV file
    df = pd.read_csv(f'{file_name}.csv')
    
    # Create SQLite connection and save to database
    conn = sqlite3.connect('patients.db')
    df.to_sql('patients', conn, if_exists='replace', index=False)
    conn.close()
    
    print(df)
    return df

if __name__ == '__main__':
    processed_regions = process_regions_data()

