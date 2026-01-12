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