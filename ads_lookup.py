import ads
import pandas as pd


table_path = 'tables/query_simbad_earnshaw.csv'
print(f'Loading {table_path}')
df = pd.read_csv(table_path)

unique_bibcodes = df['COO_BIBCODE'].unique()
print('unique_bibcodes:')
print(unique_bibcodes)

df_u = df.drop_duplicates(subset=['COO_BIBCODE'])

all_res = []
for i, r in df_u.iterrows():
    bibcode = r['COO_BIBCODE']
    main_id = r['MAIN_ID']

    print(f'Searching ADS main_id = {main_id} bibcode = {bibcode}')
    search_query = ads.SearchQuery(bibcode=bibcode)
    print(f'search_query : {search_query}')

    res = {}
    res['bibcode'] = bibcode
    res['main_id'] = main_id

    for sc in search_query:
        print(main_id, bibcode, sc.title)
        res['paper_title'] = sc.title

    all_res.append(res)


df_res = pd.DataFrame(all_res)
print(df_res)
