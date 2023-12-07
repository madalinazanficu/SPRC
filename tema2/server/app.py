
from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'My server is running!'

if __name__ == '__main__':
    app.run('0.0.0.0', port = 6000, debug = True)