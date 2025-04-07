
import pandas as pd
import sqlite3
from datetime import datetime
from random import randint, random, choice

def read_data(file_name):
    # Read CSV file
    df = pd.read_csv(f'{file_name}.csv')
    
    # Create new patient IDs
    df['patient_id'] = [randint(1,1000) for _ in range(len(df))]
    
    # Update all adverse_event rows to True where trial_outcome is Worsened
    df.loc[df['trial_outcome'] == 'Worsened', 'adverse_event'] = True
    
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
