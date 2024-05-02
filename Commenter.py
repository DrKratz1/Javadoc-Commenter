import os
import csv

directory = os.path.dirname(os.path.realpath(__file__))
directory += "\\"

setting = input("to find and write parameters type 1, to comment, type 2\nDO NOTE THAT IF YOU PRESS 1, CHANGES YOU HAVE MADE TO THE CSV FILES WILL BE OVERWRITTEN\n")


if setting == "1":
    write = True
elif setting  == "2":
    write = False
else:
    print("Invalid input")
    exit()

if (write):
    enda = {}

    for filename in os.listdir(directory):
        enda[filename] = {}
        if filename.endswith(".java"):
            # exclude IOUtils.java
            if filename == "IOUtils.java":
                continue
            
            f = open(filename, "r")
            for i, line in enumerate(f):
                # strip tabs from start of line
                line = line.lstrip()
                line = line.rstrip()
                functionName = ""

                if line.startswith("public") or line.startswith("private") or line.startswith("protected") or line.startswith("default"):
                    # remove " {" or ";" from the end of the line
                    if line.endswith("{"):
                        line = line[:-2]
                    elif "abstract" in  line and line.endswith(";"):
                        line = line[:-1]
                    else:
                        continue

                    # find index of first "("
                    bracketIndex = line.find("(")
                    line = line[:bracketIndex + 1] + " " + line[bracketIndex + 1:]

                    # found a class, not a function
                    if (bracketIndex == -1):
                        continue

                    # single out word before "(" in line
                    line = line.split()

                    start = False

                    currentParameters = []
                    functionName = ""
                    returnType = ""

                    # process line
                    for i, word in enumerate(line):

                        if start:
                            # getting parameters
                            word = word.strip(",")

                            if ")" in word:
                                word = word.split(")")
                                currentParameters.append(word[0])
                                start = False
                            else:
                                currentParameters.append(word)

                        # return types
                        if i < len(line) - 1 and  "(" in line[i + 1]:
                            returnType = word

                        # excluding constructor
                        if "(" in word and word != line[1]:
                            word = word.split("(")
                            if word[0][-1] == ">":
                                continue
                            functionName = word[0]
                            
                            # exclude main
                            if functionName == "main":
                                continue
                            
                            start = True
                
                    if len(currentParameters) == 1:
                        pass
                    else:
                        toRemove = []
                        # combine parameters with their types
                        for i, parameter in enumerate(currentParameters):
                            if i % 2 != 0:
                                currentParameters[i - 1] += " "  + parameter
                                toRemove.append(parameter)
                        
                        for remove in toRemove:
                            currentParameters.remove(remove)
                        toRemove = []
                    
                    if functionName != "":
                        # print(filename, returnType, functionName, str(currentParameters), " ".join(line))
                        enda[filename][functionName] = [returnType, currentParameters]
            f.close()
    
    # getting a set of all the parameters
    parameters = set()
    for item in enda:
        for function in enda[item]:
            for parameter in enda[item][function][1]:
                if (parameter != ""): parameters.add(parameter)
                
    functionNames = {item: {} for item in enda}
    for item in enda:
        for function in enda[item]:
                if "set" in function:
                    functionNames[item][function] = [enda[item][function][0], "Sets the value of " + function[3:].lower(), enda[item][function][1], ""]
                elif "get" in function:
                    functionNames[item][function] = [enda[item][function][0], "Returns the value of " + function[3:].lower(), enda[item][function][1], ": value of " + function[3:].lower()]
                else:
                    functionNames[item][function] = [enda[item][function][0], "", enda[item][function][1], ""]


    # writing parameters to a csv file
    paramFields = ["Parameter", "Explanation"]
    functionFields = ["File", "Function", "ReturnType", "Explanation", "Parameters", "ReturnExplanation"]
    

    parameterSorted = sorted(list(parameters))
    parameterData = [{"Parameter": parameter, "Explanation": ""} for parameter in parameterSorted]

    parameterFilename = "parameters.csv"
    functionFilename = "functions.csv"

    # check if both files already exist
    if os.path.exists(parameterFilename) and os.path.exists(functionFilename):
        # go through each file and copy existing data into new data
        with open(parameterFilename, "r") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                for parameter in parameterData:
                    if parameter["Parameter"] == row["Parameter"]:
                        parameter["Explanation"] = row["Explanation"]
        csvfile.close()
        
        with open(functionFilename, "r") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row["File"] in functionNames:
                    functionNames[row["File"]][row["Function"]] = [row["ReturnType"], row["Explanation"], row["Parameters"].split("|"), row["ReturnExplanation"]]
        csvfile.close()
        
    
    # writing out to parameters and functions files
    with open(parameterFilename, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=paramFields)
        writer.writeheader()
        writer.writerows(parameterData)

    csvfile.close()

    with open(functionFilename, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=functionFields)
        writer.writeheader()
        for item in functionNames:
            for function in functionNames[item]:
                writer.writerow({"File": item, "Function": function, "ReturnType": functionNames[item][function][0], "Explanation": functionNames[item][function][1], "Parameters": "|".join(functionNames[item][function][2]), "ReturnExplanation": functionNames[item][function][3]})
    
    csvfile.close()

    print("finished writing")
    
elif not write:
    # reading parameters from csv file
    parameters = {}
    with open("parameters.csv", "r") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            parameters[row["Parameter"]] = row["Explanation"]
    csvfile.close()
    
    # reading functions from csv file
    functions = {}
    with open("functions.csv", "r") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row["File"] not in functions:
                functions[row["File"]] = {}
            functions[row["File"]][row["Function"]] = [row["ReturnType"], row["Explanation"], row["Parameters"], row["ReturnExplanation"]]
    csvfile.close()
    
    start = "    /***"
    middle = "     * "
    end = "     */"
    
    
    for item in functions:
        outFile = item[:-5] + "_commented.txt"
        with open(outFile, "w") as output:
            # find where the functions are
            with open(item, "r") as file:
                for line in file:
                    originalLine = line
                    fail = False
                    line = line.lstrip().rstrip()
                    if line.startswith("public") or line.startswith("private") or line.startswith("protected") or line.startswith("default"):
                        if line.endswith("{") or line.endswith(";"):
                            line = line[:-2]
                        elif "abstract" in  line and line.endswith(";"):
                            line = line[:-1]
                        else:
                            fail = True

                        bracketIndex = line.find("(")
                        line = line[:bracketIndex + 1] + " " + line[bracketIndex + 1:]
                        if (bracketIndex == -1):
                            fail = True
                        line = line.split()
                        
                        functionName = ""
                        
                        for i, word in enumerate(line):
                            if "(" in word and word != line[1]:
                                word = word.split("(")
                                if word[0][-1] == ">":
                                    fail = True
                                functionName = word[0]
                        
                        if functionName in functions[item] and not fail:
                            functionParams = functions[item][functionName][2].split("|")
                            output.write(start + "\n")
                            #explanation
                            output.write(middle + functions[item][functionName][1] + "\n")
                            for i, functionParam in enumerate(functionParams):
                                # parameters
                                if (functionParam == ""): continue
                                output.write(middle + "@param " + functionParam + ": " + parameters[functionParam] + "\n")
                            # return type
                            output.write(middle + "@return " + functions[item][functionName][0] + ": " + functions[item][functionName][3] + "\n")
                            output.write(end + "\n")
                            output.write(originalLine)
                    elif line.startswith(start.lstrip()) or line.startswith(middle.lstrip().rstrip()) or line.startswith(end.lstrip()):
                        # skip if it is a javadoc comment
                        continue
                    else:
                        # write line anyways lol
                        fail = True
                    if fail:
                        output.write(originalLine)
            output.write("\n\n")
    print("finished commenting go check the files")