
import pandas as pd
import sqlite3
from datetime import datetime
from random import randint, random, choice

def read_data(file_name):
    # Read CSV file
    df = pd.read_csv(f'{file_name}.csv')
    
    # Generate unique random patient IDs between 1 and 1000
    available_ids = list(range(1, 1001))
    unique_patient_ids = df['patient_id'].unique()
    id_mapping = {old_id: available_ids.pop(randint(0, len(available_ids)-1)) 
                 for old_id in unique_patient_ids}
    
    # Map old IDs to new random IDs while preserving relationships
    df['patient_id'] = df['patient_id'].map(id_mapping)
    
    # Save back to CSV
    df.to_csv(f'{file_name}.csv', index=False)
    
    # Create SQLite connection and save to database
    conn = sqlite3.connect('patients.db')
    df.to_sql('patients', conn, if_exists='replace', index=False)
    conn.close()
    
    print(df)
    return df

if __name__ == '__main__':
    read_data('trial_results')
