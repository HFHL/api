import os

from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/")
def read_root():
    return {"Hello": "World"}

# 传入姓名参数，并打印出来
@app.route("/hello/<name>")
def hello_name(name):
    return {"Hello": name}


if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port=int(os.environ.get('PORT', 80)))