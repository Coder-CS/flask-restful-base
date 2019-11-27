from flask import Flask
from flask_restful import Api, Resource, reqparse

app = Flask(__name__)
api = Api(app)
parser = reqparse.RequestParser()

class Test(Resource):
    def get(self):
        return {"username": "hhahaha"}

@app.route('/')
def hello_world():
    return 'Hello World!'

api.add_resource(Test, '/test', endpoint='/t')


if __name__ == '__main__':
    app.run(debug=True)
