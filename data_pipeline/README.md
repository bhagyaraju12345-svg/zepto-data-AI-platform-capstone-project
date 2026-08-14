# Module 1 — Data Pipeline

## Overview

This module implements an end-to-end catalog data pipeline using
Books to Scrape as the public scraping-practice website.

The pipeline performs:

1. Web scraping using Requests and BeautifulSoup.
2. Data cleaning and type conversion.
3. GBP to INR currency conversion.
4. Normalization into a relational SQLite database.
5. SQL querying.
6. Pandas analysis using `pd.read_sql()`.
7. Reproduction of a SQL JOIN using `pd.merge()`.

---

## Data Source

Source:

Books to Scrape

https://books.toscrape.com/

The first five pages of the All Products catalogue are scraped.

Each page contains approximately 20 books, resulting in approximately
100 scraped books.

The final dataset must contain at least 60 books and at least
3 categories.

---

## Project Structure

```text
data_pipeline/
│
├── pipeline.py
├── requirements.txt
├── README.md
├── books_raw.csv
├── books_clean.csv
├── books.db
├── sql_queries.sql
├── sql_outputs.txt
└── merge_comparison.csv

Scraping

The pipeline uses:

requests
BeautifulSoup

The following fields are scraped:

title
price
star_rating
availability
category

The first five All Products catalogue pages are used.

Cleaning Decisions
Price

The website provides prices with the GBP currency symbol.

For example:

£51.77

The currency symbol is removed and the value is converted to a
floating-point number:

51.77

The resulting column is:

price_gbp

Unexpected numeric parsing failures are converted to missing values
using errors="coerce".

Missing or invalid numeric prices are replaced with the median price
of the valid observations.

Rating

The website provides ratings as text:

One
Two
Three
Four
Five

These are converted to:

1
2
3
4
5

The resulting column is:

rating

Unexpected rating values are treated as missing and median-imputed.

Availability

Availability is converted to a Boolean value:

In stock      -> True
Out of stock  -> False

Unexpected availability values cannot be safely inferred.

Therefore rows with an unparseable availability value are dropped
rather than assigning an incorrect stock status.

This is preferable because an incorrect stock status could introduce
misleading catalog information.

Currency Conversion

The assignment requires the fixed project-defined conversion rate:

1 GBP = 105.50 INR

This is an artificial fixed baseline specified by the project.

No live exchange-rate API is used.

The calculation is:

price_inr = price_gbp × 105.50

The resulting column is:

price_inr

This fixed rate is used consistently throughout the pipeline.

Database Design

SQLite is used as the relational database.

The database contains two normalized tables.

categories
category_id     INTEGER PRIMARY KEY
category_name   TEXT UNIQUE
books
book_id
title
price_gbp
price_inr
rating
in_stock
category_id

books.category_id is a foreign key referencing:

categories.category_id

This prevents repeated category information from being stored in
every book record.

SQL Analysis

At least five SQL queries are executed.

The queries collectively demonstrate:

SELECT
WHERE
ORDER BY
LIMIT
DISTINCT
BETWEEN
JOIN

The SQL query strings are saved in:

sql_queries.sql

Their executed outputs are saved in:

sql_outputs.txt

Pandas Analysis

Multiple SQL query results are loaded using:

pd.read_sql()

The normalized books and categories tables are also loaded into
Pandas.

The SQL JOIN is independently reproduced using:

pd.merge()

The SQL JOIN result and Pandas merge result are compared for equality.

The comparison is saved in:

merge_comparison.csv

Generated Files

After running the pipeline:

books_raw.csv

contains the original scraped data.

books_clean.csv

contains cleaned and converted data.

books.db

contains the normalized SQLite database.

sql_queries.sql

contains the SQL queries.

sql_outputs.txt

contains the query outputs.

merge_comparison.csv

contains the SQL JOIN versus pandas.merge comparison.

Reproducibility

The database is recreated from scratch every time pipeline.py is
executed.

Existing SQLite tables are dropped and recreated.

Therefore the complete database can be regenerated from the scraper
without manual intervention.

Validation

The pipeline validates:

At least 60 books
At least 3 categories
No missing price_gbp
Rating values between 1 and 5
No missing in_stock
No missing price_inr
SQL JOIN and pd.merge() results are equivalent

If a validation fails, the pipeline stops with an informative error.

Validation

The pipeline validates:

At least 60 books
At least 3 categories
No missing price_gbp
Rating values between 1 and 5
No missing in_stock
No missing price_inr
SQL JOIN and pd.merge() results are equivalent

