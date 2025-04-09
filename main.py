import sqlite3
import pandas as pd



# Query No : 1
# Total number of patients enrolled in each region


def load_csv_to_db():
    df_patients = pd.read_csv('patients_data.csv')
    df_regions = pd.read_csv('regions_data.csv')
    conn = sqlite3.connect('patients.db')
    df_patients.to_sql('patients_data', conn, if_exists='replace', index=False)
    df_regions.to_sql('regions_data', conn, if_exists='replace', index=False)

    conn.close()


def query_1():
    conn = sqlite3.connect('patients.db')
    cursor = conn.cursor()
    cursor.execute("""
        select region_name, count(*) as total_patients
        from patients_data 
        join regions_data on 
        patients_data.region_id = regions_data.region_id 
        group by region_name
        order by region_name""")
    col = [des[0] for des in cursor.description]
    print(col)
    results = cursor.fetchall()
    for row in results:
        print(row)
    conn.close()


# Query No : 2 
# Identify the region with fastest enrollment rate by comparing total patient enrolled with the trial duartion 



def load_csv_to_db2():
    dt_patients = pd.read_csv('patients_data.csv')
    dt_region = pd.read_csv('regions_data.csv')
    dt_trial = pd.read_csv('trial_results.csv')
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
            rd.region_name,
            rd.total_patients,
            COUNT(DISTINCT pd.patient_id) as enrolled_patients,
            ROUND(CAST(rd.total_patients AS FLOAT) / 
                  CAST(JULIANDAY(MAX(pd.enrollment_date)) - JULIANDAY(MIN(pd.enrollment_date)) AS FLOAT), 2) as enrollment_rate
        FROM regions_data rd
        JOIN patients_data pd ON rd.region_id = pd.region_id
        GROUP BY rd.region_name, rd.total_patients
        ORDER BY enrollment_rate DESC
        limit 1 ;
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
    df_patients = pd.read_csv('patients_data.csv')
    df_region = pd.read_csv('regions_data.csv')
    df_trial = pd.read_csv('trial_results.csv')
    conn = sqlite3.connect('patients.db')
    df_patients.to_sql('patients_data', conn, if_exists='replace',index = False)
    df_region.to_sql('regions_data',conn,if_exists='replace',index=False)
    df_trial.to_sql('trial_results',conn,if_exists='replace',index=False)
    conn.close()

def query_3():
    conn = sqlite3.connect('patients.db')
    cursor = conn.cursor()
    cursor.execute("""
        select 
        regions_data.region_name , 
        COUNT(CASE WHEN trial_results.trial_outcome = 'Improved' THEN 1 END) AS improved_patients,
        (COUNT(CASE WHEN trial_results.trial_outcome = 'Improved' THEN 1 END) * 100.0) /                 regions_data.total_patients
        AS improved_percentage
        from regions_data join 
        patients_data on regions_data.region_id = patients_data.region_id
        join trial_results on patients_data.patient_id = trial_results.patient_id
        group by regions_data.region_name 
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
    data_patients = pd.read_csv('patients_data.csv')
    data_region = pd.read_csv('regions_data.csv')
    data_trial = pd.read_csv('trial_results.csv')
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
            COUNT(*) AS total_adverse_events 
        FROM regions_data 
        JOIN patients_data ON regions_data.region_id = patients_data.region_id 
        JOIN trial_results ON patients_data.patient_id = trial_results.patient_id
        WHERE trial_results.adverse_event = True
        GROUP BY regions_data.region_name 
        ORDER BY total_adverse_events DESC
        limit 1 ;
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
    data_patients = pd.read_csv('patients_data.csv')
    data_region = pd.read_csv('regions_data.csv')
    data_trial = pd.read_csv('trial_results.csv')
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
        WHERE trial_results.adverse_event = True
        GROUP BY patients_data.age, patients_data.gender
        ORDER BY total_adverse_events DESC
        limit 1 ;
    """)
    col = [desc[0] for desc in cursor.description]
    print(col)
    answer = cursor.fetchall()
    for data in answer:
        print(data)
    conn.close()



if __name__=="__main__":
    load_csv_to_db()
    query_1()
    load_csv_to_db2()
    query_2()
    load_csv_to_db3()
    query_3()
    load_csv_to_db4()
    query_4()
    load_csv_to_db5()
    query_5()
