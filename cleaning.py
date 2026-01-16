import pandas as pd 

############# cleaning people.tsv ##############
people_data=pd.read_csv('/Users/bhoomi/Documents/IMDBdataset/people.tsv',sep='\t',na_values=["\\N", ""],low_memory=True)
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


############### cleaning titlealternates.tsv #################
title_alternates_data=pd.read_csv('/Users/bhoomi/Documents/IMDBdataset/title_alternates.tsv',sep='\t',na_values=["\\N", ""],low_memory=True)
duplicates=title_alternates_data[title_alternates_data.duplicated(subset=['titleId','ordering'],keep=False)].sort_values(by=['titleId','ordering'])
print(duplicates.head(60))      #Empty


############### cleaning title_crew.tsv #################
title_crew_data=pd.read_csv('/Users/bhoomi/Documents/IMDBdataset/title_crew.tsv',sep='\t',na_values=["\\N", ""],low_memory=True)
empty=title_crew_data.isna().any()
#title_crew_data=title_crew_data.dropna(subset=['tconst'])
print(empty)        #empty


################ cleaning title_episode.tsv #################
title_episode_data=pd.read_csv('/Users/bhoomi/Documents/IMDBdataset/title_episode.tsv',sep='\t',na_values=["\\N", ""],low_memory=True)
duplicate_title_episode=title_episode_data[title_episode_data.duplicated(subset=['tconst','parentTconst','seasonNumber','episodeNumber'],keep=False)].sort_values(by=['tconst','parentTconst'])
empty=title_episode_data.isna().any()
print(empty)        #empty


################ cleaning title_principals.tsv #################
title_principals_data=pd.read_csv('/Users/bhoomi/Documents/IMDBdataset/title_principals.tsv',sep='\t',na_values=["\\N", ""],low_memory=True)
title_episode_data=title_episode_data.dropna(subset=['tconst'])


################# cleaning title_ratings.tsv #################
title_ratings_data=pd.read_csv('/Users/bhoomi/Documents/IMDBdataset/title_ratings.tsv',sep='\t',na_values=["\\N", ""],low_memory=True)
title_ratings_data=title_ratings_data.dropna(subset=['tconst'])


################# cleaning titles.tsv #################
titles_data=pd.read_csv('/Users/bhoomi/Documents/IMDBdataset/titles.tsv',sep='\t',na_values=["\\N", ""],low_memory=True)
titles_data=titles_data.dropna(subset=['tconst'])
