"""
    utils.py
    ~~~~~~~~

    Common classes/functions for other modules.

"""
import json
from bson import ObjectId
import datetime

class MongoJSONEncoder(json.JSONEncoder):
    """Extend JSONEncoder to cover MongoDB field types"""
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        if isinstance(obj, datetime.datetime):
            return str(obj)
        return json.JSONEncoder.default(self, obj)