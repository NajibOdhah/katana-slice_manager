from flask import request
from flask_classful import FlaskView
from katana.utils.mongoUtils import mongoUtils
from katana.utils.policyUtils import neatUtils, test_policyUtils
from bson.json_util import dumps
import logging
import time
import uuid
import pymongo


# Logging Parameters
logger = logging.getLogger(__name__)
file_handler = logging.handlers.RotatingFileHandler(
    'katana.log', maxBytes=10000, backupCount=5)
stream_handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s %(name)s %(levelname)s %(message)s')
stream_formatter = logging.Formatter(
    '%(asctime)s %(name)s %(levelname)s %(message)s')
file_handler.setFormatter(formatter)
stream_handler.setFormatter(stream_formatter)
logger.setLevel(logging.DEBUG)
logger.addHandler(file_handler)
logger.addHandler(stream_handler)


class PolicyView(FlaskView):
    route_prefix = '/api/'
    req_fields = ["id", "url", "type"]

    def index(self):
        """
        Returns a list of policy management system and their details,
        used by: `katana policy ls`
        """
        policy_data = mongoUtils.index("policy")
        return_data = []
        for item in policy_data:
            return_data.append(dict(_id=item['_id'],
                               system_id=item['id'],
                               created_at=item['created_at'],
                               type=item['type']))
        return dumps(return_data)

    def get(self, uuid):
        """
        Returns the details of specific policy management system,
        used by: `katana policy inspect [uuid]`
        """
        data = (mongoUtils.get("policy", uuid))
        if data:
            return dumps(data), 200
        else:
            return "Not Found", 404

    def post(self):
        """
        Add a new policy management system. The request must provide the
         system details. used by: `katana policy add -f [yaml file]`
        """
        # Create the object and store it in the object collection
        try:
            if request.json["type"] == "test-policy":
                policy = test_policyUtils.Policy(id=request.json["id"],
                                                 url=request.json['url'])
            elif request.json["type"] == "neat":
                policy = neatUtils.Policy(id=request.json["id"],
                                          url=request.json['url'])
            else:
                return "Error: Not supported Policy system type", 400
        except KeyError:
            return f"Error: Required fields: {self.req_fields}", 400
        new_uuid = str(uuid.uuid4())
        request.json['_id'] = new_uuid
        request.json['created_at'] = time.time()  # unix epoch
        try:
            new_uuid = mongoUtils.add('policy', request.json)
        except pymongo.errors.DuplicateKeyError:
            return "Policy management system with id {0} already exists".\
                format(request.json["id"]), 400
        return f"Created {new_uuid}", 201

    def delete(self, uuid):
        """
        Delete a specific policy management system.
        used by: `katana policy rm [uuid]`
        """
        del_policy = mongoUtils.delete("policy", uuid)
        if del_pplicy:
            return "Deleted policy management system {}".format(uuid), 200
        else:
            # if uuid is not found, return error
            return "Error: No such policy management system: {}".format(uuid),\
                404

    def put(self, uuid):
        """
        Update the details of a specific policy engine system.
        used by: `katana policy update [uuid] -f [yaml file]`
        """
        data = request.json
        data['_id'] = uuid
        old_data = mongoUtils.get("policy", uuid)

        if old_data:
            data["created_at"] = old_data["created_at"]
            try:
                for entry in self.req_fields:
                    if data[entry] != old_data[entry]:
                        return "Cannot update field: " + entry, 400
            except KeyError:
                return f"Error: Required fields: {self.req_fields}", 400
            else:
                mongoUtils.update("policy", uuid, data)
            return f"Modified {uuid}", 200
        else:
            # Create the object and store it in the object collection
            try:
                if request.json["type"] == "test-policy":
                    policy = test_policyUtils.Policy(id=request.json["id"],
                                                     url=request.json['url'])
                elif request.json["type"] == "neat":
                    policy = neatUtils.Policy(id=request.json["id"],
                                              url=request.json['url'])
                else:
                    return "Error: Not supported Policy system type", 400
            except KeyError:
                return f"Error: Required fields: {self.req_fields}", 400
            new_uuid = str(uuid.uuid4())
            request.json['_id'] = new_uuid
            request.json['created_at'] = time.time()  # unix epoch
            try:
                new_uuid = mongoUtils.add('policy', request.json)
            except pymongo.errors.DuplicateKeyError:
                return "Policy management system with id {0} already exists".\
                    format(request.json["id"]), 400
            return f"Created {new_uuid}", 201