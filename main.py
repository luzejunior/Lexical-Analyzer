import re

dictionary = []
dict2 = []
lineCounter = 1
delimiters = set(':;.')
palavras_reservadas = ["var", "char", "begin", "end"]

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
    global dict2
    line = re.sub(r'{.*}', "", line) # Remove Commentaries '{}'
    # split = line.split(); # Split line into tokens
    split = re.findall(r'[0-9]+.[0-9]*|\w+|:=|[;:,.]',line)
    #print split
    for word in split:
        found = False

        match = re.search(r'^[0-9]+', word)
        if match:
            dictionary.append([word, "integer", lineCounter])
            found = True
            break

        if found == False:
            for delimiter in delimiters:
                if word == delimiter:
                    #dictionary.append("Token: " + word +  " labeled as: Delimiter, at line: " + str(lineCounter)) # Print delimiter
                    dictionary.append([word, "delimiter", lineCounter])
                    found = True
                    break
        #if any((d in delimiters) for d in word): # Dummy way to search delimiters
        #    strDelimiter = word[len(word)-1] # Get delimiter string
        #    dictionary.append("Token: " + word.replace(strDelimiter, "") + ", at line: " + str(lineCounter)) # Remove delimiter from word
        #    dictionary.append("Token: " + strDelimiter +  " labeled as: Delimiter, at line: " + str(lineCounter)) # Print delimiter
        #else: # If none delimiter was found
        if found == False:
            dictionary.append([word, "", lineCounter])

def printDictionary():
    for line in dictionary:
        print line
    #print dictionary

if __name__ == "__main__":
    main()
