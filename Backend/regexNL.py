# Importing libraries
import time
import exrex
import random
import re
from patternRecognizer import patternRecognition

maxRandomPermutations = 1000
maxRandomCollisions = 5
maxComplexityCharLevel = 20
maxRepeatLimit = 5
debugLevel = 1
complexCharacters = set('*+[,{-')


def checkIfRegexIsValid(regexInput):
    try:
        re.compile(regexInput)
    except re.error:
        return False
    return True


def validComplexity(regexInput):
    complexityLevel = 0
    # countComplexity = exrex.count(regexInput, 20)
    for i in regexInput:
        if i in complexCharacters:
            complexityLevel += 1
    if(debugLevel > 1):
        print(f"Complexity Level: {complexityLevel}")
    if complexityLevel > maxComplexityCharLevel:
        return False
    return True


def parse(regexInput):
    start = time.time()  # Start time for performance analysis
    if(not checkIfRegexIsValid(regexInput)):
        if(debugLevel):
            print("Invalid regex")
        return {"success": False, "message": "Invalid regex"}
    simplifiedRegexInput = simplify(regexInput)
    if(simplifiedRegexInput != regexInput and debugLevel > 1):
        print(f"Simplified regex: {simplifiedRegexInput}")
    regexInput = simplifiedRegexInput
    if (not validComplexity(regexInput)):
        if(debugLevel):
            print("Regex is too complex to process")
        return {"success": False, "message": f"This regex has too many complex characters ({complexCharacters})"}
    allPermutations = getRandomPermutations(regexInput)
    patterns = patternRecognition(allPermutations, regexInput)
    end = time.time()  # End time for performance analysis
    if(debugLevel):
        print(patterns)
        if (debugLevel > 2):
            print("\nAll permutations:")
            print(allPermutations)
            print(f"Size: {allPermutations}")
        print("Time taken: " +
              str(end - start))  # For logging
    return {
        "success": True,
        "patterns": patterns,
        "permutations": list(allPermutations),
        "processed": regexInput,
        "time": end - start
    }


def getRandomPermutations(regexInput):
    outputSet = set()
    collision = 0
    while(len(outputSet) < maxRandomPermutations and collision < maxRandomCollisions):
        randomPermutation = exrex.getone(regexInput, maxRepeatLimit)
        if(randomPermutation in outputSet):
            collision += 1
        else:
            outputSet.add(randomPermutation)
            collision = 0
    return outputSet


def simplifyOnce(inputRegex):
    new = re.sub(r'(.*)\*\1\*', r'\g<1>*', inputRegex)
    new = re.sub(r'(.*)\+\1\*', r'\g<1>+', new)
    new = re.sub(r'(.*)\*\1\+', r'\g<1>+', new)
    return(new)


def simplify(inputRegex):
    new = inputRegex
    while(new != simplifyOnce(new)):
        new = simplifyOnce(new)
    return new
