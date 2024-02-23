import pandas as pd

def clean(df, region_type='zip', yr_pcts=(1, 2, 3)):
    # Feature creation: changes in metrics over time
    for x in ['ZHVI', 'ZORI', 'Sales', 'Sale Listings', 'Days on Market', 'New Construction']:
        for year in yr_pcts:
            df[str(year) + 'yr pct change ' + x] = (df[x + ' ' + str(2023)] - df[x + ' ' + str(2023-year)])/df[x + ' ' + str(2023-year)]
    
    # Convert to other region types via groupby
    if region_type == 'metro':
        numeric_columns = list(df.select_dtypes(include=['number']).columns)
        df = df[numeric_columns+['Metro']].groupby(by='Metro').mean().reset_index(level=0)
        df = df.drop(columns=['RegionID', 'SizeRankZip', 'RegionName'])
    elif region_type == 'county':
        numeric_columns = list(df.select_dtypes(include=['number']).columns)
        df = df[numeric_columns+['CountyName', 'State']].groupby(by=['CountyName', 'State']).mean().reset_index(level=0).reset_index(level=0)
        df = df.drop(columns=['RegionID', 'SizeRankZip', 'RegionName'])
    
    return df