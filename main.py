
import pandas as pd
import sqlite3
from datetime import datetime
from random import randint, random, choice

def process_regions_data():
    # Read regions data
    df = pd.read_csv('regions_data.csv')
    
    # Generate list of two-letter codes
    import string
    letters = list(string.ascii_uppercase)
    two_letter_codes = [a + b for a in letters for b in letters]
    code_index = 0
    
    # Create a mapping for existing region names
    name_mapping = {}
    seen_names = set()
    
    # Process each row
    for idx, row in df.iterrows():
        region_id = row['region_id']
        region_name = row['region_name']
        
        if pd.isna(region_name) or region_name in seen_names:
            # Assign new unique two-letter code
            while two_letter_codes[code_index] in seen_names:
                code_index += 1
            name_mapping[region_id] = two_letter_codes[code_index]
            code_index += 1
        else:
            name_mapping[region_id] = region_name
            seen_names.add(region_name)
    
    # Apply the mapping to ensure consistency
    df['region_name'] = df['region_id'].map(name_mapping)
    
    # Keep first occurrence of each region_id
    df = df.drop_duplicates(subset=['region_id'], keep='first')
    
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
