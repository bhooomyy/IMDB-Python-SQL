import pandas as pd
people_data=pd.read_csv('/Users/bhoomi/Documents/IMDBdataset/people.tsv',sep='\t',na_values=["\\N", ""],low_memory=True)
title_alternates_data=pd.read_csv('/Users/bhoomi/Documents/IMDBdataset/title_alternates.tsv',sep='\t',na_values=["\\N", ""],low_memory=True)
title_episode_data=pd.read_csv('/Users/bhoomi/Documents/IMDBdataset/title_episode.tsv',sep='\t',na_values=["\\N", ""],low_memory=True)
title_crew_data=pd.read_csv('/Users/bhoomi/Documents/IMDBdataset/title_crew.tsv',sep='\t',na_values=["\\N", ""],low_memory=True)
title_principals_data=pd.read_csv('/Users/bhoomi/Documents/IMDBdataset/title_principals.tsv',sep='\t',na_values=["\\N", ""],low_memory=True)
title_ratings_data=pd.read_csv('/Users/bhoomi/Documents/IMDBdataset/title_ratings.tsv',sep='\t',na_values=["\\N", ""],low_memory=True)
titles_data=pd.read_csv('/Users/bhoomi/Documents/IMDBdataset/titles.tsv',sep='\t',na_values=["\\N", ""],low_memory=True)


# Intermediate
# List the top 10 titles per decade (for each titleType) ranked by averageRating, breaking ties by numVotes.
titles_leftJoin_titleRatings=pd.merge(titles_data[['tconst','titleType','primaryTitle','startYear']],title_ratings_data[['tconst','averageRating','numVotes']],on='tconst',how='inner')
#print(titles_leftJoin_titleRatings.head(60))
titles_leftJoin_titleRatings['decade']=(titles_leftJoin_titleRatings['startYear']//10)*10
titles_leftJoin_titleRatings = titles_leftJoin_titleRatings.sort_values(
    by=['decade', 'titleType', 'averageRating', 'numVotes'],
    ascending=[True, True, False, False]
)
titles_leftJoin_titleRatings['rank']=titles_leftJoin_titleRatings.groupby(['decade','titleType']).cumcount()+1
top_10_titles=titles_leftJoin_titleRatings[titles_leftJoin_titleRatings['rank']<=10]
print(top_10_titles[['titleType','primaryTitle','startYear','decade','rank','averageRating','numVotes']].sort_values(['decade','titleType','rank']).head(60))
