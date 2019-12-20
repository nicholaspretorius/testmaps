from flask_restplus import Namespace, Resource
from ..utils.logger import log

api = Namespace("hello", description="Hello world sanity check!")


@api.route("/")
class HelloWorld(Resource):
    def get(self):
        log.error("Test")
        return {"status": "success", "hello": "world!"}
