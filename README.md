# Log analysis

This Python program is an **internal reporting tool** that uses information
from the *news* database to discover what kind of articles the site's readers
like.

## Getting the Database
The data for the `news` database can be downloaded [here](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip). You can unzip the `newsdata.sql` in your working directory and run it to create the tables.
Use the command `psql -d news -f newsdata.sql`.
If you get the error `psql: FATAL: database "news" does not exist` you have to create the empty database `news` first in the working directory.

After getting the data loaded, you can test viewing the tables using commands like `\dt`, `\d table` etc. Feel free to look around, you should find three tables.
- The `authors` table includes information about the authors of articles.
- The `articles` table includes the articles themselves.
- The `log table` includes one entry for each time a user has accessed the site.

You should run `log_analysis.py` from the directory in whick the `news` database is located in.

## Database tables
There are 3 tables on the *news* Database and here is a list the important data for
this version of the tool
* **authors** table which lists each author's unique **authors.id** and their **authors.name**
* **articles** table which lists:
 * **articles.author** to be paired with **authors.id**
 * **articles.slug** to be paired with the **log** table
* **log** table which lists
 * **log.path** to be edited using the [replace function](http://www.postgresqltutorial.com/postgresql-replace/)
 and be paired with **articles.slug**
 * **log.status** to identify *errors*
 * **log.time** as a timestamp. Aggregate into single days.
			 select time::date,
			 from log
			 group by time::date
			 order by 1;

## Queries
The psql queries are written near the top of the code, separate from the functions.
User can copy those to a text editor for better readability and editing.
- On *query_3* the percentage calculation code is complicated. Improvement needed.


##	Functions
The current version of the program produces only three reports, named accordingly
1. What are the most popular three articles of all time?
2. Who are the most popular article authors of all time?
3. On which days did more than 1% of requests lead to errors?

The results are correct but improvements can be made on the way results are displayed.
