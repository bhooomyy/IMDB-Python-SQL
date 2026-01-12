import pandas as pd 

############# cleaning people.tsv ##############
people_data=pd.read_csv('/Users/bhoomi/Documents/IMDBdataset/people.tsv',sep='\t',na_values=["\\N", ""])
#print(people_data.head())
#print(people_data.isna().sum())
'''
# primary name missing check
cnt=0
for index,row in people_data.iterrows():
    if pd.isna(row['primaryName']):
        cnt+=1
        print(row['nconst'])
print(cnt)
'''
# drop rows with missing primary name
people_data=people_data.dropna(subset=['primaryName'])


# death year less than birth year check, set death year to NaN if found
mask = (
    people_data["birthYear"].notna()
    & people_data["deathYear"].notna()
    & (people_data["deathYear"] < people_data["birthYear"])
)
people_data.loc[mask, "deathYear"] = pd.NA


# check for duplicates based on primaryName and birthYear, print them after sorting
dups=people_data[people_data.duplicated(subset=['primaryName','birthYear'],keep=False)].sort_values(by=['primaryName','birthYear'])
print(dups[['nconst', 'primaryName', 'birthYear','primaryProfession','knownForTitles']].head(60))

#Convert primaryProfession and knownForTitles to lists
people_data['knownForTitles_list']=people_data['knownForTitles'].fillna('').str.split(',')
people_data['primaryProfession_list']=people_data['primaryProfession'].fillna('').str.split(',')

# Merge primaryProfessiona if knownForTitles, primaryName and birthYear are same, sort based on primaryName and birthYear, print top 60 records
merge_primaryProfession=(
    people_data
    .groupby(['primaryName', 'birthYear', 'knownForTitles'], dropna=False, as_index=False)
    .agg(
        nconst=('nconst', 'first'),
        deathYear=('deathYear', 'first'),
        primaryProfession_list=('primaryProfession_list',
            lambda s: sorted({p.strip() for lst in s for p in lst if p and p.strip()}))
    )
).sort_values(by=['primaryName', 'birthYear'])
print(merge_primaryProfession.head(60))
