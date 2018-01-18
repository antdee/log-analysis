#!/usr/bin/env python2.7
# -*- coding: ascii -*-

"""
This program runs queries to the 'news' database prints out the results.
"""

import datetime

import psycopg2


DBNAME = "news"

query_1 = """
select articles.title,
       count(log.path) as views
from articles, log
where articles.slug = replace(log.path, '/article/', '')
group by articles.title
order by views desc
limit 3;
"""

query_2 = """
select authors.name,
       count(log.path) as views
from articles, log, authors
where articles.slug = replace(log.path, '/article/', '')
and articles.author = authors.id
group by authors.name
order by views desc;
"""

# num = total number of views
# num_er = number of views that resulted in errors
# Improvement wanted for the percentage calculation
query_3 = """
select time as day,
       round( CAST(float8 (num_er / num::float) * 100 as numeric), 2)
       as error_percentage
from (select time::date,
             count(*) as num,
             count(*) filter (where status = '404 NOT FOUND') as num_er
      from log
      group by time::date
      order by 1)
      as view_3
where round( CAST(float8 (num_er / num::float) * 100 as numeric), 2) >= 1
order by error_percentage desc;
"""


def connect(database_name, query):
    """Connect to the database provided, execute the query provided"""
    # try:
    db = psycopg2.connect(database=database_name)
    c = db.cursor()
    c.execute(query)
    data = c.fetchall()
    db.close()
    return data
    # except:
    # print "An unknown error has occured"


def report_1():
    """Scan the tables articles, log. Replace the log.path to remove /article/
       use it as a common key and take the views count from the log table."""
    # try:
    print "\nReport 1"
    print "What are the most popular three articles of all time?\n"
    for n in connect(DBNAME, query_1):
        print "Article ", n[0], " has ", n[1], "number of views"
    # except:
        # print "An unknown error has occured"


def report_2():
    """Scan the tables articles, log. Replace the log.path to remove /article/
       use it as a common key and take the views count from the log table.
       Group by authors.name to get the desired result."""
    # try:
    print "\nReport 2"
    print "Who are the most popular article authors of all time?\n"
    for n in connect(DBNAME, query_2):
        print n[1], "number of views for author ", n[0]
    # except:
        # print "An unknown error has occured"


def report_3():
    """Aggregate timestamps into single days, count views per day, count errors.
       Save into view_3.
       Calculate percentage of errors in views per day.
       Display above selected threshold"""
    # try:
    print "\nReport 3"
    print "On which days did more than 1% of requests lead to errors?\n"
    for n in connect(DBNAME, query_3):
        print n[0], " ", n[1], "% of the requests led to errors"
    # except:
        # print "An unknown error has occured"


if __name__ == '__main__':
    report_1()
    report_2()
    report_3()
