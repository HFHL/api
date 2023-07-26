import os

from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world(name:str):
    return 'Welcome to the world!',name

# 带参的登录，参数为name，返回name
@app.route('/login/<name>')
def login(name:str):
    return 'Hello, %s' % name


if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port=int(os.environ.get('PORT', 80)))