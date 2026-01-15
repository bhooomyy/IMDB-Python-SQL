# IMDb Dataset Analysis (Python → SQL)

## Project Status
**Current Stage:** Basic Level (Data Cleaning & Foundational Analysis)  
**Next Stage:** Intermediate Analysis (Decade rankings, advanced joins, SQL translation)

---

## Dataset Source
This project uses the official public IMDb datasets provided in TSV format.

Source: https://datasets.imdbws.com/

Missing values represented as `\N` in the raw files are treated as null values during ingestion.

---

## Datasets Used
 Original_Dataset_Name -> Rename_Dataset_Name - Description
- `name.basics.tsv` -> `people.tsv` – People metadata
- `title.basics.tsv` –> `titles.tsv` - Core title information
- `title.ratings.tsv` -> `title_ratings.tsv` – IMDb ratings and vote counts
- `title.episode.tsv` -> `title_episode.tsv` – TV episode metadata
- `title.principals.tsv` ->`title_principals.tsv` – Cast and principal crew
- `title.crew.tsv` -> `title_crew.tsv` – Directors and writers
- `title.akas.tsv` -> `title_alternates.tsv` – Alternate titles and regions

---

## Tech Stack

- **Language:** Python 3
- **Libraries:** pandas, numpy
- **Data Format:** TSV (IMDb standard)
- **Future Extension:** SQL (PostgreSQL / SQLite)

---

## Data Cleaning & Validation

### `name.basics.tsv` (People)
- Removed records with missing `primaryName`
- Validated life-span data and corrected invalid cases where:
  - `deathYear < birthYear` → `deathYear` set to null
- Identified potential duplicate people using:
  - `primaryName` + `birthYear`
- Converted multi-valued fields into list format:
  - `primaryProfession`
  - `knownForTitles`
- Consolidated duplicate people records (same name, birth year, known titles) by:
  - Merging and deduplicating `primaryProfession`

---

### `title.akas.tsv` (Alternate Titles)
- Checked for duplicate records using composite key:
  - `titleId` + `ordering`
- Flagged duplicates for further validation

---

### `title.crew.tsv`
- Performed null-value checks across all columns
- Retained all records while identifying incomplete fields

---

### `title.episode.tsv`
- Identified duplicate episode records using:
  - `tconst`, `parentTconst`, `seasonNumber`, `episodeNumber`
- Removed records with missing title identifiers
- Performed null-value analysis for data completeness

---

### `title.principals.tsv`
- Removed records with missing `tconst` to maintain referential integrity

---

### `title.ratings.tsv`
- Removed records with missing `tconst`
- Ensured rating data is clean and joinable with title metadata

---

### `title.basics.tsv`
- Removed records with missing `tconst`
- Retained essential metadata:
  - `titleType`
  - `primaryTitle`
  - `startYear`
  - `genres`

---

## Exploratory Analysis (Basic Level)

### Movie Analysis
- Filtered titles where `titleType = 'movie'`
- Listed the first 50 movies released between **2010 and 2015**
- Results sorted by release year (`startYear`)

---

### Title Type Distribution
- Counted total titles for each `titleType`
- Displayed results in descending order
- Used to understand dataset composition

---

### Ratings Analysis
- Identified titles with at least **50,000 votes**
- Ranked titles by `averageRating`
- Joined rating data with title metadata
- Identified titles with **no rating information available** using left joins

---

### TV Series Episode Analysis
- Filtered titles where `titleType = 'tvSeries'`
- Joined series metadata with episode data
- Calculated total number of episodes per series
- Listed top 20 TV series with the highest episode count

---

### People / Actor Analysis
- Filtered people whose `primaryProfession` includes:
  - `actor`
  - `actress`
- Prepared dataset for appearance-based aggregation

---

## Current Coverage
At this stage, the project demonstrates:

- Real-world data cleaning and validation
- Handling of multi-valued IMDb fields
- Duplicate detection and consolidation logic
- Multi-table joins using pandas
- Foundational exploratory data analysis
- IMDb-compliant dataset handling

---

## Intermediate Analysis 

At the intermediate stage, the project moves beyond descriptive statistics into ranking, aggregation, and multi-dimensional comparisons, closely mirroring real-world SQL analytics problems.

### Decade-Based Title Rankings
- Ranked titles per decade and per `titleType`
- Used `averageRating` as the primary ranking metric
- Applied `numVotes` as a deterministic tie-breaker
- Implemented SQL-style window logic using ordered sorting + `groupby().cumcount()` (ROW_NUMBER equivalent)
- Extracted top 10 titles per decade per title type

### Regional & Language Reach Analysis
- Focused on movies and TV series only
- Joined core title metadata with alternate title data
- Measured international reach using:
  - Distinct regions
  - Distinct languages
  - Total alternate title records
- Ranked and extracted the top 100 titles with the widest regional and language coverage



## Advanced Analysis

The advanced stage introduces weighted metrics and career-aware analytics, focusing on relative performance rather than absolute thresholds.

### Actor–Director Collaboration Analysis
- Filtered actor/actress credits from `title.principals`
- Normalized multi-director titles using split + explode
- Created actor–director pairs per title and joined ratings data
- Computed success metrics per (director, actor):
  - `num_movie_cnt` (unique shared titles)
  - `total_votes` (sum of votes)
  - `weighted_rating` = sum(`averageRating` × `numVotes`) / sum(`numVotes`)
- Ranked and extracted the top 100 actor–director pairings by `weighted_rating`, then collaboration count and votes

### Breakout Performance Detection (Popularity Surge)
- Built chronological filmographies per actor/actress using `startYear`
- Computed rolling baselines over the previous 5 titles (shifted to avoid leakage):
  - `baseline_votes` (rolling mean of votes)
  - `baseline_rating` (rolling mean of ratings)
- Flagged breakout titles where:
  - `numVotes` ≥ 3 × `baseline_votes`
  - `averageRating` ≥ `baseline_rating`
- Selected the first breakout title per actor/actress and printed key comparison metrics