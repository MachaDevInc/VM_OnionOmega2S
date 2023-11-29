import json


def save_config(data):
    with open('/VM/credentials/config.json', 'w') as outfile:
        json.dump(data, outfile)


def load_config():
    with open('/VM/credentials/config.json', 'r') as infile:
        data = json.load(infile)
    return data


def save_Terminal_config(data):
    with open('/VM/terminal-config/config.json', 'w') as outfile:
        json.dump(data, outfile)


def load_Terminal_config():
    with open('/VM/terminal-config/config.json', 'r') as infile:
        data = json.load(infile)
    return data


def save_VM_config(data):
    with open('/VM/vm-config/config.json', 'w') as outfile:
        json.dump(data, outfile)


def load_VM_config():
    with open('/VM/vm-config/config.json', 'r') as infile:
        data = json.load(infile)
    return data
