import os

from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world(name:str):
    return 'Welcome to the world!',name

@app.post('/login')
def login(name:str):
    return 'Welcome to login!',name


if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port=int(os.environ.get('PORT', 80)))