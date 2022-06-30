# Pattern Recognition Algorithms

import re

# Popularly used email regex
emailRegex = r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+'
# Popular patterns for phone number regexes:
phoneRegexes = {
    1: r"([1-9]{3}-[0-9]{3}-[0-9]{4})",  # 123-345-6789,
    2: r"^\d{10}$",  # 1234567890
    3: r"(\([1-9]{3}\)-[0-9]{3}{30-9]{4})",  # (123)-456-7890,
    4: r"(\([1-9]{3}\)\s[0-9]{3}\s[0-9]{4})",  # (123) 456 7890
    5: r"([1-9]{3}\s[0-9]{3}\s[0-9]{4})"  # 123 456 7890
}


# Get the minimum length possible for a regex from given permutations
def minimumLength(permutations, inputRegex):
    minLen = None
    if(checkPatternMatch("", inputRegex)):
        return 0
    for permutation in permutations:
        if (minLen is None or len(permutation) <= minLen):
            minLen = len(permutation)
    return minLen


# Check preceding characters patterns
def checkPrecedence(permutations):
    patternCount = {}
    end = {}
    result = {}
    for word in permutations:
        i = 0
        if(len(word) > 1):
            end[word[-1]] = True
        while(i < len(word) - 1):
            if(word[i] not in patternCount):
                patternCount[word[i]] = word[i + 1]
            if(patternCount[word[i]] != word[i + 1]):
                patternCount[word[i]] = None
            i += 1
    for char in patternCount:
        if(patternCount[char] is not None):
            result[char] = {"next": patternCount[char]}
            if(char in end):
                result[char]["end"] = True
            else:
                result[char]["end"] = False
    return result


# Check proceeding characters patterns
def checkProceeding(permutations):
    patternCount = {}
    start = {}
    result = {}
    for word in permutations:
        if(len(word) > 1):
            start[word[0]] = True
        i = 1
        while(i < len(word)):
            if(word[i] not in patternCount):
                patternCount[word[i]] = word[i - 1]
            if(patternCount[word[i]] != word[i - 1]):
                patternCount[word[i]] = None
            i += 1
    for char in patternCount:
        if(patternCount[char] is not None):
            result[char] = {"prev": patternCount[char]}
            if(char in start):
                result[char]["start"] = True
            else:
                result[char]["start"] = False
    return result


# Find characters that have only odd or even occurrences in all permutations
def checkOddEven(permutations):
    patternCount = {}
    iteration = 0
    result = {
        "odd": [],
        "even": []
    }
    # To avoid checking for odd characters that only occur once in all
    # permutations
    occursOnce = {}
    for word in permutations:
        iteration += 1
        chars = set(word)
        for char in chars:
            if(char not in patternCount):
                patternCount[char] = {}
            patternCount[char][iteration] = (word.count(char) % 2) == 0
            if(char not in occursOnce):
                occursOnce[char] = {}
            if(word.count(char) == 1):
                occursOnce[char][iteration] = True
            else:
                occursOnce[char][iteration] = False
    for char in occursOnce:
        if(checkList(occursOnce[char].values(), True)):
            patternCount[char][1] = None
    for char in patternCount:
        isAllEven = checkList(patternCount[char].values(), True)
        isAllOdd = checkList(patternCount[char].values(), False)
        if(isAllEven):
            result["even"].append(char)
        if(isAllOdd):
            result["odd"].append(char)
    return result


# Checks if all elements in a list are same as compareTo
def checkList(lst, compareTo):
    elem = compareTo
    isSame = True
    for item in lst:
        if elem != item:
            isSame = False
            break
    return isSame


# Checks if an input string satisfies a regex
def checkPatternMatch(inputStr, patternInput):
    pattern = re.compile(patternInput)
    if(re.fullmatch(pattern, inputStr)):
        return True
    return False


# Check for similarity to popular regex patterns such as phone number and
# email regex validation
def checkPopularPatterns(outputSet):
    matches = {
        "emails": None,
        "phone": None
    }
    for word in outputSet:
        if(checkPatternMatch(word, emailRegex) and (matches["emails"] is None or matches["emails"] is True)):
            matches["emails"] = True
        else:
            matches["emails"] = False
        phoneResult = []
        for key in phoneRegexes:
            regex = phoneRegexes[key]
            phoneResult.append(checkPatternMatch(word, regex))
        if (True in phoneResult and (
                matches["phone"] is None or matches["phone"] is True)):
            matches["phone"] = True
        else:
            matches["phone"] = False
    return matches


# Main method to compute all results
def patternRecognition(permutations, inputRegex):
    patternsOutput = {}
    patternsOutput["minimumLength"] = minimumLength(permutations, inputRegex)
    patternsOutput["preceding"] = checkPrecedence(permutations)
    patternsOutput["proceeding"] = checkProceeding(permutations)
    patternsOutput["oddEven"] = checkOddEven(permutations)
    patternsOutput["popularPatterns"] = checkPopularPatterns(permutations)
    return patternsOutput
