WORD = 0
CLASSIFICATION = 1
LINE = 2
MISSING_ARG = -1
MISSING_ID = -2


class Syntactic:
    def __init__(self, lexical_input=['token','classification',1]):
        self.lexical_input = lexical_input[::-1]

    def _show_error(self,error_type=0 , token = []):
        if error_type == MISSING_ARG:
            print('Missing argument ' + token[WORD] + ' at line ' + int(token[LINE]) + '.')
        elif error_type == MISSING_ID:
            print('Missing identifier following \'program\'...')
        print('Exiting program...')
        exit(0)

    def _get_next_token(self,pop=True):
        if len(self.lexical_input) == 0:
            return False
        if pop:
            return self.lexical_input.pop()
        else:
            return self.lexical_input[-1]


    def _get_word(self, token=[]):
        return token[WORD]

    def _get_line(self, token=[]):
        return token[LINE]

    def _get_classification(self, token=[]):
        return token[CLASSIFICATION]

    def test(self):

        while True:
            token = self._get_next_token()
            if not token:
                break

            print(self._get_classification(token) + ' ' + self._get_word(token))

    def _program_routine(self):
        token = self._get_next_token()
        if token and self._get_word(token) == 'program':
            token = self._get_next_token()
            if token and self._get_classification(token) == 'identifier':
                token = self._get_next_token()
                if token and self._get_word(token) == ';':
                    # checking now for possible declarations
                    token = self._get_next_token(pop=False)
                    if token and self._get_word(token) == 'var':
                        self._get_next_token()
                        self._variables_declaration_routine()

                    # todo subprograms declaration routine

                    if token and self._get_word(token) == 'begin':
                else:
                    self._show_error(MISSING_ARG, token)
            else:
                self._show_error(MISSING_ID, token)
        else:
            self._show_error(MISSING_ARG, token)


    def _variables_declaration_routine(self):

        self._identifiers_list_routine()
        token = self._get_next_token()
        if token and self._get_word(token) == ':':
            self._type_routine()
            token = self._get_next_token()
            if token and self._get_word(token) == ';':
                self._variable_declaration_subroutine()
            else:
                self._show_error(MISSING_ARG,token)
        else:
            self._show_error(MISSING_ARG,token)

    def _variable_declaration_subroutine(self):
        #it might be empty
        if self._identifiers_list_routine():
            token = self._get_next_token()
            if token and self._get_word(token) == ':':
                self._type_routine()
                token = self._get_next_token()
                if token and self._get_word(token) == ';':
                    self._variable_declaration_subroutine()
                else:
                    self._show_error(MISSING_ARG,token)
            else:
                self._show_error(MISSING_ARG,token)



    def _identifiers_list_routine(self):
        token = self._get_next_token(pop=False)
        if token and self._get_classification(token) == 'identifier':
            self._get_next_token()
            self._identifiers_list_subroutine()
            return True
        else:
            return False

    def _identifiers_list_subroutine(self):
        token = self._get_next_token(pop=False) #not popping token cause routine accepts empty
        if token and self._get_word() == ',':
            self._get_next_token() #it means the current token can be popped from list
            token = self._get_next_token()
            if token and self._get_classification(token) == 'identifier':
                self._identifiers_list_subroutine()
            else:
                self._show_error(MISSING_ARG,token)
            return True
        else:
            return False


    def _type_routine(self):
        token = self._get_next_token()
        if token:
            word = self._get_word(token)
            if word != 'boolean' and word != 'real' and word != 'integer':
                self._show_error(MISSING_ARG,token)


    def _sub_programs_routine(self):
        if self._sub_program_routine():
            token = self._get_next_token()
            if token and self._get_word(token) == ';':
                self._sub_programs_routine()
            else:
                self._show_error(MISSING_ARG,token)
            return True
        else:
            return False



    def _sub_program_routine(self):
        token = self._get_next_token(pop=False)
        if token and self._get_word(token) == 'procedure':
            self._get_next_token()
            token = self._get_next_token()
            if token and self._get_classification() == 'identifier':
                









