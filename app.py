from flask import Flask, request
from flask_restful import Resource, Api
from flask_httpauth import HTTPBasicAuth
from models import People, Activities, Users

auth = HTTPBasicAuth()
app = Flask(__name__)
api = Api(app)


@auth.verify_password
def verify(login, password):
    if not (login, password):
        return False
    return Users.query.filter_by(login=login, password=password).first()


class Person(Resource):
    @auth.login_required
    def get(self, name):
        person = People.query.filter_by(name=name).first()
        try:
            response = {
                "name": person.name,
                "age": person.age,
                "id": person.id
            }
        except AttributeError:
            response = {"status": "404", "message": "Not found"}
        return response

    @auth.login_required
    def put(self, name):
        person = People.query.filter_by(name=name).first()
        info = request.json
        if "name" in info:
            person.name = info["name"]
        if "age" in info:
            person.age = info["age"]
        person.save()
        response = {
            "id": person.id,
            "name": person.name,
            "age": person.age
        }
        return response

    @auth.login_required
    def delete(self, name):
        person = People.query.filter_by(name=name).first()
        try:
            person.delete()
            response = {"status": 200, "message": "{} deleted successfully".format(person.name)}
        except AttributeError:
            response = {"status": "404", "message": "Not found"}
        return response


class ListPeople(Resource):
    @auth.login_required
    def get(self):
        people = People.query.all()
        response = [
            {
                "id": person.id,
                "name": person.name,
                "age": person.age
            } for person in people
        ]
        return response

    @auth.login_required
    def post(self):
        info = request.json
        person = People(name=info["name"], age=info["age"])
        person.save()
        response = {
            "id": person.id,
            "name": person.name,
            "age": person.age
        }
        return response


class ListActivities(Resource):
    @auth.login_required
    def get(self):
        activities = Activities.query.all()
        response = [
            {
                "id": activity.id,
                "name": activity.person.name,
                "event": activity.name
            } for activity in activities
        ]
        return response

    @auth.login_required
    def post(self):
        info = request.json
        person = People.query.filter_by(name=info["person"]).first()
        activity = Activities(name=info["event"], person=person)
        activity.save()
        response = {
            "id": activity.id,
            "person": activity.person.name,
            "event": activity.name
        }
        return response


api.add_resource(Person, "/person/<string:name>/")
api.add_resource(ListPeople, "/person/")
api.add_resource(ListActivities, "/activities/")


if __name__ == '__main__':
    app.run(debug=True)
