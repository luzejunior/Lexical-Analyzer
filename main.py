import re

dictionary = []
dict2 = []
lineCounter = 1
delimiters = set(';,:()')
sum_operators = set('+-')
assignment_operator = [':=']
multiply_operators = set('*/')
relational_operators = ['<','>','<=','>=','=','<>']

key_words = ['var', 'char', 'begin', 'end','program','integer','real','boolean','procedure','if','then','else','while','not','do']


def main():
    readArchive("program.txt")
    printDictionary()


def readArchive(path):
    global lineCounter
    with open(path, "r") as file:
        source_code = file.read()
        source_code_no_comments = process_comments2(source_code)
        lines = source_code_no_comments.splitlines()
        for line in lines:
            #new_line = process_comments(line)
            readLine(line)
            #print (line)
            lineCounter = lineCounter + 1


# def pre_process(line):
#     new_line = re.sub(r'{.*}', "", line) # Remove Commentaries '{}'
#     return re.sub('\n', '', new_line)

# def process_comments(line):
#     #source_code = re.sub(r'\n', '\\c', source_code)
#     return re.sub(r'{.*}|{.*$|^.+}', "", line)
#     #source_code = re.sub(r'\\c', r'\n', source_code)
#     #return source_code.splitlines()

def process_comments2(source_code):
    counter = 0
    index_counter = 0
    new_source_code = list(source_code)
    for character in new_source_code:
        #print (character + " " + str(counter) + " ")
        if character == '{' and counter == 0:
            #print ("{ found")
            new_source_code[index_counter] = ""
            counter = 1
        elif character == '}' and counter == 1:
            #print ("} Found")
            new_source_code[index_counter] = ""
            counter = 0
        elif counter == 1 and character != '\n':
            #print ("inside comment")
            new_source_code[index_counter] = ""
        index_counter += 1
    if counter == 1:
        print('Error: Curly brackets of comments open|closed without opening|closing the other. Symbol')
        exit(1)
    return ''.join(new_source_code)


def readLine(line):
    global dict2
    line = new_patterns(line) #for new patterns that might be added
    symbols = re.findall(r':=|<>|<=|>=|[=;,><+\-*/(){}]|[^\w\s\.]', line)
    no_symbols = re.sub(r'(\w+)*[,;=:><+\-*/](\w+)*', r'\1 \2', line) # removing symbols except for dot '.'
    no_symbols_tokens = no_symbols.split() #spliting into tokens

    analyze(no_symbols_tokens)
    analyze_symbols(symbols)


def new_patterns(line):
    new_floats = re.findall(r'\+\d+\e\-\d+', line)
    for new_float in new_floats:
        dictionary.append([new_float, 'new_float', lineCounter])
    return re.sub(r'\+\d+\e\-\d+', '', line)


def analyze(tokens):
    for word in tokens:
        # match = re.match(r'\+\d+\e\-\d+', word)
        # if match:
        #     dictionary.append([match.group(),'new_real',lineCounter])
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
        # Therefor  e, they'll be broken into two parts, putting the second
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
            if word in key_words:
                dictionary.append([word, 'keyword', lineCounter])
            else:
                dictionary.append([word, 'identifier', lineCounter])
            continue


def analyze_symbols(tokens):
    for symbol in tokens:
        if symbol in delimiters:
            dictionary.append([symbol, 'delimiter', lineCounter])
        elif symbol in sum_operators:
            dictionary.append([symbol, 'sum_operator', lineCounter])
        elif symbol in multiply_operators:
            dictionary.append([symbol, 'multiply_operator', lineCounter])
        elif symbol in relational_operators:
            dictionary.append([symbol, 'relational_operator', lineCounter])
        elif symbol in assignment_operator:
            dictionary.append([symbol, 'assignment_operator', lineCounter])
        elif symbol in ['{','}']:
            print('Error: Curly brackets of comments open|closed without opening|closing the other. Symbol: \''
                  + symbol + '\' , at line: ' + str(lineCounter))
            exit(1)
        else:
            print('Error: Character not recognized by language. Symbol: \''
                  + symbol + '\' , at line: ' + str(lineCounter))
            exit(1)




def printDictionary():
    for line in dictionary:
        print (line)
    # print dictionary


if __name__ == "__main__":
    main()
