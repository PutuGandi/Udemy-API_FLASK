from flask import Flask, jsonify, request
from flask_restful import Api, Resource 
from pymongo import MongoClient
from flask_bcrypt import Bcrypt

app=Flask(__name__)
api=Api(app)

# db harus sama dengan nama service db di docker-compose.yaml
# port 27017 ialah port default-nya
client = MongoClient("mongodb://db:27017")

# buat database
db = client.SentencesDatabase

# buat collection
users = db["Users"]

# bcrypt
bcrypt = Bcrypt()

def verifyPass(username,password):
    hashing_pw = users.find({
        "Username":username
    })[0]["Password"]

    if bcrypt.check_password_hash(hashing_pw, password):
        return True
    else:
        return False 

def countTokens(username):
    tokens = users.find({
        "Username":username 
    })[0]["Tokens"]
    return tokens

class Register(Resource):
    def post(self):
        # Langkah 1, ambil data dari user
        postedData = request.get_json()

        # ambil data
        username = postedData["Username"]
        password = postedData["Password"]
        
        # hashing pass
        hashing_pass = bcrypt.generate_password_hash(password)

        # store username & password into database
        users.insert({
            "Username" : username,
            "Password" : hashing_pass,
            "Sentence" : "",
            "Tokens" : 10
        })

        json = {
            "status":200,
            "message":"sukes masuk API"
        }

        return jsonify(json)

class Store(Resource):
    def post(self):
        # langkah 1 mendapat podt data
        postedData = request.get_json()

        # langkah 2, baca data
        username = postedData["Username"]
        password = postedData["Password"]
        sentence = postedData["Sentence"]

        # langkah 3, verifikasi username & password 
        correct_pw = verifyPass(username,password)

        if not correct_pw:
            json = {
                "status":302
            }
            return jsonify(json)

        # langkah 4, verifikasi user punya cukup token
        num_tokens = countTokens(username)
        if num_tokens <= 0:
            json = {
                "status":301
            }
            return jsonify(json)

        # langkah 5, store sentence , take on tokern away and return 200ok
        users.update({
            "Username":username
        }, {
            "$set":{
                "Sentence":sentence,
                "Tokens": num_tokens-1
                }
        })

        json = {
            "status":200,
            "msg":"sentence saved succesfully"
        }
        return jsonify(json)

class Get(Resource):
    def get(self):
        postedData = request.get_json()

        username = postedData["Username"]
        password = postedData["Password"]

        # verifikasi username & passs yang match
        correct_pw = verifyPass(username,password)

        if not correct_pw:
            json = {
                "status":302
            }
            return jsonify(json)

        num_tokens = countTokens(username)
        if num_tokens <= 0:
            json = {
                "status":301
            }
            return jsonify(json)

        # make user PAY!! dengan mengurangi token
        users.update({
            "Username":username
        }, {
            "$set":{
                "Tokens":num_tokens-1
            }
        })

        sentence = users.find({
            "Username": username
        })[0]["Sentence"]

        json = {
            "status":200,
            "sentence":sentence
        }

        return jsonify(json)

api.add_resource(Register,'/register')
api.add_resource(Store,'/store')
api.add_resource(Get,'/get')

if __name__ == "__main__":
    app.run(host='0.0.0.0')