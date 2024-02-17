import pandas as pd


def load(zhvi_years=(2003, 2008, 2013, 2018, 2019, 2020, 2021, 2022, 2023),
         zori_years=(2018, 2019, 2020, 2021, 2022, 2023),
         sale_listings_years=(2019, 2020, 2021, 2022, 2023),
         sales_years=(2013, 2018, 2019, 2020, 2021, 2022, 2021),
         days_on_market_years=(2019, 2020, 2021, 2022, 2023),
         new_cons_years=(2018, 2019, 2020, 2021, 2022, 2023)):
    '''
    Returns a df of regions by zipcode along with 6 different metrics for that region:
    Zillow Home Value Index (ZHVI), Zillow Home Value Forecast (ZHVF), Zillow Observed Rent Index (ZORI),
    Average Number of Monthly Sale Listings, Average Number of Monthly Sales, Average Number of Days on Market,
    Average Number of Monthly New Constructions

    To get data for different years pass an alternate tuple/list for any of the following metrics
    :param zhvi_years: Must be 2003 or later
    :param zori_years: Must be 2018 or later
    :param sale_listings_years: Must be 2019 or later
    :param sales_years: must be 2013 or later
    :param days_on_market_years: must be 2019 or later
    :param new_cons_years: must be 2018 or later
    :return:
    '''


    zhvi_url = 'https://files.zillowstatic.com/research/public_csvs/zhvi/Zip_zhvi_uc_sfrcondo_tier_0.33_0.67_sm_sa_month.csv?t=1707768517 '
    zhvf_url = 'https://files.zillowstatic.com/research/public_csvs/zhvf_growth/Zip_zhvf_growth_uc_sfrcondo_tier_0.33_0.67_sm_sa_month.csv?t=1707768517 '
    zori_url = 'https://files.zillowstatic.com/research/public_csvs/zori/Zip_zori_uc_sfrcondomfr_sm_month.csv?t=1707768517 '
    sale_listings_url = 'https://files.zillowstatic.com/research/public_csvs/invt_fs/Metro_invt_fs_uc_sfrcondo_sm_month.csv?t=1707768517 '
    sales_url = 'https://files.zillowstatic.com/research/public_csvs/sales_count_now/Metro_sales_count_now_uc_sfrcondo_month.csv?t=1707768517 '
    days_on_market_url = 'https://files.zillowstatic.com/research/public_csvs/mean_doz_pending/Metro_mean_doz_pending_uc_sfrcondo_sm_month.csv?t=1707768517 '
    new_cons_url = 'https://files.zillowstatic.com/research/public_csvs/new_con_sales_count_raw/Metro_new_con_sales_count_raw_uc_sfrcondo_month.csv?t=1707768517 '
    metro_mapping_url = 'https://raw.githubusercontent.com/chambliss/Major-Metro-Areas-And-Their-Cities/master/major_metro_areas.csv'
    transit_url = 'datasets/transit_scores.csv'
    walk_url = 'https://edg.epa.gov/EPADataCommons/public/OA/EPA_SmartLocationDatabase_V3_Jan_2021_Final.csv'

    zhvi = pd.read_csv(zhvi_url)
    zhvf = pd.read_csv(zhvf_url)
    zori = pd.read_csv(zori_url)
    sale_listings = pd.read_csv(sale_listings_url)
    sales = pd.read_csv(sales_url)
    days_on_market = pd.read_csv(days_on_market_url)
    new_cons = pd.read_csv(new_cons_url)
    metro_mapping = pd.read_csv(metro_mapping_url)
    transit = pd.read_csv(transit_url)
    walk = pd.read_csv(walk_url)

    # ZHVI feature selection
    zhvi_new_cols = []
    for year in zhvi_years:
        new_column = 'ZHVI ' + str(year)
        zhvi_new_cols.append(new_column)
        component_cols = [x for x in zhvi.columns.to_list() if str(year) in x]
        zhvi[new_column] = zhvi[component_cols].mean(axis=1)

    zhvi = zhvi[['RegionID', 'SizeRank', 'RegionName', 'RegionType', 'StateName',
                 'State', 'City', 'Metro', 'CountyName'] + zhvi_new_cols]

    zhvi = zhvi.rename(columns={'SizeRank': 'SizeRankZip'})

    # ZHVF feature selection
    zhvf.columns = ['RegionID', 'SizeRank', 'RegionName', 'RegionType', 'StateName', 'State', 'City', 'Metro',
                    'CountyName', 'ZHVF BaseDate', 'ZHVF 2024-02-29', 'ZHVF 2024-04-30', 'ZHVF 2025-01-31']

    zhvf = zhvf.rename(columns={'SizeRank': 'SizeRankZip'})

    # ZORI feature selection
    zori_new_cols = []
    for year in zori_years:
        new_column = 'ZORI ' + str(year)
        zori_new_cols.append(new_column)
        component_cols = [x for x in zori.columns.to_list() if str(year) in x]
        zori[new_column] = zori[component_cols].mean(axis=1)

    zori = zori[['RegionID', 'SizeRank', 'RegionName', 'RegionType', 'StateName',
                 'State', 'City', 'Metro', 'CountyName'] + zori_new_cols]

    zori = zori.rename(columns={'SizeRank': 'SizeRankZip'})

    # Sale Listings feature selection
    sale_listings_new_cols = []
    for year in sale_listings_years:
        new_column = 'Sale Listings ' + str(year)
        sale_listings_new_cols.append(new_column)
        component_cols = [x for x in sale_listings.columns.to_list() if str(year) in x]
        sale_listings[new_column] = sale_listings[component_cols].mean(axis=1)

    sale_listings = sale_listings[['RegionID', 'SizeRank', 'RegionName',
                                   'RegionType', 'StateName'] + sale_listings_new_cols]

    sale_listings = sale_listings.rename(columns={'SizeRank': 'SizeRankMSA'})

    # Sales feature selection
    sales_new_cols = []
    for year in sales_years:
        new_column = 'Sales ' + str(year)
        sales_new_cols.append(new_column)
        component_cols = [x for x in sales.columns.to_list() if str(year) in x]
        sales[new_column] = sales[component_cols].mean(axis=1)

    sales = sales[['RegionID', 'SizeRank', 'RegionName',
                   'RegionType', 'StateName'] + sales_new_cols]

    sales = sales.rename(columns={'SizeRank': 'SizeRankMSA'})

    # Days-on-market feature selection
    dom_new_cols = []
    for year in days_on_market_years:
        new_column = 'Days on Market ' + str(year)
        dom_new_cols.append(new_column)
        component_cols = [x for x in days_on_market.columns.to_list() if str(year) in x]
        days_on_market[new_column] = days_on_market[component_cols].mean(axis=1)

    days_on_market = days_on_market[['RegionID', 'SizeRank', 'RegionName',
                                     'RegionType', 'StateName'] + dom_new_cols]

    days_on_market = days_on_market.rename(columns={'SizeRank': 'SizeRankMSA'})

    # New-cons feature selection
    cons_new_cols = []
    for year in new_cons_years:
        new_column = 'New Construction ' + str(year)
        cons_new_cols.append(new_column)
        component_cols = [x for x in new_cons.columns.to_list() if str(year) in x]
        new_cons[new_column] = new_cons[component_cols].mean(axis=1)

    new_cons = new_cons[['RegionID', 'SizeRank', 'RegionName',
                         'RegionType', 'StateName'] + cons_new_cols]

    new_cons = new_cons.rename(columns={'SizeRank': 'SizeRankMSA'})

    # Cleaning metro-statistical-area mapping to use for joins
    metro_mapping['Metro Area'] = metro_mapping['Metro Area'].apply(lambda x: x.replace(' Metro Area', ''))
    metro_mapping = metro_mapping.rename(columns={'Metro Area': 'Metro'})
    metro_mapping = metro_mapping[['City', 'Metro']]

    # Joining dataframes
    df = pd.merge(zhvi, zhvf, on=['RegionID', 'SizeRankZip', 'RegionName', 'RegionType', 'StateName',
                                  'State', 'City', 'Metro', 'CountyName'], how='outer')
    df = pd.merge(df, zori, on=['RegionID', 'SizeRankZip', 'RegionName', 'RegionType', 'StateName',
                                'State', 'City', 'Metro', 'CountyName'], how='outer')

    df2 = pd.merge(sale_listings, sales, on=['RegionID', 'SizeRankMSA', 'RegionName', 'RegionType', 'StateName'],
                   how='outer')
    df2 = pd.merge(df2, days_on_market, on=['RegionID', 'SizeRankMSA', 'RegionName', 'RegionType', 'StateName'],
                   how='outer')
    df2 = pd.merge(df2, new_cons, on=['RegionID', 'SizeRankMSA', 'RegionName', 'RegionType', 'StateName'],
                   how='outer')
    df2['City'] = df2['RegionName'].apply(lambda x: x.split(',')[0])
    df2 = df2.drop(columns=['RegionName', 'RegionType', 'RegionID'])

    df2 = pd.merge(df2, metro_mapping[['Metro', 'City']], on='City', how='left')
    df2 = df2.drop(columns=['City'])

    df = pd.merge(df, df2, on=['Metro', 'StateName'])

    df = df.drop(columns=['StateName'])

    # Adding transit scores
    transit = transit.drop(columns='Unnamed: 0')
    transit = transit.rename(columns={x: 'Transit ' + x for x in ['Rank', 'Score', 'TCI', 'Jobs',
                                                                  'Trips/Week', 'Routes']})
    df = pd.merge(df, transit, on=['City', 'State'], how='left')

    return df
