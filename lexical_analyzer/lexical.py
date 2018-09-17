import re


class Lexical:
    def __init__(self, _file_path=''):
        self._file_path = _file_path
        self._dictionary = []
        self._line_counter = 1
        self._tokens_list = []
        self._delimiters = set(';,:()')
        self._sum_operators = ['+', '-', 'or']
        self._assignment_operator = [':=']
        self._multiply_operators = ['*', '/', 'and']
        self._relational_operators = ['<', '>', '<=', '>=', '=', '<>']
        self._keywords = ['var', 'char', 'begin', 'end', 'program', 'integer', 'real', 'boolean', 'procedure', 'if',
                          'then', 'else', 'while', 'not', 'do']
        self._booleans = ['true', 'false']

    def analyze(self):
        self._line_counter = 1
        self.__read_archive()

    def __read_archive(self):

        with open(self._file_path, "r") as file:
            source_code = file.read()
            source_code_no_comments = self._process_comments(source_code)
            lines = source_code_no_comments.splitlines()

            for line in lines:
                # new_line = process_comments(line)
                self._read_line(line)
                self._line_counter = self._line_counter + 1

    def _read_line(self, line=''):
        line = re.sub(r'//.*', '', line)
        # line = new_patterns(line) #for new patterns that might be added
        # symbols = re.findall(r':=|<>|<=|>=|[=;,><+\-*/(){}]|[^\w\s\.]', line)
        # no_symbols = re.sub(r'(\w+)*[,;=:><+\-*/](\w+)*', r'\1 \2', line) # removing symbols except for dot '.'
        # no_symbols_tokens = no_symbols.split() #spliting into tokens
        self._analyzer(line)
        # analyze(no_symbols_tokens)
        # analyze_symbols(symbols)

    def _process_comments(self, source_code=''):
        counter = 0
        index_counter = 0
        new_source_code = list(source_code)
        for character in new_source_code:
            # print (character + " " + str(counter) + " ")
            if character == '{' and counter == 0:
                # print ("{ found")
                new_source_code[index_counter] = ""
                counter = 1
            elif character == '}' and counter == 1:
                # print ("} Found")
                new_source_code[index_counter] = ""
                counter = 0
            elif counter == 1 and character != '\n':
                # print ("inside comment")
                new_source_code[index_counter] = ""
            index_counter += 1
        if counter == 1:
            print('Error: Curly brackets of comments open|closed without opening|closing the other. Symbol')
            exit(1)
        return ''.join(new_source_code)

    def _analyzer(self, line=''):
        self._tokens_list = re.sub(r'(\w*)(:=|<>|<=|>=|[=;,><+\-*/(){}]|[^\w\s\.])(\w*)', r'\1 \2 \3', line).split()  # inserting space between simbols to split correctly
        for token in self._tokens_list:
            self._analyze_token(token)

    def _analyze_token(self, token=''):
        if not self._analyze_words(token):
            if not self._analyze_symbols(token):
                print('Error: Character not recognized by language. Symbol: \''
                      + token + '\' , at line: ' + str(self._line_counter))
                exit(1)

    def _analyze_words(self, word=''):
        match = re.match(r'\d+\.\d*x\d+\.\d*y\d+\.\d*z', word)
        if match:
            self._dictionary.append([match.group(), 'float_3d', self._line_counter])
            self._reappend(word, match.group())
            return True
        # Analyzing if it is a float number
        match = re.match(r'\d+\.\d*', word)
        if match:
            self._dictionary.append([match.group(), 'real', self._line_counter])
            self._reappend(word, match.group())
            return True
        # Analyzing if it is  a integer
        # Note that tokens like 33ff will be identified as integer
        # But, in fact it a combination of both integer and identifier
        # Therefor  e, they'll be broken into two parts, putting the second
        # to be analyzed again
        match = re.match(r'\d+', word)
        if match:
            self._dictionary.append([match.group(), 'integer', self._line_counter])
            self._reappend(word, match.group())
            return True
        # Analyzing if it is either a keyword or identifier
        match = re.match(r'[a-zA-Z]\w*', word)
        if match:
            if word in self._sum_operators:
                self._dictionary.append([match.group(), 'sum_operator', self._line_counter])
            elif word in self._multiply_operators:
                self._dictionary.append([match.group(), 'multiply_operator', self._line_counter])
            elif word in self._keywords:
                self._dictionary.append([match.group(), 'keyword', self._line_counter])
            elif word in self._booleans:
                self._dictionary.append([match.group(), 'boolean', self._line_counter])
            else:
                self._dictionary.append([match.group(), 'identifier', self._line_counter])
                self._reappend(word, match.group())
            return True
        if word == '.':
            self._dictionary.append([word, 'delimiter', self._line_counter])
            return True
        match = re.match(r'(\.)\w*', word)
        if match:
            self._dictionary.append([match.group(1), 'delimiter', self._line_counter])
            new_word = re.sub(r'\.', '', word, 1)

            if len(new_word) > 0:
                self._analyze_token(new_word)
            return True

        return False

    def _analyze_symbols(self, symbol=''):
        found = True
        if symbol in self._delimiters:
            self._dictionary.append([symbol, 'delimiter', self._line_counter])
        elif symbol in self._sum_operators:
            self._dictionary.append([symbol, 'sum_operator', self._line_counter])
        elif symbol in self._multiply_operators:
            self._dictionary.append([symbol, 'multiply_operator', self._line_counter])
        elif symbol in self._relational_operators:
            self._dictionary.append([symbol, 'relational_operator', self._line_counter])
        elif symbol in self._assignment_operator:
            self._dictionary.append([symbol, 'assignment_operator', self._line_counter])
        else:
            found = False

        return found

    def _reappend(self, word="", match=""):
        if word != match:
            new_word = re.sub(match, '', word, 1)
            if len(new_word) > 0:
                self._analyze_token(new_word)

    def get_list(self):
        return self._dictionary.copy()


