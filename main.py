import re

dictionary = []
dict2 = []
lineCounter = 1
delimiters = set(';,:()')
sum_operators = set('+-')
assignment_operator = [':=']
multiply_operators = set('*/')
relational_operators = ['<','>','<=','>=','=','<>']

key_words = ['var', 'char', 'begin', 'end','program','integer','real','boolean','procedure','if','then'',else','while','not','do']


def main():
    readArchive("program.txt")
    printDictionary()


def readArchive(path):
    global lineCounter
    with open(path, "r") as file:
        source_code = file.read()
        lines = process_comments(source_code)
        for line in lines:
            readLine(line)
            lineCounter = lineCounter + 1


def pre_process(line):
    new_line = re.sub(r'{.*}', "", line) # Remove Commentaries '{}'
    return re.sub('\n', '', new_line)

def process_comments(source_code):
    source_code = re.sub(r'\n', '\\c', source_code)
    source_code = re.sub(r'{.*}', '', source_code)
    source_code = re.sub(r'\\c', r'\n', source_code)
    return source_code.splitlines()



def readLine(line):
    global dict2
    pre_processed = pre_process(line)
    symbols = re.findall(r':=|<>|<=|>=|[=;,><+\-*/(){}]|[^\w\s\.]', line)
    # print(unreconized_symbols)
    no_symbols = re.sub(r'(\w+)*[,;=:><+\-*/](\w+)*', r'\1 \2', pre_processed) # removing symbols except for dot '.'
    no_symbols_tokens = no_symbols.split() #spliting into tokens

    analyze(no_symbols_tokens)
    analyze_symbols(symbols)


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
            re.match(r'[a-zA-Z]\w*', word)
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
