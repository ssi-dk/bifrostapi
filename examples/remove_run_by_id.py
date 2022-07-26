from os import getenv
from bson.objectid import ObjectId
import bifrostapi

# Call this once before making any other calls.
bifrostapi.add_URI(getenv('MONGO_CONNECTION'))

obj_id = ObjectId(input("Run id: "))
run = bifrostapi.runs.get_run_by_id(obj_id)
print(f"Preparing to remove run with name {run['name']}...")