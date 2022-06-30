import ads
import pandas as pd

df = pd.read_csv('tables/query_simbad_earnshaw.csv')
unique_bibcodes = df['COO_BIBCODE'].unique()

df_u = df.drop_duplicates(subset=['COO_BIBCODE'])

all_res = []

for i, r in df_u.iterrows():
    bibcode = r['COO_BIBCODE']
    main_id = r['MAIN_ID']

    papers = ads.SearchQuery(bibcode=bibcode)

    res = {}
    res['bibcode'] = bibcode
    res['main_id'] = main_id

    for paper in papers:
        print(main_id, bibcode, paper.title)
        res['paper_title'] = paper.title

    all_res.append(res)


df_res = pd.DataFrame(all_res)
print(df_res)
