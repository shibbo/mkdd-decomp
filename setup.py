# setup.py -- by shibboleet

import zipfile
import urllib.request
import os
import sys
import subprocess
import hashlib

def install(what):
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', what])

if not os.path.exists("baserom.dol"):
    print("baserom.dol does not exist. Place a MK:DD dol named baserom.dol in the root.")
    sys.exit(1)
else:
    print("Found baserom.dol...")

with open("baserom.dol", "rb") as input:
    data = input.read()

    hash = hashlib.sha256(data).hexdigest().upper()
    if hash == "A497E0F14E9B1013C0723D951372C9EC563A79570A6D087B47CB463AE77C92CF":
        print("baserom.dol hash verified...")
    else:
        print("baserom.dol hash invalid. Wrong version?")
        sys.exit(1)

try:
    import capstone
    print("Found capstone, continuing...")
except ModuleNotFoundError:
    print("Module 'capstone' not installed. Installing...")
    install("capstone")

try:
    import elftools
    print("Found elftools, continuing...")
except ModuleNotFoundError:
    print("Module `elftools` not found. Installing...")
    install("pyelftools")

try:
    import ninja
    print("Found ninja, continuing...")
except ModuleNotFoundError:
    print("Module 'ninja' not found. Installing...")
    install("ninja")

try:
    import colorama
    print("Found colorama, continuing...")
except ModuleNotFoundError:
    print("Module 'colorama' not found. Installing...")
    install("colorama")

if not os.path.exists("Compilers"):
    print("Compilers folder not found, downloading...")

    with urllib.request.urlopen("http://shibbo.net/smg/Compilers.zip") as response, open("Compilers.zip", 'wb') as out:
        data = response.read()
        out.write(data)

    if os.path.exists("Compilers.zip"):
        os.mkdir("Compilers")
        print("Extracting file...")
        with zipfile.ZipFile("Compilers.zip", "r") as zip:
            zip.extractall("Compilers")

        os.remove("Compilers.zip")
    else:
        print("Compilers.zip failed to download.")
        sys.exit(1)
else:
    print("Found compilers folder, continuing...")

print("Done.")
sys.exit(1)