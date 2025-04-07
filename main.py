
import pandas as pd
import sqlite3
from datetime import datetime
from random import randint, random, choice

def process_regions_data():
    # Read regions data
    df = pd.read_csv('regions_data.csv')
    
    # Keep first occurrence of each region_id (ensuring unique region_id)
    df = df.drop_duplicates(subset=['region_id'], keep='first')
    
    # For each unique region_name, keep only one region_id
    df = df.drop_duplicates(subset=['region_name'], keep='first')
    
    # Keep only first 100 records
    df = df.head(100)
    
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
    print("Processed regions data:")
    print(processed_regions)
