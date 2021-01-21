from flask import Flask, jsonify, request
from flask_restful import Api, Resource 

app=Flask(__name__)
api=Api(app)

def checkstatus(postedData, funcName):
    if funcName == "add" or funcName == "multiply" or funcName == "substract":
        if "x" not in postedData or "y" not in postedData:
            return 301
        else:
            return 200
    elif funcName == "division":
        if "x" not in postedData or "y" not in postedData:
            return 301
        elif postedData["x"] == 0 or postedData["y"]==0:
            return 302
        else:
            return 200
class Add(Resource):
    def post(self):
        postedData = request.get_json()
        statusCode = checkstatus(postedData, "add")
        if statusCode != 200:
            retJs = {
                "Hasil":"Error",
                "Status":statusCode
            }
            return jsonify(retJs)
        x = postedData["x"]
        y = postedData["y"]
        x = int(x)
        y = int(y)
        z = x + y
        js = {
            "Hasil":z,
            "Status Code":200
        }
        return jsonify(js)

class Substract(Resource):
    def post(self):
        postedData = request.get_json()
        statusCode = checkstatus(postedData, "substract")
        if statusCode != 200:
            retJs = {
                "Hasil":"Error",
                "Status":statusCode
            }
            return jsonify(retJs)
        x = postedData["x"]
        y = postedData["y"]
        x = int(x)
        y = int(y)
        z = x - y
        js = {
            "Hasil":z,
            "Status Code":200
        }
        return jsonify(js)

class Division(Resource):
    def post(self):
        postedData = request.get_json()
        statusCode = checkstatus(postedData, "division")
        if statusCode != 200:
            retJs = {
                "Hasil":"Error",
                "Status":statusCode
            }
            return jsonify(retJs)
        x = postedData["x"]
        y = postedData["y"]
        x = int(x)
        y = int(y)
        z = x / y
        js = {
            "Hasil":z,
            "Status Code":200
        }
        return jsonify(js)

class Multiply(Resource):
    def post(self):
        postedData = request.get_json()
        statusCode = checkstatus(postedData, "multiply")
        if statusCode != 200:
            retJs = {
                "Hasil":"Error",
                "Status":statusCode
            }
            return jsonify(retJs)
        x = postedData["x"]
        y = postedData["y"]
        x = int(x)
        y = int(y)
        z = x * y
        js = {
            "Hasil":z,
            "Status Code":200
        }
        return jsonify(js)

api.add_resource(Add,'/add')
api.add_resource(Multiply,'/multiply')
api.add_resource(Substract,'/substract')
api.add_resource(Division,'/division')

@app.route('/')
def awal():
    return "Hai"

if __name__ == "__main__":
    app.run(host='0.0.0.0')