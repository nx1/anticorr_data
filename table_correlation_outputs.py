from process_corr import load_df_prop, load_df_fit_samples, load_df_fit_values

print('Loading df_prop...')
df_prop = load_df_prop()
print('Removing duplicates...')
df_prop = df_prop.drop(labels=['include_bad'], axis=1)
df_prop = df_prop.drop(labels=['include_UL'], axis=1)
df_prop = df_prop.drop_duplicates()

print(df_prop)

df_prop_outpath = 'tables/correlation_N_datapoints.csv'
print(f'saving df_prop_to: {df_prop_outpath}')
df_prop.to_csv(df_prop_outpath, index=False)

print('Loading df_fit_samples...')
df_fit_samples = load_df_fit_samples()
print(df_fit_samples)

df_fit_samples_outpath = 'tables/fit_samples.csv'
print(f'saving df_prop_to: {df_fit_samples_outpath}')
# df_fit_samples.to_csv(df_fit_samples_outpath, index=False)



print('Loading df_fit_values...')
df_fit_values = load_df_fit_values()
print(df_fit_values)

df_fit_values_outpath = 'tables/correlation_fit_values.csv'
print(f'saving df_fit_values to: {df_fit_values_outpath}')
df_fit_values.to_csv(df_fit_values_outpath, index=False)
