import re

dictionary = []
dict2 = []
lineCounter = 1
tokens_list = []
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
        source_code_no_comments = process_comments(source_code)
        lines = source_code_no_comments.splitlines()

        for line in lines:
            #new_line = process_comments(line)
            readLine(line)
            lineCounter = lineCounter + 1


def cleanComment(line):
    return re.sub(r'//.*', '', line)


def process_comments(source_code):
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
    line = cleanComment(line)
    # line = new_patterns(line) #for new patterns that might be added
    # symbols = re.findall(r':=|<>|<=|>=|[=;,><+\-*/(){}]|[^\w\s\.]', line)
    # no_symbols = re.sub(r'(\w+)*[,;=:><+\-*/](\w+)*', r'\1 \2', line) # removing symbols except for dot '.'
    # no_symbols_tokens = no_symbols.split() #spliting into tokens
    analyzer(line)
    # analyze(no_symbols_tokens)
    # analyze_symbols(symbols)


def analyzer(line=""):
    global tokens_list
    tokens_list = re.sub(r'(\w*)(:=|<>|<=|>=|[=;,><+\-*/(){}]|[^\w\s\.])(\w*)', r'\1 \2 \3', line).split() #inserting space between simbols to split correctly
    for token in tokens_list:
        analyze_token(token)


def analyze_token(token):
    if not analyze_words(token):
        if not analyze_symbols(token):
            print('Error: Character not recognized by language. Symbol: \''
                  + token + '\' , at line: ' + str(lineCounter))
            exit(1)


def new_patterns(line):
    new_floats = re.findall(r'\d+\.\d*x\d+\.\d*y\d+\.\d*z', line)
    for new_float in new_floats:
        dictionary.append([new_float, 'float_3d', lineCounter])
    return re.sub(r'\d+\.\d*x\d+\.\d*y\d+\.\d*z', '', line)


def reappend(word="", match=""):
    if word != match:
        new_word = re.sub(match, '', word, 1)
        if len(new_word) > 0:
            analyze_token(new_word)


def analyze_words(word):
    # match = re.match(r'\+\d+\e\-\d+', word)
    # if match:
    #     dictionary.append([match.group(),'new_real',lineCounter])
    # Analyzing if it is a float number
    match = re.match(r'\d+\.\d*', word)
    if match:
        dictionary.append([match.group(), 'float', lineCounter])
        reappend(word, match.group())
        return True
    # Analyzing if it is  a integer
    # Note that tokens like 33ff will be identified as integer
    # But, in fact it a combination of both integer and identifier
    # Therefor  e, they'll be broken into two parts, putting the second
    # to be analyzed again
    match = re.match(r'\d+', word)
    if match:
        dictionary.append([match.group(), 'integer', lineCounter])
        reappend(word, match.group())
        return True
    # Analyzing if it is either a keyword or identifier
    match = re.match(r'[a-zA-Z]\w*', word)
    if match:
        if word in key_words:
            dictionary.append([match.group(), 'keyword', lineCounter])
        else:
            dictionary.append([match.group(), 'identifier', lineCounter])
            reappend(word, match.group())
        return True
    if word == '.':
        dictionary.append([word, 'delimiter', lineCounter])
        return True
    match = re.match(r'(\.)\w*', word)
    if match:
        dictionary.append([match.group(1), 'delimiter', lineCounter])
        new_word = re.sub(r'\.', '', word, 1)

        if len(new_word) > 0:
            analyze_token(new_word)
        return True

    return False

def analyze_symbols(symbol):
    found = True
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
    else:
        found = False

    return found




def printDictionary():
    for line in dictionary:
        print (line)
    # print dictionary


if __name__ == "__main__":
    main()
