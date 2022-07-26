from os import getenv

import bifrostapi

# Call this once before making any other calls.
bifrostapi.add_URI(getenv('MONGO_CONNECTION'))

run_name = input("Run name: ")
runs = bifrostapi.runs.get_runs(run_name)
run_count = 0

try:
    while True:
        print()
        run = next(runs)
        print(f"Run _id: {run['_id']}")
        print("Samples:")
        for sample in run['samples']:
            print(sample)
        run_count += 1
except StopIteration:
    print(f"Found {run_count} runs.")
