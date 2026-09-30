# data_loader.py

import pandas as pd
 
df = pd.read_csv('data/superstore.csv', encoding='latin-1')
df['Order Date'] = pd.to_datetime(df['Order Date'])
df['Ship Date']  = pd.to_datetime(df['Ship Date'])
df['Year']  = df['Order Date'].dt.year
df['Month'] = df['Order Date'].dt.to_period('M').astype(str)
 
REGIONS    = sorted(df['Region'].unique())
CATEGORIES = sorted(df['Category'].unique())
 
def filter_df(filters):
    """Return the rows of df that match the filter selections.
    filters is the dict kept in the store: regions, cats, start, end."""
    dff = df
    if not filters:
        return dff
    if filters.get('regions'):
        dff = dff[dff['Region'].isin(filters['regions'])]
    if filters.get('cats'):
        dff = dff[dff['Category'].isin(filters['cats'])]
    if filters.get('start'):
        dff = dff[dff['Order Date'] >= filters['start']]
    if filters.get('end'):
        dff = dff[dff['Order Date'] <= filters['end']]
    return dff
 
print(df.shape)        # (9994, 23)
print(df['Region'].unique())   # ['South', 'West', 'Central', 'East']
print(df['Category'].unique()) # ['Furniture' 'Office Supplies' 'Technology']