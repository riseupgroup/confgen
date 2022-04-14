from fileinput import filename
from pybars import Compiler

import csv
import gspread

import os
import shutil

from dotenv import load_dotenv
load_dotenv()

## gspread
gc = gspread.service_account(filename='credentials.json')
docid = os.environ["doc_id"]

spreadsheet = gc.open_by_key(docid)
sheet = spreadsheet.worksheet(os.environ["sheet"])
csv = sheet.get_all_values()

## pybars

compiler = Compiler()

template_dir = "./templates"
templates = {}
for root, dirs, files in os.walk(template_dir):
    for filename in files:
        try:
            with open(os.path.join(template_dir, filename), "r") as f:
                name = ".".join(filename.split(".")[:-1]) # without .hbs
                templates[name] = f.read()
        except IOError:
            raise IOError(f"Error reading {filename} . Is the file missing?")

# map every entry to the compiled version
templates = { k: compiler.compile(v) for k, v in templates.items()} 
 

config_dir = "./configs"


## main

def conv():
    names = csv[0]
    objs = []
    for i, row in enumerate(csv[1:]):
        obj = {}
        for i2, name, in enumerate(names):
            if not row[i2] and name != "peer_ipv4":
                raise AttributeError(f"Attribute '{name}' missing on config nr {i}!")     
            obj[name] = row[i2]
        objs.append(obj)
    return objs
    
peers = conv()

def clear_folder(path):
    for root, dirs, files in os.walk(path):
        for f in files:
            os.unlink(os.path.join(root, f))
        for d in dirs:
            shutil.rmtree(os.path.join(root, d))

def gen(what = "wg"):
    folder = os.path.join(config_dir, what)
    os.makedirs(folder)
    for i, peer in enumerate(peers):
        out = templates[what](peers[i])
        with open(os.path.join(folder, f"dn42peer{i}.conf"), "w") as f:
            f.write(out)


clear_folder(config_dir)

# Wireguard
for k in templates.keys():
    gen(k)
