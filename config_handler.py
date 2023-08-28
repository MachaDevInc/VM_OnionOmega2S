import json


def save_config(data):
    with open('/root/credentials/config.json', 'w') as outfile:
        json.dump(data, outfile)


def load_config():
    with open('/root/credentials/config.json', 'r') as infile:
        data = json.load(infile)
    return data


def save_Terminal_config(data):
    with open('/root/terminal-config/config.json', 'w') as outfile:
        json.dump(data, outfile)


def load_Terminal_config():
    with open('/root/terminal-config/config.json', 'r') as infile:
        data = json.load(infile)
    return data


def save_VM_config(data):
    with open('/root/vm-config/config.json', 'w') as outfile:
        json.dump(data, outfile)


def load_VM_config():
    with open('/root/vm-config/config.json', 'r') as infile:
        data = json.load(infile)
    return data
