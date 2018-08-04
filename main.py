import re

dictionary = []
lineCounter = 1
delimiters = set(':;.')

def main():
    readArchive("program.txt")
    printDictionary()

def readArchive(path):
    global lineCounter
    with open(path, "r") as file:
        for line in file:
            readLine(line)
            lineCounter = lineCounter + 1

def readLine(line):
    line = re.sub(r'{.*}', "", line) # Remove Commentaries '{}'
    split = line.split(); # Split line into tokens
    for word in split:
        if any((d in delimiters) for d in word): # Dummy way to search delimiters
            strDelimiter = word[len(word)-1] # Get delimiter string
            dictionary.append("Token: " + word.replace(strDelimiter, "") + ", at line: " + str(lineCounter)) # Remove delimiter from word
            dictionary.append("Token: " + strDelimiter +  " labeled as: Delimiter, at line: " + str(lineCounter)) # Print delimiter
        else: # If none delimiter was found
            dictionary.append("Token: " + word + ", at line: " + str(lineCounter))

def printDictionary():
    for line in dictionary:
        print line

if __name__ == "__main__":
    main()
