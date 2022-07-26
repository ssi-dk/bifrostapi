from os import getenv
from sys import exit
import argparse

import bifrostapi

# Call this once before making any other calls.
bifrostapi.add_URI(getenv('MONGO_CONNECTION'))

parser = argparse.ArgumentParser(
    description='Interactive script for removing a run and related objects from MongoDB')
parser.add_argument('run_id', type=str, help='The MongoDB _id field of the run object')
args = parser.parse_args()

run = bifrostapi.runs.get_run_by_id(args.run_id)
print(f"Preparing to remove a run document with name {run['name']} and related documents.")
print("The run document refers these samples (name consistency is being checked):")
print("Object id, name")
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

print("OK to delete these samples from the samples collection. OK? (y/n)")
answer = input()
if answer not in ['y', 'Y']:
    print("No changes were made to the database.")
    exit()
else:
    print("Deleting sample documents...")
    for run_sample in run['samples']:
        print(run_sample['_id'])
        bifrostapi.samples.delete_sample_by_id(run_sample['_id'])