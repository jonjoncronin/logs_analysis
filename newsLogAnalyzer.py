#!/usr/local/bin/python3
import sys
import psycopg2
from code import InteractiveConsole
from datetime import datetime

__author__ = "Jon Cronin"

DBNAME = "news"


def connectAndQuery(someSqlQuery):
    """
    Connect to the news database and make a query on behalf of the
    caller.
    someSqlQuery -- some string containing the SQL statement to be sent
    to the DB
    returns -- a dictionary containing the string values returned from
    the DB
    """
    # print("executing someSqlQuery")
    dbConnection = psycopg2.connect(database=DBNAME)
    dbCursor = dbConnection.cursor()
    dbCursor.execute(someSqlQuery)
    output = dbCursor.fetchall()
    dbConnection.close()
    return output


def queryPopArticles():
    """
    Queries for the 3 most popular articles by page view and
    prints them out in a nice format.
    """
    # print("executing command 1")
    output = connectAndQuery("select title,num              \
                           from articles                    \
                           join pathcount on slug=titlepath \
                           limit 3;")
    print("3 most popular articles by page view:")
    print(" Views  | Article Title ")
    print("==================================================")
    for row in output:
        print('{0:7} - {1}'.format(row[1], row[0]))


def queryPopAuthors():
    """
    Queries for the most read authors by cummulative page
    views and prints them out in a nice format.
    """
    # print("executing command 2")
    output = connectAndQuery("select authors.name, SUM(num) \
                          from authors                   \
                          join articles on authors.id=articles.author \
                          join pathcount on articles.slug=pathcount.titlepath \
                          group by authors.name          \
                          order by SUM(num) desc;")
    print("Author Popularity by cummulative page views:")
    print(" Views  | Author ")
    print("==================================================")
    for row in output:
        print('{0:7} - {1}'.format(row[1], row[0]))


def queryBadRequests():
    """
    Queries for the days where the number of page requests that
    result in errors is > (greater than) 1% the totoal number of
    page requests for that day. Displays that result in a nice format.
    """
    # print("executing command 3")
    output = connectAndQuery("select dailysuccesses.day,            \
            (cast(error_count as float)/cast(ok_count as float)) as pcterrors\
            from dailysuccesses          \
            join dailyerrors on dailysuccesses.day=dailyerrors.day \
            where (cast(error_count as float)/cast(ok_count as float)) > .01;")
    print("Days where more than 1% of page requests were errors:")
    print("==================================================")
    for row in output:
        someDate = datetime.strptime(row[0], "%Y:%m:%d")
        pctError = float(row[1]) * 100.00
        print('{0} had {1:.2f}% errors'.format(
            someDate.strftime('%b %d %Y'), pctError))


def displayUserMenu():
    """
    Displays a simple user menu/CLI prompt to allow the user to
    specify what queries they want to see.
    """
    print("\nPlease select an action - ")
    print("===================================================")
    print("1 - Display the 3 most popular articles by page views")
    print("2 - Display the most popular article authors by page view")
    print("3 - Display the days when there were more than 1% requests leading"
          " to errors")
    print("q - quit")


def cli_prompt():
    """
    Main running loop of the script which displays the command prompt
    allowing the user to trigger a query or quit.
    """
    while True:
        displayUserMenu()
        command = InteractiveConsole.raw_input(": ")
        if command == '1':
            queryPopArticles()
        elif command == '2':
            queryPopAuthors()
        elif command == '3':
            queryBadRequests()
        elif command == 'q' or command == 'Q':
            print("Thanks for stopping bye - ")
            break
        else:
            print("You've entered an invalid command - please try again")


cli_prompt()
