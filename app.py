from flask import Flask, render_template
from flask_bootstrap import Bootstrap

app = Flask(__name__)
Bootstrap(app)


@app.route('/')
def user_directory():
    return render_template('index.html')


@app.route('/status')
def hello_world():
    return "Hello World"


if __name__ == '__main__':
    app.run()
