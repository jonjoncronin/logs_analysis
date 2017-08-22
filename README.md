<!-- TOC depthFrom:1 depthTo:6 withLinks:1 updateOnSave:1 orderedList:0 -->

	- [Summary](#summary)
	- [Resources](#resources)
		- [newsLogAnalyzer.py](#newsloganalyzerpy)
		- [pathcount SQL view](#pathcount-sql-view)
		- [dailysuccesses SQL view](#dailysuccesses-sql-view)
		- [dailyerrors SQL view](#dailyerrors-sql-view)
	- [Usage](#usage)
	- [Results](#results)
		- [command (1)](#command-1)
		- [command (2)](#command-2)
		- [command (3)](#command-3)
		- [command (q || Q)](#command-q-q)
		- [invalid command](#invalid-command)

<!-- /TOC -->
## Summary
As part of my re-education on full stack web development this repo contains the
delivery of the 3rd project laid out in the curriculum for the Udacity
Full stack web developer nanodegree.

This project is the first project connected to The Backend: Databases and
Applications section of the curriculum. It is intended to continue to build
on the Python skills I've been growing as well as to build some core SQL skills
and database concepts

The project description is fairly straight forward. We are given a database that
has been pre-populated with content relating to what could be a blog with
tables that represent articles, authors and logs of page views. Using a Python
script we are to connect to a postgresql server (that is running on a VM
hosted on the local machine) and pull certain data from the tables and display
it in a nice format. On the database server we are allowed to create SQL views
but are NOT to alter the database schema or table content.

## Resources
### newsLogAnalyzer.py
The newsLogAnalyzer module is really just a script. It does not define any new
classes or objects but it does utilize a few modules to make a connection
to a postgresql database server as well as to handle some nice formatting of
a date.

The newsLogAnalyzer provides a very simple command line interface menu that the
user can interact with in order to make the specific queries that are required
by the project.

The following commands and queries are supported -
1 - Display the 3 most popular articles by page views
2 - Display the most popular article authors by page view
3 - Display the days when there were more than 1% requests leading to errors
q - quit

### pathcount SQL view
A view was added to the news database to help simplify the SQL syntax and
queries to be performed by the newsLogAnalyzer. This pathcount view is intended
to return a table that has truncated the path column of the log table down to
match the slug column of the articles table as well as to give the count of
page requests for each path in the table.
```SQL
SELECT "substring"(log.path, '\/article\/+(.+)'::text) AS titlepath,
count(*) AS num
FROM log
GROUP BY log.path
ORDER BY (count(*)) DESC;
```

### dailysuccesses SQL view
A view was added to the news database to help simplify the SQL syntax and
queries to be performed by the newsLogAnalyzer. this dailysuccesses view is
intended to return a table that has truncated the timestamp of page requests
down to just the Month, Day, Year as well as count of '200 OK' statuses in the
log table.
```SQL
SELECT subquery.day, subquery.status, count(subquery.day) AS ok_count
FROM (
	SELECT to_char(log."time", 'YYYY:MM:DD'::text) AS day, log.status
	FROM log) subquery
WHERE subquery.status = '200 OK'::text
GROUP BY subquery.day, subquery.status
ORDER BY subquery.day;
```

### dailyerrors SQL view
A view was added to the news database to help simplify the SQL syntax and
queries to be performed by the newsLogAnalyzer. this dailyerrors view is
intended to return a table that has truncated the timestamp of page requests
down to just the Month, Day, Year as well as count of '404 ERROR' statuses in
the log table.
```SQL
SELECT subquery.day,subquery.status, count(subquery.day) AS error_count
FROM (
	SELECT to_char(log."time", 'YYYY:MM:DD'::text) AS day, log.status
	FROM log) subquery
WHERE subquery.status <> '200 OK'::text
GROUP BY subquery.day, subquery.status
ORDER BY subquery.day;
```

## Usage
Usage of this python script assumes quite a bit.
As the given "news" database needs to be running on a postgresql server and
server administration is beyond the scope of this project I will simply ask you
to refer to the pages from the Udacity site that describe how to "Prepare the
software and data" for this project. The quick summary is that you need a VM
running locally that has a postgresql server running and that has python3
installed.

The python script needs to be copied or available to that server/VM as the
script will be making a local connection to the "news" database being hosted
there.

- Open a terminal window on the VM/server.
- Navigate to the location of the newsLogAnalyzer.py script.
- Execute the script - $> python3 newsLogAnalyzer.py
	* You will be prompted with the following CLI
```
	Please select an action -
	===================================================
	1 - Display the 3 most popular articles of all time
	2 - Display the most popular article authors of all time
	3 - Display the days when there were more than 1% requests leading to errors
	q - quit
```
- Make your selection (1,2,3 or q) and wait for your results

## Results
### command (1)
```
3 most popular articles by page view:
 Views  | Article Title
==================================================
 338647 - Candidate is jerk, alleges rival
 253801 - Bears love berries, alleges bear
 170098 - Bad things gone, say good people
```
### command (2)
```
Author Popularity by cummulative page views:
 Views  | Author
==================================================
 507594 - Ursula La Multa
 423457 - Rudolf von Treppenwitz
 170098 - Anonymous Contributor
  84557 - Markoff Chaney
```
### command (3)
```
Days where more than 1% of page requests were errors:
==================================================
Jul 17 2016 had 2.32% errors
```
### command (q || Q)
```
Thanks for stopping bye -
```
### invalid command
```
You've entered an invalid command - please try again
```
