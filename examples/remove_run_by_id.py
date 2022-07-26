from os import getenv
from sys import exit
import bifrostapi

# Call this once before making any other calls.
bifrostapi.add_URI(getenv('MONGO_CONNECTION'))

run_id = input("Run id: ")
run = bifrostapi.runs.get_run_by_id(run_id)
print(f"Preparing to remove run with name {run['name']}...")
print("The run document refers these samples (name consistency is being checked):")
for run_sample in run['samples']:
    sample = bifrostapi.samples.get_sample_by_id(run_sample['_id'])
    if sample is None:
        print(f"ERROR: a sample that was referenced in run did not exist in samples collection:")
        print(run_sample)
        exit(1)
    if run_sample['name'] != sample['name']:
        print(f"ERROR: name consistency check failed for sample id {run_sample['_id']}.")
        print(f"Run sample name is {run_sample['name']}")
        print(f"Sample name is {sample['name']}")
        exit(2)
    else:
        print(run_sample['_id'], run_sample['name'])
    