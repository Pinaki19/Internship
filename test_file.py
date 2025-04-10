import pandas as pd

def count_trial_outcomes():
    df = pd.read_csv('clinician_notes.csv')
    df_cleaned = pd.read_csv('cleaned_notes.csv')  # Handle quoted fields

    # Get unique note text and outcomes mapping
    outcome_map = df_cleaned[['note_text', 'trial_outcome']].drop_duplicates()

    # Merge to get outcomes for clinical notes
    df_merged = df.merge(outcome_map, on='note_text', how='left')

    # Count outcomes
    outcome_counts = df_merged['trial_outcome'].value_counts()
    print("\nTrial Outcome Counts:")
    print("====================")
    print(f"Improved: {outcome_counts.get('Improved', 0)}")
    print(f"Stable: {outcome_counts.get('Stable', 0)}")
    print(f"Worsened: {outcome_counts.get('Worsened', 0)}")

if __name__=="__main__":
    count_trial_outcomes()