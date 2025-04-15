import pandas as pd

path=r'C:\Users\pinak\Downloads\Internship\main\CSV\trial_results.csv'
field='visit_date'

def fix_date(date):
    l=date.split('-')
    l.reverse()
    return '-'.join(l)

df=pd.read_csv(path)

df[field]=df[field].apply(fix_date)

df.to_csv(path,index=False)