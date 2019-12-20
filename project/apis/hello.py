from flask_restplus import Namespace, Resource

api = Namespace("hello", description="Hello world sanity check!")


@api.route("/")
class HelloWorld(Resource):
    def get(self):
        """Hello world!"""
        return {"status": "success", "hello": "world!"}
