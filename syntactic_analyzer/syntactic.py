WORD = 0
CLASSIFICATION = 1
LINE = 2
MARK = '$'
TOP = -1
SUBTOP = -2


class Syntactic:
    def __init__(self, lexical_input=['token', 'classification', 1]):
        self.lexical_input = lexical_input[::-1]
        self.success = False
        self._last_read = []
        self._symbols_table = []
        self._symbol_arguments_table = []
        self._types_table = []
        self._current_arithmetic_op = 'none'
        self._arguments = []
        self._current_procedure = []

    def _enter_scope(self):
        self._symbols_table.append([MARK, "mark"])

    def _exit_scope(self):
        if len(self._symbols_table) > 0:
            symbol = self._symbols_table[-1]
            while symbol[0] != MARK:
                self._symbols_table.pop()
                symbol = self._symbols_table[-1]
            self._symbols_table.pop()

    def _validate_declaration(self, token, type = ""):

        for symbol in reversed(self._symbols_table):

            if self._get_word(token) == symbol[0]:
                if (type == 'procedure' and symbol[1] != 'procedure') or (type != 'procedure' and symbol[1] == 'procedure') :
                  print('oi')
                else:
                    self._show_error(token, 'This symbol has already been declared in the current scope.'
                                        ' {Validate Declaration Routine}')
            if symbol[0] == MARK:
                self._symbols_table.append([self._get_word(token), type])
                break

    def _check_symbol_usage(self, token):
        word = self._get_word(token)
        for symbol in reversed(self._symbols_table):
            if symbol[0] == word:
                return
        self._show_error(token, 'Symbol used hasn\'t been declared in the current scope. {Check Symbol Usage Routine}')

    def _update_symbol_list(self, type_):
        for symbol in self._symbols_table:
            if symbol[1] == "":
                symbol[1] = type_

    def _push_symbol_table(self, token='', type_=''):
        if type_ != '':
            self._types_table.append(type_)
            return

        found = False
        word = self._get_word(token)
        for symbol in reversed(self._symbols_table):
            if symbol[0] == word and symbol[1] != 'procedure':
                self._types_table.append(symbol[1])
                found = True
                break

        if not found:
            self._show_error(token,
                             'Symbol used hasn\'t been declared in the current scope. {Check Symbol Usage Routine}')

    def _replace_symbol_table(self, new_type=''):
        self._types_table.pop()
        self._types_table.pop()
        if new_type != '':
            self._types_table.append(new_type)

    def _relational_operation_handler(self):

        if self._types_table[TOP] == 'integer' and self._types_table[SUBTOP] == 'integer':
            self._replace_symbol_table('boolean')
        elif self._types_table[TOP] == 'integer' and self._types_table[SUBTOP] == 'real':
            self._replace_symbol_table('boolean')
        elif self._types_table[TOP] == 'real' and self._types_table[SUBTOP] == 'integer':
            self._replace_symbol_table('boolean')
        elif self._types_table[TOP] == 'real' and self._types_table[SUBTOP] == 'real':
            self._replace_symbol_table('boolean')
        else:
            self._show_error(error_msg='Type mismatched in relational operation.'
                                       ' Comparison between \'' + self._types_table[TOP] +
                                       '\' and \'' + self._types_table[SUBTOP] +
                                       '\' not allowed. {Relational Operational Handler}')

    def _arithmetic_operation_handler(self):
        if self._current_arithmetic_op in ['and', 'or']:
            if self._types_table[TOP] == 'boolean' and self._types_table[SUBTOP] == 'boolean':
                self._types_table.pop()  # only one pop cause the type boolean must stay
                #  in order to make type check if others operations
            else:
                self._show_error(error_msg='Type mismatched in logic operation. Operation between \''
                                           + self._types_table[SUBTOP] +
                                           '\' and \'' + self._types_table[TOP] +
                                           '\' not allowed. {Arithmetic Operation Handler}')
        else:
            if self._types_table[TOP] == 'integer' and self._types_table[SUBTOP] == 'integer':
                self._replace_symbol_table('integer')
            elif self._types_table[TOP] == 'integer' and self._types_table[SUBTOP] == 'real':
                self._replace_symbol_table('real')
            elif self._types_table[TOP] == 'real' and self._types_table[SUBTOP] == 'integer':
                self._replace_symbol_table('real')
            elif self._types_table[TOP] == 'real' and self._types_table[SUBTOP] == 'real':
                self._replace_symbol_table('real')
            else:
                # print(self._types_table)
                self._show_error(error_msg='Type mismatched in arithmetic operation. Operation between \''
                                           + self._types_table[SUBTOP] +
                                           '\' and \'' + self._types_table[TOP] +
                                           '\' not allowed. {Arithmetic Operation Handler}')

    def _assignment_operation_handler(self):
        if self._types_table[TOP] == 'integer' and self._types_table[SUBTOP] == 'integer':
            self._replace_symbol_table()
        elif self._types_table[TOP] == 'integer' and self._types_table[SUBTOP] == 'real':
            self._replace_symbol_table()
        elif self._types_table[TOP] == 'real' and self._types_table[SUBTOP] == 'real':
            self._replace_symbol_table()
        elif self._types_table[TOP] == 'boolean' and self._types_table[SUBTOP] == 'boolean':
            self._replace_symbol_table()
        else:

            self._show_error(error_msg='Type mismatched in assignment operation. Trying to assign \'' +
                                       self._types_table[TOP] + '\' to \'' + self._types_table[SUBTOP] +
                                       '\' {Assignment Operation Handler}')
        self._types_table.clear()

    def _condition_operation_handler(self):
        if self._types_table[TOP] == 'boolean' and self._types_table[SUBTOP] == 'boolean':
            self._replace_symbol_table()
        else:
            self._show_error(
                error_msg='Type mismatched in condition operation. \'' +
                          self._types_table[SUBTOP] + '\' and \'' +
                          self._types_table[TOP] + '\'. {Condition Operation Handler}')
        self._types_table.clear()

    def _procedure_activation_handler(self):

        procedure_arguments = []

        """
        trying to find the correct procedure and its arguments
        keeping only the arguments in the list
        """
        for index, sym in enumerate(reversed(self._arguments)):
            if sym[0] == self._current_procedure[0]:
                procedure_arguments = self._arguments[0:len(self._arguments)-index-1]
                for i, symbol in enumerate(reversed(procedure_arguments)):
                    if symbol[1] == 'procedure':
                        procedure_arguments = procedure_arguments[len(procedure_arguments) - i:]
                        break
                break

        if procedure_arguments:
            if len(procedure_arguments) != len(self._types_table):
                self._show_error(error_msg='Different number of passed arguments'
                                           ' from function declaration during activation'
                                           ' of procedure \'' + self._current_procedure[0] +
                                 '\'. {Procedure Activation Handler}')

            self._types_table = self._types_table[::-1]

            """
            comparing argument to argument and checking its types
            """
            while len(procedure_arguments) > 0:
                symbol_argument = procedure_arguments[-1]
                symbol_calling = self._types_table[-1]
                if (symbol_argument[1] == symbol_calling) or \
                        (symbol_argument[1] == 'real' and symbol_calling == 'integer'):
                    self._types_table.pop()
                    procedure_arguments.pop()
                else:
                    self._show_error(error_msg= 'Type mismatched during calling of the function \'' +
                                     self._current_procedure[0] + '\'. Types: \'' + symbol_calling +
                                     '\' and ' + '\'' + symbol_argument[1] + '\'. {Procedure Activation Handler}')

    def _set_current_procedure(self, token):
        self._current_procedure = [self._get_word(token), 'procedure']

    def _append_arguments(self):
        last_row = False
        for symbol in reversed(self._symbols_table):
            if last_row:
                self._arguments.append(symbol)
                break
            if symbol[0] != MARK:
                self._arguments.append(symbol)
            else:
                last_row = True

    def _show_error(self, token='', error_msg=''):
        if not token:
            error_msg = '[Semantic Error]'\
                        ' | LAST TOKEN READ: \'' + self._get_word(self._last_read)\
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
            self._show_error(False, error_msg='Program syntax is not correct.')
        self._last_read = self.lexical_input[-1]
        if pop:
            return self.lexical_input.pop()
        else:
            return self.lexical_input[-1]

    def _get_word(self, token):
        return token[WORD]

    def _get_line(self, token):
        return token[LINE]

    def _get_classification(self, token):
        return token[CLASSIFICATION]

    def _checker(self, token, type_=WORD, compare_to='', belong_to=[]):
        if belong_to:
            return token and token[type_] in belong_to
        else:
            return token and token[type_] == compare_to

    def start(self):
        # print(self.lexical_input)
        self._program_routine()
        if self.success:
            print('Your program syntax is correct.')


    def _program_routine(self):
        token = self._get_next_token()
        if self._checker(token, type_=WORD, compare_to='program'):
            self._enter_scope()
            token = self._get_next_token()
            if self._checker(token, type_=CLASSIFICATION, compare_to='identifier'):
                self._validate_declaration(token, "program")
                token = self._get_next_token()
                if self._checker(token, type_=WORD, compare_to=';'):
                    # checking now for possible declarations
                    token = self._get_next_token(pop=False)
                    if self._checker(token, type_=WORD, compare_to='var'):
                        self._get_next_token()
                        self._variables_declaration_routine()
                    self._sub_programs_routine()
                    self._compound_command_routine()
                    token = self._get_next_token()
                    if self._checker(token, type_=WORD, compare_to='.'):
                        self.success = True
                    else:
                        self._show_error(token, error_msg='Missing expected \'.\' finishing the program.')

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
            t_type = self._type_routine()
            self._update_symbol_list(t_type)
            token = self._get_next_token()
            if self._checker(token, type_=WORD, compare_to=';'):
                self._variable_declaration_subroutine()
            else:
                self._show_error(token, error_msg='Missing expected \';\'. {Variable_Declaration_Routine}')
        else:
            self._show_error(token, error_msg='Missing expected \':\'. {Variable_Declaration_Routine}')

    def _variable_declaration_subroutine(self):
        if self._identifiers_list_routine(capture_error=False):
            token = self._get_next_token()
            if self._checker(token, type_=WORD, compare_to=':'):
                t_type = self._type_routine()
                self._update_symbol_list(t_type)
                token = self._get_next_token()
                if self._checker(token, type_=WORD, compare_to=';'):
                    self._variable_declaration_subroutine()
                else:
                    self._show_error(token, error_msg='Missing expected \';\'. {Variable_SubDeclaration_Routine}')
            else:
                self._show_error(token, error_msg='Missing expected \':\'. {Variable_SubDeclaration_Routine}')

    def _identifiers_list_routine(self, capture_error=True):
        token = self._get_next_token(pop=False)
        if self._checker(token, type_=CLASSIFICATION, compare_to='identifier'):
            self._validate_declaration(token)
            self._get_next_token()
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
            if self._checker(token, type_=CLASSIFICATION, compare_to='identifier'):
                self._validate_declaration(token)
                self._identifiers_list_subroutine()
            else:
                self._show_error(token, error_msg='Missing expected identifier. {Identifier_SubList_Routine}')

    def _type_routine(self, capture_error=True):
        token = self._get_next_token()
        if not self._checker(token, type_=WORD, compare_to='integer'):
            if not self._checker(token, type_=WORD, compare_to='real'):
                if not self._checker(token, type_=WORD, compare_to='boolean'):
                    self._show_error(token, error_msg='Missing expected type. {Type_Routine}')
                else:
                    return "boolean"
            else:
                return "real"
        else:
            return "integer"

    def _sub_programs_routine(self, capture_error=True):
        if self._sub_program_routine(capture_error=False):
            token = self._get_next_token()
            if self._checker(token, type_=WORD, compare_to=';'):
                self._sub_programs_routine()
            else:
                self._show_error(token, error_msg='Missing expected \';\'. {SubPrograms_Routine}')

    def _sub_program_routine(self, capture_error=True):

        token = self._get_next_token(pop=False)
        if self._checker(token, type_=WORD, compare_to='procedure'):

            self._get_next_token()
            token = self._get_next_token()
            if self._checker(token, type_=CLASSIFICATION, compare_to='identifier'):
                self._validate_declaration(token, "procedure")
                self._enter_scope()
                self._arguments_routines(capture_error=False)
                # print(self._symbols_table)
                token = self._get_next_token()
                if self._checker(token, type_=WORD, compare_to=';'):
                    token = self._get_next_token(pop=False)
                    if self._checker(token, type_=WORD, compare_to='var'):
                        self._get_next_token()
                        self._variables_declaration_routine()
                    else:
                        if not token:
                            self._show_error(token, error_msg='Missing possible expected \'var\'.')
                    self._sub_programs_routine()
                    self._compound_command_routine()
                    self._exit_scope()

                else:
                    self._show_error(token, error_msg='Missing expected \';\'. {SubProgram_Routine}')
            else:
                self._show_error(token, error_msg='Missing expected identifier. {SubProgram_Routine}')
            return True
        else:
            if capture_error:
                self._show_error(token, error_msg='Missing expected \'procedure\'. {SubProgram_Routine}')
            else:
                return False

    def _arguments_routines(self, capture_error=True):
        token = self._get_next_token(pop=False)
        if self._checker(token, type_=WORD, compare_to='('):
            self._get_next_token()
            self._parameters_list_routine()
            self._append_arguments()

            token = self._get_next_token()
            if not self._checker(token, type_=WORD, compare_to=')'):
                self._show_error(token, error_msg='Missing expected \')\'. {Arguments_Routine}')
            return True
        else:
            if capture_error:
                self._show_error(token, error_msg='Missing expected \'(\'. {Arguments_Routine}')
            else:
                return False

    def _parameters_list_routine(self, capture_error=True):

        self._identifiers_list_routine()
        token = self._get_next_token()
        if self._checker(token, type_=WORD, compare_to=':'):
            t_type = self._type_routine()
            self._update_symbol_list(t_type)
            self._parameters_list_subroutine()
        else:
            self._show_error(token, error_msg='Missing expected \':\'. {Parameters_Routine}')

    def _parameters_list_subroutine(self):
        token = self._get_next_token(pop=False)
        if self._checker(token, type_=WORD, compare_to=';'):
            self._get_next_token()
            self._identifiers_list_routine()
            token = self._get_next_token()
            if self._checker(token, type_=WORD, compare_to=':'):
                    t_type = self._type_routine()
                    self._update_symbol_list(t_type)
                    self._parameters_list_subroutine()
            else:
                self._show_error(token, error_msg='Missing expected \':\'. {Parameters_SubRoutine}')

    def _compound_command_routine(self, capture_error=True):
        token = self._get_next_token(pop=False)
        # print(token)
        if self._checker(token, type_=WORD, compare_to='begin'):
            self._get_next_token()
            self._optional_commands_routine()
            token = self._get_next_token()
            if not self._checker(token, type_=WORD, compare_to='end'):
                self._show_error(token, error_msg='Missing expected \'end\'. {Compound_Command_Routine}')

            return True
        else:
            if capture_error:
                self._show_error(token, error_msg='Missing expected \'begin\'. {Compound_Command_Routine}')
            else:
                return False

    def _optional_commands_routine(self, capture_error=True):
        token = self._get_next_token(pop=False)
        if not self._checker(token, type_=WORD, compare_to='end'):
            self._command_list_routine()

    def _command_list_routine(self):
        if self._command_routine(capture_error=False):
            self._command_list_subroutine()

    def _command_list_subroutine(self):
        token = self._get_next_token(pop=False)
        if self._checker(token, type_=WORD, compare_to=';'):
            self._get_next_token()
            self._command_routine()
            self._command_list_subroutine()

    def _command_routine(self, capture_error=True):
        token_temp = self._get_next_token(pop=False)
        if self._checker(token_temp, type_=CLASSIFICATION, compare_to='identifier'):
            self._check_symbol_usage(token_temp)
            self._get_next_token()
            token = self._get_next_token(pop=False)
            if self._checker(token, type_=CLASSIFICATION, compare_to='assignment_operator'):
                self._push_symbol_table(token_temp)
                self._get_next_token()
                self._expression_routine()
                self._assignment_operation_handler()
            elif self._checker(token, type_=WORD, compare_to='('):
                self._set_current_procedure(token_temp)
                self._get_next_token()
                self._list_expression_routine()
                token = self._get_next_token()
                if not self._checker(token, type_=WORD, compare_to=')'):
                    self._show_error(token, error_msg='Missing expected \')\''
                                                      ' closing the expression_list. {Command_Routine}')
                else:
                    self._procedure_activation_handler()

            return True
        elif self._checker(token_temp, type_=WORD, compare_to='if'):
            self._get_next_token()
            self._push_symbol_table(type_='boolean')
            self._expression_routine()
            self._condition_operation_handler()
            token = self._get_next_token()
            if self._checker(token, type_=WORD, compare_to='then'):
                self._command_routine()
                token = self._get_next_token(pop=False)
                if self._checker(token, type_=WORD, compare_to='else'):
                    self._get_next_token()
                    self._command_routine()
            else:
                self._show_error(token, error_msg='Missing expected \'then\'.')
            return True
        elif self._checker(token_temp, type_=WORD, compare_to='while'):
            self._get_next_token()
            self._push_symbol_table(type_='boolean')
            self._expression_routine()
            self._condition_operation_handler()
            token = self._get_next_token()
            if self._checker(token, type_=WORD, compare_to='do'):
                self._command_routine()
            else:
                self._show_error(token, error_msg='Missing expected \'do\'.')
            return True
        elif self._checker(token_temp, type_=WORD, compare_to='do'):
            self._get_next_token()
            self._command_routine()
            token = self._get_next_token()
            if self._checker(token, type_=WORD, compare_to='while'):
                token = self._get_next_token()
                if self._checker(token, type_=WORD, compare_to='('):
                    self._push_symbol_table(type_='boolean')
                    self._expression_routine()
                    self._condition_operation_handler()
                    token = self._get_next_token()
                    if not self._checker(token, type_=WORD, compare_to=')'):
                        self._show_error(token, error_msg='Missing expected \')\'. {Command_Routine}')
                else:
                    self._show_error(token, error_msg='Missing expected \'(\'. {Command_Routine}')
            else:
                self._show_error(token, error_msg='Missing expected \'while\' {Command_Routine}.')
        elif not self._compound_command_routine(capture_error=False):
            if capture_error:
                self._show_error(token_temp, error_msg='Missing expected command.')
            else:
                return False

    def _list_expression_routine(self):
        self._expression_routine()
        self._list_expression_subroutine()

    def _list_expression_subroutine(self):
        token = self._get_next_token(pop=False)
        if self._checker(token, type_=WORD, compare_to=','):
            self._get_next_token()
            self._expression_routine()
            self._list_expression_subroutine()

    def _expression_routine(self):
        self._simple_expression_routine()
        token = self._get_next_token(pop=False)
        if self._checker(token, type_=CLASSIFICATION, compare_to='relational_operator'):
            self._get_next_token()
            self._simple_expression_routine()
            self._relational_operation_handler()

    def _simple_expression_routine(self):
        token = self._get_next_token(pop=False)
        if self._checker(token, type_=CLASSIFICATION, compare_to='sum_operator'):
            self._current_arithmetic_op = self._get_word(token)
            self._get_next_token()
            self._term_routine()
            self._simple_expression_subroutine()
        else:
            self._term_routine()
            self._simple_expression_subroutine()

    def _simple_expression_subroutine(self):
        token = self._get_next_token(pop=False)
        if self._checker(token, type_=CLASSIFICATION, compare_to='sum_operator'):
            self._current_arithmetic_op = self._get_word(token)
            self._get_next_token()
            self._term_routine()
            self._arithmetic_operation_handler()
            self._simple_expression_subroutine()

    def _term_routine(self):
        self._factor_routine()
        self._term_subroutine()

    def _term_subroutine(self):
        token = self._get_next_token(pop=False)
        if self._checker(token, type_=CLASSIFICATION, compare_to='multiply_operator'):
            self._current_arithmetic_op = self._get_word(token)
            self._get_next_token()
            self._factor_routine()
            self._arithmetic_operation_handler()
            self._term_subroutine()

    def _factor_routine(self):
        token_temp = self._get_next_token()
        if self._checker(token_temp, type_=CLASSIFICATION, compare_to='identifier'):
            self._check_symbol_usage(token_temp)
            self._push_symbol_table(token_temp)
            token = self._get_next_token(pop=False)
            if self._checker(token, type_=WORD, compare_to='('):
                self._get_next_token()
                self._list_expression_routine()
                token = self._get_next_token()
                if not self._checker(token, type_=WORD, compare_to=')'):
                    self._show_error(token, error_msg='Missing expected \')\''
                                                      ' closing the expression_list. {Factor_Routine}')
        elif self._checker(token_temp, type_=WORD, compare_to='('):
            self._expression_routine()
            token = self._get_next_token()
            if not self._checker(token, type_=WORD, compare_to=')'):
                self._show_error(token, error_msg='Missing expected \')\''
                                                  ' closing the expression_list. {Factor_Routine}')
        elif self._checker(token_temp, type_=WORD, compare_to='not'):
            self._factor_routine()
        else:
            if not self._checker(token_temp, type_=CLASSIFICATION, belong_to=['integer', 'real']):
                if not self._checker(token_temp, type_=WORD, belong_to=['true', 'false']):
                    self._show_error(token_temp, error_msg='Missing expected factor.')
            self._push_symbol_table(token_temp, self._get_classification(token_temp))
