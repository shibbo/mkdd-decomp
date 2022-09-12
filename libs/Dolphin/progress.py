import csv, glob, math, os, sys
from pathlib import Path

libraries = { }

def truncate(number, digits) -> float:
    stepper = 10.0 ** digits
    return math.trunc(stepper * number) / stepper

def generateFullProgJSON(label, percent, color):
    json = []
    json.append("{\n")
    json.append("\t\"schemaVersion\": 1,\n")
    json.append(f"\t\"label\": \"{label}\",\n")
    json.append(f"\t\"message\": \"{percent}%\",\n")
    json.append(f"\t\"color\": \"{color}\"\n")
    json.append("}")

    with open(f"data/{label}.json", "w") as w:
        w.writelines(json)

class Function:
    name = ""
    isCompleted = False
    funcSize = 0

    def __init__(self, name, isComplete, funcSize):
        self.name = name
        self.isCompleted = isComplete
        self.funcSize = funcSize

class Object:
    name = ""
    functions = []
    totalFunctions = 0
    totalCompletedFunctions = 0

    def __init__(self, name):
        self.name = name
        self.functions = list()
        self.totalFunctions = 0
        self.totalCompletedFunctions = 0

    def addFunction(self, function):
        self.functions.append(function)

        if function.isCompleted:
            self.totalCompletedFunctions += 1
        
        self.totalFunctions += 1

    def getFunctions(self):
        return self.functions

    def calculateProgress(self):
        fullSize = 0
        doneSize = 0
        for function in self.functions:
            fullSize += function.funcSize
            
            if function.isCompleted:
                doneSize += function.funcSize

        return doneSize, fullSize

class Library:
    name = ""
    objects = []

    def __init__(self, name):
        self.name = name
        self.objects = list()

    def addObject(self, object):
        self.objects.append(object)

    def addFunctionToObject(self, obj, function):
        if self.containsObject(obj.name):
            self.findObject(obj.name).addFunction(function)
        else:
            self.addObject(obj)
            self.addFunctionToObject(obj, function)

    def findObject(self, objectName):
        for obj in self.objects:
            if obj.name == objectName:
                return obj

        return None

    def getObjects(self):
        return self.objects
    
    def containsObject(self, object):
        for obj in self.objects:
            if obj.name == object:
                return True

        return False

    def calculateProgress(self):
        fullSize = 0
        doneSize = 0

        for obj in self.objects:
            d, f = obj.calculateProgress()
            fullSize += f
            doneSize += d
        
        return doneSize, fullSize

    def getName(self):
        return self.name

    def generateJSONTag(self, percent, color):
        json = []
        json.append("{\n")
        json.append("\t\"schemaVersion\": 1,\n")
        json.append(f"\t\"label\": \"{self.name}\",\n")
        json.append(f"\t\"message\": \"{truncate(percent, 3)}%\",\n")
        json.append(f"\t\"color\": \"{color}\"\n")
        json.append("}")

        with open(f"data/json/{self.name}.json", "w") as w:
            w.writelines(json)

    def generateMarkdown(self):
        # first we are going to generate the tables for the object files themselves in the library
        page = []
        page.append(f"# {self.name}\n")
        page.append("| Symbol | Meaning \n")
        page.append("| ------------- | ------------- \n")
        page.append("| :x: | Object has not yet been started. \n")
        page.append("| :eight_pointed_black_star: | Object is in progress. \n")
        page.append("| :white_check_mark: | Object is completed. \n")
        page.append("\n\n")
        page.append("| Object | Percentage (of Bytes) | Functions Done / Total Functions | Percentage (Functions) | Status \n")
        page.append("| ------------- | ------------- | ------------- | ------------- | ------------- \n")

        for obj in self.objects:
            d, f = obj.calculateProgress()
            prog = (d / f) * 100.0
            funcProg = (obj.totalCompletedFunctions / obj.totalFunctions) * 100.0

            marker = ":x:"

            if d == f:
                marker = ":white_check_mark:"
            elif d != f and d != 0:
                marker = ":eight_pointed_black_star:"

            page.append(f"| {obj.name} | {prog}% | {obj.totalCompletedFunctions} / {obj.totalFunctions} | {funcProg}% | {marker} \n")

        page.append("\n\n")

        # now we can do it per object in the library
        for obj in self.objects:
            page.append(f"# {obj.name}\n")
            page.append("| Symbol | Decompiled? |\n")
            page.append("| ------------- | ------------- |\n")

            for func in obj.getFunctions():
                marker = ":x:"

                if func.isCompleted:
                    marker = ":white_check_mark:"

                funcName = func.name.replace("<", "&lt;")
                funcName = funcName.replace(">", "&gt;")

                page.append(f"| {funcName} | {marker} |\n")

            page.append("\n\n")

        with open(f"docs/lib/{self.name}.md", "w") as w:
            w.writelines(page)

game_libs = [
    "Dolphin.a",
]

func_sizes = {}

# start by reading function sizes
with open("../../data/funcSizes.txt", "r") as file:
    lines = file.readlines()

    for line in lines:
        spl = line.split('=')
        sym = spl[0]
        func_sizes[sym] = spl[1].split('::', 1)[1]

csv_files = glob.glob("csv/*.csv")

for csv_file in sorted(csv_files, key=str.casefold):
    lib_name = Path(csv_file).stem
    lib_arch_name = Path(csv_file).stem + ".a"

    library = Library(lib_name)

    with open(csv_file, "r") as c:
        csv_reader = csv.reader(c)

        for row in csv_reader:
            symbol = row[0]
            symbol = symbol.replace("&#44;", ",")
            if symbol == "Symbol Name":
                continue

            obj = row[1]
            lib = row[2]
            done = row[3] == "true"

            funcSize = int(func_sizes[symbol].strip("\n"))
            func = Function(symbol, done, funcSize)

            obj = Object(obj)
            library.addFunctionToObject(obj, func)

    libraries[lib_name] = library

full_sdk_size = 0
done_sdk_size = 0


print("Calculating percentages...")

for key in libraries:
    lib = libraries[key]
    d, f = lib.calculateProgress()

    libName = f"{lib.getName()}.a"

    if libName in game_libs:
        full_sdk_size += f
        done_sdk_size += d

progPercent_sdk = (done_sdk_size / full_sdk_size ) * 100.0

print(f"Progress: {progPercent_sdk}% [{done_sdk_size} / {full_sdk_size}] bytes")
print("Generating JSON...")

generateFullProgJSON("Dolphin", progPercent_sdk, "blue")

print("Generating markdown pages...")

# now we generate our progress page
progressPage = []
progressPage.append("| Library | Percentage |\n")
progressPage.append("| ------------- | ------------- |\n")

for key in libraries:
    lib = libraries[key]
    d, f = lib.calculateProgress()
    libprog = (d / f) * 100.0
    progressPage.append(f"| [{key}](https://github.com/shibbo/mkdd-decomp/blob/main/libs/Dolphin/docs/lib/{key}.md) | {libprog}% |\n")

with open("docs/PROGRESS.md", "w") as w:
    w.writelines(progressPage)

# now we write the progress page for each library
for key in libraries:
    lib = libraries[key]
    lib.generateMarkdown()

print("Done.")
