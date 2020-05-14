from flask import Flask

app = Flask(__name__)  # set ame of app to name of module/file

@app.route('/') # when a request to route / (home page) comes in from a client
def index():
    return 'Hello World!' # print 'Hello World!' on page


if __name__ == '__main__':
    app.run()