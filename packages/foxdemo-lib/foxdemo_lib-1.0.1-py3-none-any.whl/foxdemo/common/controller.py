from flask_restful import Resource


class ApiController(Resource):

    path = "/"
    registry = set()

    @classmethod
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls.registry.add(cls)

