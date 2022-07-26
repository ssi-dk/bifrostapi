import bifrostapi

# Call this once before making any other calls.
bifrostapi.add_URI("mongodb://localhost:27017/bifrost_prod")

run_name = input("Run name: ")
print(bifrostapi.runs.check_run_name(run_name))