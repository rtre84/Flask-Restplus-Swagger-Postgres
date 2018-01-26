
from models import Todo
from db import session

# from flask.ext.restful import reqparse
# from flask.ext.restful import abort
# from flask.ext.restful import Resource
# from flask.ext.restful import fields
# from flask.ext.restful import marshal_with

from flask_restplus import reqparse
from flask_restplus import abort
from flask_restplus import Resource
from flask_restplus import fields
from flask_restplus import marshal_with

todo_fields = {
    'id': fields.Integer,
    'task': fields.String,
    'uri': fields.Url('todo', absolute=True),
}

parser = reqparse.RequestParser()
parser.add_argument('task', type=str)

class TodoResource(Resource):
    @marshal_with(todo_fields)
    def get(self, id):
        todo = session.query(Todo).filter(Todo.id == id).first()
        if not todo:
            abort(404, message="Todo {} doesn't exist".format(id))
        return todo

    def delete(self, id):
        todo = session.query(Todo).filter(Todo.id == id).first()
        if not todo:
            abort(404, message="Todo {} doesn't exist".format(id))
        session.delete(todo)
        session.commit()
        return {}, 204

    @marshal_with(todo_fields)
    def put(self, id):
        parsed_args = parser.parse_args()
        todo = session.query(Todo).filter(Todo.id == id).first()
        todo.task = parsed_args['task']
        session.add(todo)
        session.commit()
        return todo, 201


class TodoListResource(Resource):
    @marshal_with(todo_fields)
    def get(self):
        todos = session.query(Todo).all()
        return todos

    # Testing the below method using curl
    # curl - X POST - -header 'Accept: application/json' 'http://localhost:5000/todos' - d "task='Write Unit Tests'"
    # OR
    # curl -X POST --header 'Content-Type: application/json' --header 'Accept: application/json' 'http://localhost:5000/todos' -d '{"task":"Testing via curl"}'
    #
    # TODO: Add Swagger Documentation for task so test from swagger ui shows a valid request
    @marshal_with(todo_fields)
    def post(self):
        parsed_args = parser.parse_args()
        todo = Todo(task=parsed_args['task'])
        session.add(todo)
        session.commit()
        return todo, 201
