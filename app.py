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


def fetchBasedOnNameAndState(name, state):
    SELECT_FROM_PEOPLE_BASED_ON_NAME_AND_STATE_QUERY = " SELECT * from people "
    getConnection()
    cursor = cnx.cursor()
    if name or state:
        SELECT_FROM_PEOPLE_BASED_ON_NAME_AND_STATE_QUERY += " Where "
    if name:
        SELECT_FROM_PEOPLE_BASED_ON_NAME_AND_STATE_QUERY += " Name LIKE " + "'" + name + "'"
    if state and name:
        SELECT_FROM_PEOPLE_BASED_ON_NAME_AND_STATE_QUERY += " OR "
    if state:
        SELECT_FROM_PEOPLE_BASED_ON_NAME_AND_STATE_QUERY += " State LIKE " + "'" + state + "'"
    print(SELECT_FROM_PEOPLE_BASED_ON_NAME_AND_STATE_QUERY)
    cursor.execute(SELECT_FROM_PEOPLE_BASED_ON_NAME_AND_STATE_QUERY)
    people = cursor.fetchall()
    cnx.close()
    return people


@app.route('/', methods=['GET', 'POST'])
def search():
    global data
    print(request.method)
    if request.method == "POST":
        print('Here')
        name = request.form['name']
        state = request.form['state']
        print(name, state)
        data = fetchBasedOnNameAndState(name, state)
    else:
        print('Get')
        data = fetchAllData()
    return render_template('index.html', data=data)


@app.route('/status')
def hello_world():
    return "Hello World"


if __name__ == '__main__':
    app.run()
