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

def model_features(df, add=None):
    column_selection = ['ZORI 2023', 'ZHVI 2023', 'ZHVF 2025-01-31', 'Transit Score', 'NatWalkInd', '3yr pct change ZHVI',
                        '3yr pct change ZORI', '3yr pct change Sale Listings', '3yr pct change Sales', '3yr pct change Days on Market',
                        '3yr pct change New Construction']
    
    # Adding any features not included by default
    if add is not None:
        for x in add:
            if x not in column_selection:
                column_selection.append(x)
    
    return(df[column_selection])