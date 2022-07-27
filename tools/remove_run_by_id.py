from os import getenv
from sys import exit
import argparse

import bifrostapi
from bifrostapi import sample_components

# Call this once before making any other calls.
bifrostapi.add_URI(getenv('MONGO_CONNECTION'))

parser = argparse.ArgumentParser(
    description='Interactive script for removing a run and related objects from MongoDB')
parser.add_argument('run_id', type=str, help='The MongoDB _id field of the run object')
args = parser.parse_args()

run = bifrostapi.runs.get_run_by_id(args.run_id)
if run is None:
    print(f"ERROR: no run exists with id {args.run_id}")
    exit(1)
print(f"Preparing to remove a run document with name {run['name']} and related documents.")

# Sample documents
for run_sample in run['samples']:
    sample = bifrostapi.samples.get_sample_by_id(run_sample['_id'])
    if sample is None:
        print(f"ERROR: a sample that was referenced in run did not exist in samples collection:")
        print(run_sample)
        exit(2)
    if run_sample['name'] != sample['name']:
        print(f"ERROR: name consistency check failed for sample id {run_sample['_id']}.")
        print(f"Run sample name is {run_sample['name']}")
        print(f"Sample name is {sample['name']}")
        exit(3)
    else:
        component_names = [component['name'] for component in sample['components']]
        print(sample['name'], component_names)
    # Sample component documents
    sample_components = list(bifrostapi.sample_components.find_sample_component_ids_by_sample_id(sample['_id']))
    sample_component_object_ids = [sc['_id'] for sc in sample_components]
    for oid in sample_component_object_ids:
        bifrostapi.sample_components.delete_sample_component_by_id(oid)
    print(f"Deleted {len(sample_components)} documents from sample_components collection")

print("Deleting sample documents...")
for run_sample in run['samples']:
    print(run_sample['_id'])
    bifrostapi.samples.delete_sample_by_id(run_sample['_id'])

# Run document
print("Deleting run document")
bifrostapi.runs.delete_run_by_id(run['_id'])