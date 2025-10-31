from json import load, dump
def read(file_name):
    with open(f"JSONs/{file_name}", "r") as f:
        data  = load(f)
    return data

def save(file_name, data):
    with open(f"JSONs/{file_name}", "w") as f:
        dump(data, f, indent = "\t")

def reset_vals(file_name):
    data1 = read(file_name)

    def to_zero(data):
        if isinstance(data, dict):
            return {k: to_zero(v) for k, v in data.items()}
        elif isinstance(data, list):
            return [to_zero(element) for element in data]
        elif isinstance(data, int) or (isinstance(data, str) and data == ""):
            return 0
        else:
            return data
        
    data2 = to_zero(data1)

    save(file_name, data2)

def toggle_bool(file_name, key_list):
    data = read(file_name)
    keys = key_list.split(",")

    cur = data
    for key in keys[:-1]:
        cur = cur[key]
        

    last_key = keys[-1]
    cur[last_key] = not cur[last_key]

    save(file_name, data)

def set_json_val(file_name, key_map, new_val, widget):
    if new_val == "":
        new_val = 0
    data = read(file_name)
    if isinstance(widget, str):
        key_list = key_map[widget]
    else:
        key_list = key_map[str(widget).split(".")[-1]]

    if callable(key_list):
        key_list = key_list()

    keys = key_list.split(",")

    cur = data
    for key in keys[:-1]:
        cur = cur[key]
    last_key = keys[-1]
    cur[last_key] = new_val

    save(file_name, data)

def get_json_val(file_name, key_map, widget):
    data = read(file_name)
    if isinstance(widget, str):
        key_list = key_map[widget]
    else:
        key_list = key_map[str(widget).split(".")[-1]]

    if callable(key_list):
        key_list = key_list()

    keys = key_list.split(",")


    cur = data
    for key in keys[:-1]:
        cur = cur[key]
    last_key = keys[-1]
    val = cur[last_key]

    return val
