import pandas as pd

path=r'C:\Users\pinak\Downloads\Internship\main\CSV\trial_results.csv'

def fn(x):
    if x=='Worsened':
        return True
    return False
    

df=pd.read_csv(path)

df['adverse_event']=df['trial_outcome'].apply(fn)

df.to_csv(path,index=False)