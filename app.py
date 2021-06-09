from flask import Flask, render_template
# import pyodbc

app = Flask(__name__)

# server = os.getenv('SERVER_NAME')
# database = os.getenv('DB_NAME')
# username = os.getenv('USERNAME')
# password = os.getenv('PASSWORD')
# port = os.getenv('PORT')

# server = 'vighnesh-cloud-computing.database.windows.net'
# database = 'cloud_computing'
# username = 'vighnesh@vighnesh-cloud-computing'
# password = 'kira#552888'
# port = 1433
# driver = '/opt/homebrew/etc/odbcinst.ini'
#
# with pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password) as conn:
#     with conn.cursor() as cursor:
#         cursor.execute("SELECT TOP 3 name, collation_name FROM sys.databases")
#         row = cursor.fetchone()
#         while row:
#             print (str(row[0]) + " " + str(row[1]))
#             row = cursor.fetchone()


@app.route('/')
def user_directory():
    return render_template('index.html')


@app.route('/status')
def hello_world():
    return "Hello World"


if __name__ == '__main__':
    app.run()
