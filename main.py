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

opt_if_mp_bgp_attr = ["self_ll_ipv4", "peer_ll_ipv4"]

def conv():
    names = csv[0]
    objs = []
    for i, row in enumerate(csv[2:]): # skip attribute names and default values
        obj = {}
        for i2, name, in enumerate(names):
            obj[name] = row[i2]

        for k in obj.keys():
            if not obj[k] and obj["mp_bgp"] != "yes" and (obj[k] not in opt_if_mp_bgp_attr):
                raise AttributeError(f"Attribute '{k}' missing on config nr {i}!")    
            if obj[k] == "no":
                obj[k] = "" # for handlebars 
        objs.append(obj)
    return objs
    
peers = conv()

def clear_folder(path):
    for root, dirs, files in os.walk(path):
        for d in dirs:
            shutil.rmtree(os.path.join(root, d))

def gen(what):
    folder = os.path.join(config_dir, what)
    os.makedirs(folder)
    clear_folder(folder)
    for i, peer in enumerate(peers):
        out = templates[what](peers[i])
        with open(os.path.join(folder, f"dn42peer{i}.conf"), "w") as f:
            f.write(out)


clear_folder(config_dir)

# Wireguard
for k in templates.keys():
    gen(k)
