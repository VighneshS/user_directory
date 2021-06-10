import json

from flask import Flask, render_template, request
import os
import mysql.connector
from mysql.connector import errorcode

app = Flask(__name__)

server = os.environ['UD_HOST_NAME']
database = os.environ['UD_DB_NAME']
username = os.environ['UD_DB_USERNAME']
password = os.environ['UD_DB_PASSWORD']

SELECT_ALL_FROM_PEOPLE_QUERY = "SELECT * FROM people"


class SearchParams(dict):

    # __init__ function
    def __init__(self):
        self = dict()

    # Function to add key:value
    def add(self, key, value):
        self[key] = value


def getConnection():
    global cnx
    try:
        cnx = mysql.connector.connect(user=username, password=password,
                                      host=server,
                                      database=database)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    return cnx


def fetchAllData():
    getConnection()
    cursor = cnx.cursor()
    cursor.execute(SELECT_ALL_FROM_PEOPLE_QUERY)
    people = cursor.fetchall()
    cnx.close()
    return people


def fetchBasedOnNameAndState(searchParams):
    SELECT_FROM_PEOPLE_BASED_ON_NAME_AND_STATE_QUERY = " SELECT * from people "
    getConnection()
    cursor = cnx.cursor()
    if searchParams:
        SELECT_FROM_PEOPLE_BASED_ON_NAME_AND_STATE_QUERY += " Where "
    else:
        return fetchAllData()
    count = 0
    for key in searchParams:
        if count > 0:
            SELECT_FROM_PEOPLE_BASED_ON_NAME_AND_STATE_QUERY += " OR "
        SELECT_FROM_PEOPLE_BASED_ON_NAME_AND_STATE_QUERY += " " + key + " LIKE " + "'%" + searchParams[key] + "%'"
        count += 1

    print(SELECT_FROM_PEOPLE_BASED_ON_NAME_AND_STATE_QUERY)
    cursor.execute(SELECT_FROM_PEOPLE_BASED_ON_NAME_AND_STATE_QUERY)
    people = cursor.fetchall()
    cnx.close()
    return people


@app.route('/', methods=['GET', 'POST'])
def search():
    global data
    searchParams: SearchParams = SearchParams()
    if request.method == "POST":
        if request.form['name']:
            searchParams.add('Name', request.form['name'])
        if request.form['state']:
            searchParams.add('State', request.form['state'])
        if request.form['salary']:
            searchParams.add('Salary', request.form['salary'])
        if request.form['grade']:
            searchParams.add('Grade', request.form['grade'])
        if request.form['room']:
            searchParams.add('Room', request.form['room'])
        if request.form['telnum']:
            searchParams.add('Telnum', request.form['telnum'])
        if request.form['keywords']:
            searchParams.add('Keywords', request.form['keywords'])
        data = fetchBasedOnNameAndState(searchParams)
    else:
        data = fetchAllData()
    return render_template('index.html', data=data)


@app.route('/getUserByName', methods=['POST'])
def getUserByName():
    global data
    searchParams: SearchParams = SearchParams()
    if request.form['name']:
        searchParams.add('Name', request.form['name'])
    return json.dumps(fetchBasedOnNameAndState(searchParams))


@app.route('/status')
def hello_world():
    return "Hello World"


if __name__ == '__main__':
    app.run()
