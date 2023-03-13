from flask import Flask
from flask import request

app = Flask(__name__)


@app.route("/result", methods = ["POST", "GET"])
def result():
    if request.method == "GET":
        return {"API" : "hakdog ka"}
    
    elif request.method == "POST":
        num1 = request.json.get('num1')
        num2 = request.json.get('num2')

        cal = {}

        cal['addition'] = num1+num2
        cal['subtraction'] = num1-num2

        return (cal)


if __name__ == '__main__':
    app.run(debug = True, port = 2000)