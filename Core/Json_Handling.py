from json import load, dump
def read(file_name):
    with open(f"JSONs/{file_name}", "r") as f:
        data  = load(f)
    return data

def save(file_name, data):
    with open(f"JSONs/{file_name}", "w") as f:
        dump(data, f, indent = "\t")