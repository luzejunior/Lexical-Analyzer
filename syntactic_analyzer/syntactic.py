WORD = 0
CLASSIFICATION = 1
LINE = 2
MISSING_ARG = -1
MISSING_ID = -2


class Syntactic:
    def __init__(self, lexical_input=['token','classification',1]):
        self.lexical_input = lexical_input[::-1]
        self.success = False
        self._last_read =[]

    def _show_error(self, token=[], error_msg=''):
        if token == False:
            error_msg = '[Syntax Error] Reached EOF.'\
                        ' | LAST TOKEN: \''+ self._get_word(self._last_read)\
                        + '\' | LINE: ' + str(self._get_line(self._last_read)) + ' | Description:  ' + error_msg
        else:
            error_msg = '[Syntax Error] CURRENT TOKEN: \'' + self._get_word(token) + '\' | LINE: '\
                        + str(self._get_line(token)) +\
                        '| Description: ' + error_msg
        print(error_msg)
        return exit(0)

    def _get_next_token(self, pop=True):
        if len(self.lexical_input) == 0:
            # if self.success:
            #     print('Syntax Analyzer has completed the process with success.')
            # else:
            #     print('Syntax Analyzer has completed the process with NO success.')
            # exit(0)
            return False
        self._last_read = self.lexical_input[-1]
        if pop:
            return self.lexical_input.pop()
        else:
            return self.lexical_input[-1]


    def _get_word(self, token=[]):
        return token[WORD]

    def _get_line(self, token=[]):
        return token[LINE]

    def _checker(self,token=[],type_=WORD, compare_to=''):
        return token and token[type_] == compare_to

    def _get_classification(self, token=[]):
        return token[CLASSIFICATION]

    def start(self):
        # print(self.lexical_input)
        self._program_routine()

    def _program_routine(self, capture_error=True):
        token = self._get_next_token()
        if self._checker(token, type_=WORD, compare_to='program'):
            token = self._get_next_token()
            if self._checker(token, type_=CLASSIFICATION, compare_to='identifier'):
                token = self._get_next_token()
                if self._checker(token, type_=WORD, compare_to=';'):
                    # checking now for possible declarations
                    token = self._get_next_token(pop=False)
                    if self._checker(token, type_=WORD, compare_to='var'):
                        self._get_next_token()
                        self._variables_declaration_routine()
                    self._sub_programs_routine()
                    self.success = True

                else:
                    self._show_error(token, error_msg='Missing expected \';\'. {Program_Routine}.')
            else:
                self._show_error(token, error_msg='Missing expected identifier. {Program_Routine}')
        else:
            self._show_error(token, error_msg='Missing expected \'program\'. {Program_Routine}')

    def _variables_declaration_routine(self, capture_error=True):

        self._identifiers_list_routine()
        token = self._get_next_token()
        if self._checker(token, type_=WORD, compare_to=':'):
            self._type_routine()
            token = self._get_next_token()
            if self._checker(token, type_=WORD, compare_to=';'):
                self._variable_declaration_subroutine()
            else:
                if capture_error:
                    self._show_error(token, error_msg='Missing expected \';\'. {Variable_Declaration_Routine}')
        else:
            if capture_error:
                self._show_error(token, error_msg='Missing expected \':\'. {Variable_Declaration_Routine}')

    def _variable_declaration_subroutine(self):
        #it might be empty
        if self._identifiers_list_routine(capture_error=False):
            token = self._get_next_token()
            if self._checker(token, type_=WORD, compare_to=':'):
                self._type_routine()
                token = self._get_next_token()
                if self._checker(token, type_=WORD, compare_to=';'):
                    self._variable_declaration_subroutine()
                else:
                    self._show_error(token, error_msg='Missing expected \';\'. {Variable_SubDeclaration_Routine}')
            else:
                self._show_error(token, error_msg='Missing expected \':\'. {Variable_SubDeclaration_Routine}')

    def _identifiers_list_routine(self, capture_error=True):
        token = self._get_next_token(pop=capture_error)
        if self._checker(token,type_=CLASSIFICATION, compare_to='identifier'):
            self._get_next_token(pop=not capture_error)
            self._identifiers_list_subroutine()
            if not capture_error:
                return True
        else:
            if capture_error:
                self._show_error(token, error_msg='Missing expected identifier. {Identifier_List_Routine}')
            else:
                return False

    def _identifiers_list_subroutine(self):
        token = self._get_next_token(pop=False) #not popping token cause routine accepts empty
        if self._checker(token, type_=WORD, compare_to=','):
            self._get_next_token() #it means the current token can be popped from list
            token = self._get_next_token()
            if self._checker(token, type=CLASSIFICATION, compare_to='identifier'):
                self._identifiers_list_subroutine()
            else:
                self._show_error(token,error_msg='Missing expected identifier. {Identifier_SubList_Routine}')

    def _type_routine(self, capture_error=True):
        token = self._get_next_token()
        if not self._checker(token, type_=WORD, compare_to='integer'):
            if not self._checker(token, type_=WORD, compare_to='real'):
                if not self._checker(token, type_=WORD, compare_to='boolean'):
                    self._show_error(token, error_msg='Missing expected type. {Type_Routine}')



    def _sub_programs_routine(self, capture_error=True):
        if self._sub_program_routine(capture_error=False):
            token = self._get_next_token()
            if self._checker(token, type_=WORD, compare_to=';'):
                self._sub_programs_routine()
            else:
                self._show_error(token, error_msg='Missing expected \';\'.')

    def _sub_program_routine(self, capture_error=True):
        token = self._get_next_token(pop=capture_error)
        if self._checker(token, type_=WORD, compare_to='procedure'):
            self._get_next_token(pop=not capture_error)
            token = self._get_next_token()
            if self._checker(token, type_=CLASSIFICATION, compare_to='identifier'):
                self._arguments_routines(capture_error=False)
                token = self._get_next_token()
                if self._checker(token, type_=WORD, compare_to=';'):
                    token = self._get_next_token(pop=False)
                    if self._checker(token,type_=WORD, compare_to='var'):
                        self._get_next_token()
                        self._variables_declaration_routine()
                    self._sub_programs_routine()
                    # self._compound_command_routine()

                else:
                    self._show_error(token, error_msg='Missing expected \';\'.')
            else:
                self._show_error(token, error_msg='Missing expected \';\'.')
            return True
        else:
            if capture_error:
                self._show_error(token, error_msg='Missing expected \';\'.')
            else:
                return False






    def _arguments_routines(self, capture_error=True):
        token = self._get_next_token(pop=capture_error)
        if self._checker(token, type_=WORD, compare_to='('):
            self._get_next_token(pop= not capture_error)
            self._parameters_list_routine()
            token = self._get_next_token()
            if self._checker(token,type_=WORD, compare_to=')'):
                self._show_error(token, 'Missing expected \')\'.')
            return True
        else:
            if capture_error:
                self._show_error(token,'Missing expected \'(\'.')
            else:
                return False


    def _parameters_list_routine(self, capture_error=True):
        self._identifiers_list_routine()
        token = self._get_next_token()
        if token and self._get_word(token) == ':':
            self._type_routine()
            self._parameters_list_subroutine()
        else:
            self._show_error(token, error_msg='Missing expected \':\'.')




    def _parameters_list_subroutine(self):
        token = self._get_next_token(pop=False)
        if self._checker(token, type_=WORD, compare_to=';'):
            self._get_next_token()
            self._identifiers_list_routine()
            token = self._get_next_token()
            if self._checker(token,type_=WORD,compare_to=':'):
                    self._type_routine()
                    self._parameters_list_subroutine()
            else:
                self._show_error(token,error_msg='Missing expected \':\'.')

    #
    # def _compound_command_routine(self, capture_error=True):






