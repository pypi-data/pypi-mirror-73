import inspect
import logging

from flask import Flask
from flask_restful import Api

from controller import ApiController


def initialize_app():
    app = Flask(__name__)
    api = Api(app)

    for controller_class in ApiController.registry:
        logging.info("Adding controller '{controller}'".format(controller=controller_class.__name__))
        paths = [controller_class.path]
        if "id" in inspect.signature(controller_class.get).parameters.keys():
            paths.append("{base_path}/<id>".format(base_path=controller_class.path))
        api.add_resource(controller_class, *paths)

    return app