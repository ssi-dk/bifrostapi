from os import getenv
import bifrostapi

# Call this once before making any other calls.
bifrostapi.add_URI(getenv('MONGO_CONNECTION'))

run_id = input("Run id: ")
run = bifrostapi.runs.get_run_by_id(run_id)
print(f"Preparing to remove run with name {run['name']}...")