import sqlite3
import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import chi2_contingency, ttest_ind
cur_dir= os.path.dirname(__file__)

# Query No : 1
# Total number of patients enrolled in each region

def load_csv_to_db1():
    df_patients = pd.read_csv(os.path.join(cur_dir,'CSV','patients_data.csv'))
    df_regions = pd.read_csv(os.path.join(cur_dir,'CSV','regions_data.csv'))
    conn = sqlite3.connect('patients.db')
    df_patients.to_sql('patients_data', conn, if_exists='replace', index=False)
    df_regions.to_sql('regions_data', conn, if_exists='replace', index=False)
    conn.close()


def query_1():
    conn = sqlite3.connect('patients.db')
    cursor = conn.cursor()
    cursor.execute("""
        SELECT region_name, rd.region_id,
        COUNT(patient_id) AS total_patients
        FROM patients_data 
        JOIN regions_data rd ON 
        patients_data.region_id = rd.region_id 
        GROUP BY region_name
        ORDER BY region_name""")
    col = [des[0] for des in cursor.description]
    print(col)
    results = cursor.fetchall()
    for row in results:
        print(row)
    conn.close()


# Query No : 2 
# Identify the region with fastest enrollment rate by comparing total patient enrolled with the trial duartion 


def load_csv_to_db2():
    dt_patients = pd.read_csv(os.path.join(cur_dir,'CSV','patients_data.csv'))
    dt_region = pd.read_csv(os.path.join(cur_dir,'CSV','regions_data.csv'))
    dt_trial = pd.read_csv(os.path.join(cur_dir,'CSV','trial_results.csv'))
    conn = sqlite3.connect('patients.db')
    dt_patients.to_sql('patients_data', conn, if_exists='replace', index=False)
    dt_region.to_sql('regions_data', conn, if_exists='replace', index=False)
    dt_trial.to_sql('trial_results', conn, if_exists='replace', index=False)
    conn.close()

def query_2():
    conn = sqlite3.connect('patients.db')
    cursor = conn.cursor()
    cursor.execute("""
    SELECT 
    rd.region_name, rd.region_id,
    COUNT(pd.patient_id) AS total_patients,
    ROUND((COUNT(pd.patient_id)*1.0)/(
    SELECT ((strftime('%Y',MAX(tr.visit_date)) - (strftime('%Y',MIN(tr.visit_date))))*12+                       (strftime('%m',MAX(tr.visit_date)) - (strftime('%m',MIN(tr.visit_date))))) AS trial_duration
    FROM trial_results tr)
    *1.0,2) AS enrollment_rate
    FROM regions_data rd
    JOIN patients_data pd ON rd.region_id = pd.region_id
    GROUP BY rd.region_name
    ORDER BY enrollment_rate DESC
    LIMIT 1
         ; 
        """)
    cols = [desc[0] for desc in cursor.description]
    print(cols)
    rows = cursor.fetchall()
    for data in rows:
        print(data)
    conn.close()


# Query No : 3 
# Determine the percentage of patient in each region who show "improved" outcome 

def load_csv_to_db3():
    df_patients = pd.read_csv(os.path.join(cur_dir,'CSV','patients_data.csv'))
    df_region = pd.read_csv(os.path.join(cur_dir,'CSV','regions_data.csv'))
    df_trial = pd.read_csv(os.path.join(cur_dir,'CSV','trial_results.csv'))
    conn = sqlite3.connect('patients.db')
    df_patients.to_sql('patients_data', conn, if_exists='replace',index = False)
    df_region.to_sql('regions_data',conn,if_exists='replace',index=False)
    df_trial.to_sql('trial_results',conn,if_exists='replace',index=False)
    conn.close()

def query_3():
    conn = sqlite3.connect('patients.db')
    cursor = conn.cursor()
    cursor.execute("""
    SELECT
        rd.region_name,
        rd.region_id,
        COUNT(DISTINCT CASE WHEN tr.trial_outcome = 'Improved' THEN pd.patient_id END) AS improved_patients,
        COUNT(DISTINCT pd.patient_id) as total_patients,
        ROUND(
            (COUNT(DISTINCT CASE WHEN tr.trial_outcome = 'Improved' THEN pd.patient_id END) * 100.0) /
            NULLIF(COUNT(pd.patient_id), 0), 2)
        AS improved_percentage
        FROM regions_data rd
        LEFT JOIN patients_data pd ON rd.region_id = pd.region_id
        LEFT JOIN trial_results tr ON pd.patient_id = tr.patient_id
        GROUP BY rd.region_id, rd.region_name
        ORDER BY improved_percentage DESC
        ;
    """)
    col = [des[0] for des in cursor.description]
    print(col)
    row = cursor.fetchall()
    for data in row:
        print(data)
    conn.close()



# Query No : 4 
# Find the region with most adverse event 

def load_csv_to_db4():
    data_patients = pd.read_csv(os.path.join(cur_dir,'CSV','patients_data.csv'))
    data_region = pd.read_csv(os.path.join(cur_dir,'CSV','regions_data.csv'))
    data_trial = pd.read_csv(os.path.join(cur_dir,'CSV','trial_results.csv'))
    conn = sqlite3.connect('patients.db')
    data_patients.to_sql('patients_data', conn, if_exists='replace',index = False)
    data_region.to_sql('regions_data',conn,if_exists='replace',index=False)
    data_trial.to_sql('trial_results',conn,if_exists='replace',index=False)
    conn.close() 

def query_4():
    conn = sqlite3.connect('patients.db')
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 
            regions_data.region_name,
            regions_data.region_id,
            COUNT(*) AS total_adverse_events 
        FROM regions_data 
        JOIN patients_data ON regions_data.region_id = patients_data.region_id 
        JOIN trial_results ON patients_data.patient_id = trial_results.patient_id
        WHERE trial_results.adverse_event = TRUE
        GROUP BY regions_data.region_name 
        ORDER BY total_adverse_events DESC
        LIMIT 1;
    """)
    col = [desc[0] for desc in cursor.description]
    print(col)
    answer = cursor.fetchall()
    for data in answer:
        print(data)
    conn.close()


# Query No : 5 .
# Analayze whether age or gender correlates strongly with adverse events 

def load_csv_to_db5():
    data_patients = pd.read_csv(os.path.join(cur_dir,'CSV','patients_data.csv'))
    data_region = pd.read_csv(os.path.join(cur_dir,'CSV','regions_data.csv'))
    data_trial = pd.read_csv(os.path.join(cur_dir,'CSV','trial_results.csv'))
    conn = sqlite3.connect('patients.db')
    data_patients.to_sql('patients_data', conn, if_exists='replace',index = False)
    data_region.to_sql('regions_data',conn,if_exists='replace',index=False)
    data_trial.to_sql('trial_results',conn,if_exists='replace',index=False)
    conn.close()

def query_5():
    conn = sqlite3.connect('patients.db')
    cursor = conn.cursor()
    cursor.execute("""
        SELECT
            patients_data.age,
            patients_data.gender,
            COUNT(*) AS total_adverse_events
        FROM patients_data
        JOIN trial_results ON patients_data.patient_id = trial_results.patient_id
        WHERE trial_results.adverse_event = TRUE
        GROUP BY patients_data.age, patients_data.gender
        ORDER BY total_adverse_events DESC
        ;
    """)
    col = [desc[0] for desc in cursor.description]
    print(col)
    answer = cursor.fetchall()
    for data in answer:
        print(data)
    conn.close()


# Function to perform SQL query and fetch merged data
def fetch_merged_data(patient_info_csv, visit_data_csv, db_name='adverse_event_analysis.db'):
    # Connect to SQLite database (or create it if it doesn't exist)
    conn = sqlite3.connect(db_name)

    # Load data into pandas
    patient_info_df = pd.read_csv(patient_info_csv)
    visit_data_df = pd.read_csv(visit_data_csv)

    # Load data into SQLite tables
    patient_info_df.to_sql('patient_info', conn, if_exists='replace', index=False)
    visit_data_df.to_sql('visit_data', conn, if_exists='replace', index=False)

    # SQL query to join the two tables based on patient_id
    query = """
    SELECT p.patient_id, p.age, p.gender, v.adverse_event
    FROM patient_info p
    JOIN visit_data v ON p.patient_id = v.patient_id
    """
    
    # Fetch the merged data into a DataFrame
    merged_df = pd.read_sql_query(query, conn)

    # Ensure 'adverse_event' is boolean
    merged_df['adverse_event'] = merged_df['adverse_event'].astype(bool)

    return merged_df

# Main function to analyze and plot the data
def analyze_adverse_events(patient_info_csv, visit_data_csv):
    # Fetch the merged data using the SQL function
    merged_df = fetch_merged_data(patient_info_csv, visit_data_csv)

    # Plot Age vs Adverse Event (Boxplot)
    plt.figure(figsize=(8, 6))
    sns.boxplot(x='adverse_event', y='age', data=merged_df, palette='Blues')
    plt.title('Age vs Adverse Event')
    plt.xlabel('Adverse Event')
    plt.ylabel('Age')
    plt.show()

    # Plot Gender vs Adverse Event (Countplot)
    plt.figure(figsize=(8, 6))
    sns.countplot(x='gender', hue='adverse_event', data=merged_df, palette='Blues')
    plt.title('Gender vs Adverse Event')
    plt.xlabel('Gender')
    plt.ylabel('Count of Adverse Events')
    plt.show()

    # Chi-Square Test for Gender and Adverse Event
    contingency_table = pd.crosstab(merged_df['gender'], merged_df['adverse_event'])
    chi2, p, _, _ = chi2_contingency(contingency_table)
    print(f"\nChi-Square Test for Gender and Adverse Event: p-value = {p}")

    # T-test for Age and Adverse Event
    age_with_adverse_event = merged_df[merged_df['adverse_event'] == True]['age']
    age_without_adverse_event = merged_df[merged_df['adverse_event'] == False]['age']
    t_stat, p_value = ttest_ind(age_with_adverse_event, age_without_adverse_event)
    print(f"\nT-test for Age and Adverse Event: p-value = {p_value}")




if __name__=="__main__":
    # load_csv_to_db1()
    # query_1()
    # load_csv_to_db2()
    # query_2()
    # load_csv_to_db3()
    # query_3()
    # load_csv_to_db4()
    # query_4()
    # load_csv_to_db5()
    # query_5()
    #analyze_adverse_events(r'C:\Users\pinak\Downloads\Internship\main\CSV\patients_data.csv', r'C:\Users\pinak\Downloads\Internship\main\CSV\trial_results.csv')
