import json

from mongoengine import Document


class DictMixin(object):

    def to_dict(self):
        return json.loads(self.to_json())


class BaseDocument(Document, DictMixin):
    meta = {"abstract": True}

