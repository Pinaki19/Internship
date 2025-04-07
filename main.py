
import pandas as pd
import sqlite3
from datetime import datetime
from random import randint, random, choice

def process_regions_data():
    # Read regions data
    df = pd.read_csv('regions_data.csv')
    
    # Create sets to track used IDs and names
    used_ids = set()
    used_names = set()
    max_id = df['region_id'].max()
    
    # Process each row
    for index, row in df.iterrows():
        region_id = row['region_id']
        region_name = row['region_name']
        
        # If ID already used, generate new unique ID
        if region_id in used_ids:
            max_id += 1
            df.at[index, 'region_id'] = max_id
            region_id = max_id
            
        # If name already used, generate new unique name
        if region_name in used_names:
            new_name = f'REG_{max_id}'
            while new_name in used_names:
                max_id += 1
                new_name = f'REG_{max_id}'
            df.at[index, 'region_name'] = new_name
            region_name = new_name
            
        used_ids.add(region_id)
        used_names.add(region_name)
    
    # Sort by region_id for consistency
    df = df.sort_values('region_id')
    
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

