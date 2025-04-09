
import pandas as pd

# Read the CSV files
notes_df = pd.read_csv('clinician_notes.csv')
regions_df = pd.read_csv('regions_data.csv')

# Count notes per region
notes_per_region = notes_df.groupby('region_id').size().reset_index(name='note_count')

# Merge with region names
result = pd.merge(
    notes_per_region,
    regions_df[['region_id', 'region_name']],
    on='region_id',
    how='left'
)

# Sort by region name
result = result.sort_values('region_name')

# Save results
result.to_csv('notes_per_region.csv', index=False)

# Print results
print("\nNotes per Region:")
print("================")
for _, row in result.iterrows():
    print(f"{row['region_name']} (ID: {row['region_id']}): {row['note_count']} notes")
