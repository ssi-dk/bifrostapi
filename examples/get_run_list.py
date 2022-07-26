import bifrostapi

# Call this once before making any other calls.
bifrostapi.add_URI("mongodb://localhost:27017/bifrost_prod")

runs = bifrostapi.runs.get_run_list()
for run in runs:
    print(run['name'])