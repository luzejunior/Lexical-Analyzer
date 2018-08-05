    import re

    dictionary = []
    dict2 = []
    lineCounter = 1
    delimiters = set(':;.')
    key_words = ['var', 'char', 'begin', 'end','program','integer','real','boolean','procedure','if','then'',else','while','not','do']


    def main():
        readArchive("program.txt")
        printDictionary()


    def readArchive(path):
        global lineCounter
        with open(path, "r") as file:
            for line in file:
                readLine(line)
                lineCounter = lineCounter + 1


    def pre_process(line):
        new_line = re.sub(r'{.*}', "", line) # Remove Commentaries '{}'
        return re.sub('\n', '', new_line)


    def readLine(line):
        global dict2
        # split = line.split(); # Split line into tokens
        # split = re.findall(r'[0-9]+.[0-9]*|[0-9]+|:=|[:;,.+-/*()><=]|\w+',line) # Split line into tokens
        # split = re.findall(r'\w+', line)
        # print(split)
        pre_processed = pre_process(line)
        no_symbols = re.sub(r'(\w+)*[,;=:><+\-*/](\w+)*', r'\1 \2', pre_processed) # removing symbols
        # print(no_symbols)
        no_symbols_tokens = no_symbols.split() #spliting into tokens
        analyze(no_symbols_tokens)
        # for word in no_symbols_tokens:
        #     found = False
        #     match = re.search(r'^[0-9]+', word)
        #     if match:
        #         dictionary.append([word, "integer", lineCounter])
        #         found = True
        #         break
        #
        #     if found == False:
        #         for delimiter in delimiters:
        #             if word == delimiter:
        #                 # dictionary.append("Token: " + word +  " labeled as: Delimiter, at line: " + str(lineCounter)) # Print delimiter
        #                 dictionary.append([word, "delimiter", lineCounter])
        #                 found = True
        #                 break
        #     # if any((d in delimiters) for d in word): # Dummy way to search delimiters
        #     #    strDelimiter = word[len(word)-1] # Get delimiter string
        #     #    dictionary.append("Token: " + word.replace(strDelimiter, "") + ", at line: " + str(lineCounter)) # Remove delimiter from word
        #     #    dictionary.append("Token: " + strDelimiter +  " labeled as: Delimiter, at line: " + str(lineCounter)) # Print delimiter
        #     # else: # If none delimiter was found
        #     if found == False:
        #         dictionary.append([word, "", lineCounter])


    def analyze(tokens):
        for word in tokens:
            # Analyzing if it is a float number
            match = re.match(r'\d+\.\d*', word)
            if match:
                if match.group() != word:
                    tokens.append(re.sub(match.group(), '', word, 1))
                dictionary.append([match.group(), 'float', lineCounter])
                continue
            # Analyzing if it is  a integer
            # Note that tokens like 33ff will be identified as integer
            # But, in fact it a combination of both integer and identifier
            # Therefore, they'll be broken into two parts, putting the second
            # to be analyzed again
            match = re.match(r'\d+', word)
            if match:
                if match.group() != word:
                    tokens.append(re.sub(match.group(), '', word, 1))
                dictionary.append([match.group(), 'integer', lineCounter])
                continue
            if word == '.':
                dictionary.append([word, 'delimiter', lineCounter])
                continue
            match = re.match(r'\w*(\.)\w*', word)
            if match:
                dictionary.append([match.group(1), 'delimiter', lineCounter])
                new_words = re.sub(r'\.', ' ', word, 1)
                new_words = new_words.split()
                for w in new_words:
                    tokens.append(w)
                continue

            #Analyzing if it is either a keyword or identifier
            match = re.match(r'[a-zA-Z]\w*', word)
            if match:
                re.match(r'[a-zA-Z]\w*', word)
                if word in key_words:
                    dictionary.append([word, 'keyword', lineCounter])
                else:
                    dictionary.append([word, 'identifier', lineCounter])
                continue



    def printDictionary():
        for line in dictionary:
            print (line)
        # print dictionary


    if __name__ == "__main__":
        main()
