#!/usr/bin/python
import os
import argparse
import shutil
from pathlib import Path

templates_folder = f"{os.path.dirname(os.path.realpath(__file__))}/templates"

def newProject(path):
    print(f"Creating new project at: {path}")
    os.mkdir(path)
    os.mkdir(f"{path}/src")

    with open(f"{templates_folder}/main-template.c", "r") as templateFile, open(f"{path}/src/main.c", "w+") as outFile:
        for line in templateFile:
            outFile.write(line)
    
    with open(f"{templates_folder}/makefile-template", "r") as templateFile, open(f"{path}/Makefile", "w+") as outFile:
        for line in templateFile:
            outFile.write(line)

    shutil.copyfile(f"{templates_folder}/gitignore-template",f"{path}/.gitignore")
    

def updateProject(path):
    filestr = ""
    code_files = []

    # traverse root directory, and list directories as dirs and files as files
    for root, dirs, files in os.walk(f"{path}/src"):
        for file in files:
            if(Path(file).suffix == ".c"):
                code_files.append(f"{os.path.relpath(root,path)}/{file}")

    with open(f"{path}/Makefile","r") as makefile:
        filestr = makefile.readlines()

    with open(f"{path}/Makefile", "w") as makefile:
        for line in filestr:
            if line.startswith("\t$(CC)"):
                line = "\t" + line.strip() + " " + " ".join(filter(lambda file: file not in line, code_files))
                line = line + '\n'
            makefile.write(line)

def addSource(path, filename):
    os.makedirs(os.path.dirname(f"{path}/src/{filename}"), exist_ok=True)
    safeFileName = filename.replace("/","_")
    with open(f"{templates_folder}/source-template.c", "r") as templateFile, open(f"{path}/src/{filename}.c", "w+") as outFile:
        for line in templateFile:
            line = line.replace("header-template.h",f"{os.path.basename(filename)}.h")
            outFile.write(line)
            
    
    with open(f"{templates_folder}/header-template.h", "r") as templateFile, open(f"{path}/src/{filename}.h", "w+") as outFile:
        for line in templateFile:
            line = line.replace("HEADER_TEMPLATE",f"{safeFileName.upper()}")
            outFile.write(line)
    updateProject(path)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("location",nargs="?", default=".")
    parser.add_argument("--new", action="store_true")
    parser.add_argument("--add", metavar="filename")

    args = parser.parse_args()

    pathStr = args.location
    workingPath = Path(os.path.realpath(pathStr))

    if (args.new):  
        if(os.path.isdir(workingPath)):
            print("Please select a non-existing folder to create a project in")
        else:      
            newProject(workingPath)
    if (os.path.isdir(workingPath)):
        if (args.add):
            addSource(workingPath, args.add)
        else:
            updateProject(workingPath)
    else:
        print("Project folder not found.")
    


if __name__ == "__main__":
    main()