import json

from flask import Flask, render_template, request, redirect
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


def fetchBasedOnSearchQuery(searchParams):
    SELECT_FROM_PEOPLE_BASED_ON_NAME_AND_STATE_QUERY = " SELECT * from people where id = '" + searchParams['id'] + "'"
    getConnection()
    cursor = cnx.cursor()
    print(SELECT_FROM_PEOPLE_BASED_ON_NAME_AND_STATE_QUERY)
    cursor.execute(SELECT_FROM_PEOPLE_BASED_ON_NAME_AND_STATE_QUERY)
    people = cursor.fetchall()
    cnx.close()
    return people


def fetchBasedOnRoomQuery(searchParams):
    SELECT_FROM_PEOPLE_BASED_ON_NAME_AND_STATE_QUERY = " SELECT * from people where room between " + searchParams[
        'roomFrom'] + " AND " + searchParams['roomTo']
    getConnection()
    cursor = cnx.cursor()
    print(SELECT_FROM_PEOPLE_BASED_ON_NAME_AND_STATE_QUERY)
    cursor.execute(SELECT_FROM_PEOPLE_BASED_ON_NAME_AND_STATE_QUERY)
    people = cursor.fetchall()
    cnx.close()
    return people


def saveBasedOnName(editParams):
    UPDATE_PEOPLE_BASED_ON_NAME_QUERY = " UPDATE people "
    getConnection()
    cursor = cnx.cursor()
    if editParams:
        UPDATE_PEOPLE_BASED_ON_NAME_QUERY += " SET "
    else:
        return fetchAllData()
    count = 0
    for key in editParams:
        if key != 'targetName':
            if count > 0:
                UPDATE_PEOPLE_BASED_ON_NAME_QUERY += ' , '
            UPDATE_PEOPLE_BASED_ON_NAME_QUERY += key + " = " + "'" + editParams[key] + "'"
            count += 1
    UPDATE_PEOPLE_BASED_ON_NAME_QUERY += " where Name = '" + editParams['targetName'] + "' "
    print(UPDATE_PEOPLE_BASED_ON_NAME_QUERY)
    try:
        # Execute the SQL command
        cursor.execute(UPDATE_PEOPLE_BASED_ON_NAME_QUERY)

        # Commit your changes in the database
        cnx.commit()
    except:
        # Rollback in case there is any error
        cnx.rollback()
    cnx.close()


def deleteBasedOnName(targetName: str):
    DELETE_PEOPLE_BASED_ON_NAME_QUERY = " DELETE people WHERE Name='" + targetName + "' "
    getConnection()
    cursor = cnx.cursor()
    try:
        # Execute the SQL command
        cursor.execute(DELETE_PEOPLE_BASED_ON_NAME_QUERY)

        # Commit your changes in the database
        cnx.commit()
    except:
        # Rollback in case there is any error
        cnx.rollback()
    cnx.close()


@app.route('/', methods=['GET', 'POST'])
def search():
    return render_template('index.html')


@app.route('/find', methods=['GET', 'POST'])
def find():
    global data
    data = []
    searchParams: SearchParams = SearchParams()
    if request.method == "POST":
        if request.form['id']:
            searchParams.add('id', request.form['id'])
            data = fetchBasedOnSearchQuery(searchParams)
    return render_template('find.html', data=data)


@app.route('/findByRoom', methods=['GET', 'POST'])
def findByRoom():
    global data
    data = []
    searchParams: SearchParams = SearchParams()
    if request.method == "POST":
        if request.form['roomFrom']:
            searchParams.add('roomFrom', request.form['roomFrom'])
        if request.form['roomTo']:
            searchParams.add('roomTo', request.form['roomTo'])
        data = fetchBasedOnSearchQuery(searchParams)
    return render_template('find.html', data=data)


@app.route('/getUserByName', methods=['POST'])
def getUserByName():
    global data
    searchParams: SearchParams = SearchParams()
    if request.form['name']:
        searchParams.add('Name', request.form['name'])
    return json.dumps(fetchBasedOnSearchQuery(searchParams))


@app.route('/update', methods=['POST'])
def updateUserByName():
    global data
    editParams: SearchParams = SearchParams()
    if request.form['name']:
        editParams.add('targetName', request.form['targetName'])
        editParams.add('Name', request.form['name'])
        editParams.add('State', request.form['state'])
        saveBasedOnName(editParams)
    return redirect('/')


@app.route('/delete', methods=['DELETE'])
def deleteUserByName():
    if request.form['targetName']:
        deleteBasedOnName(request.form['targetName'])
    return redirect('/')


@app.route('/status')
def hello_world():
    return "Hello World"


if __name__ == '__main__':
    app.run()
