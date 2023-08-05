from rhme.hme_parser.grammar import yacc as yacc
from rhme.hme_parser.grammar import lex as lex
from rhme.hme_parser import base_grammar as base_grammar
from rhme.hme_parser import check_grammar_lex as check_grammar_lex
from rhme.helpers.exceptions import GrammarError, LexicalError, SintaticError
from rhme import helpers
import numpy as np

class CheckSintax():
    def __init__(self):
        self.__first_error = True
        self.latex_string=""
        self.latex=""
        self.latex_list=""
        self.attempts=0
        self.index=0
        self.token_errors_history=[]
        self.yacc_error_list=None
        self.symbols_attempts_in_lex=[] # ?
        self.grammar_errors_history=[]
        self.pure_yacc_errors=[]

    def __locate_grammar_error(self):
        helpers.debug("\n[check_grammar_sintax.py] __locate_grammar_error() | Locating all errors and creating a data structure.")

        yacc_error_list = self.yacc_error_list.copy()
        latex = self.latex.copy()
        grammar_errors = []
        grammar_errors_history = []
        

        helpers.debug("[check_grammar_sintax.py] __locate_grammar_error() | Errors:")
        helpers.debug(yacc_error_list)

        for error in yacc_error_list:

            helpers.debug("[check_grammar_sintax.py] __locate_grammar_error() | ...for()")
            if error['value'] != None:

                helpers.debug("[check_grammar_sintax.py] __locate_grammar_error() | ...for() value not none")

                latex_error = self.latex_string[error['lexpos']::]
                latex_error_token = error['value']
                latex_error_pos = error['lexpos']

                count = 0
                count_list = 0

                helpers.debug("\n[check_grammar_sintax.py] __locate_grammar_error() | LATEX: ")
                helpers.debug(latex)

                helpers.debug("\n[check_grammar_sintax.py] __locate_grammar_error() | before for() ")

                for symbol in latex:
                    helpers.debug("[check_grammar_sintax.py] __locate_grammar_error() | \
                    ...for() symbol['label']: %s " % symbol['label'])

                    helpers.debug("[check_grammar_sintax.py] __locate_grammar_error() | \
                    ...for() latex_error_token['label']: %s " % latex_error_token)

                    helpers.debug("[check_grammar_sintax.py] __locate_grammar_error() | count: %d" % count)
                    helpers.debug("[check_grammar_sintax.py] __locate_grammar_error() | latex_error_pos: %d" % latex_error_pos)

                    if symbol['label'] == latex_error_token and count == latex_error_pos:
                        helpers.debug("[check_grammar_sintax.py] __locate_grammar_error() | \
                        ...for() found error position: %d " % count)
                        grammar_errors.append({
                            'pos': latex_error_pos,
                            'pos_list': count_list,
                            'label': symbol['label'],
                            'prediction': symbol['prediction'],
                            'attempts': [latex_error_pos]
                        })
                        grammar_errors_history.extend(grammar_errors)
                        break

                    count += len(symbol['label'])
                    count_list += 1

            else:
                helpers.debug("Use automata to fix")
                continue

        return grammar_errors, grammar_errors_history

    def check_correct_grammar(self):
        helpers.debug("\n---------------------------------------------------------------------------------")
        helpers.debug("[check_grammar_sintax.py] check_correct_grammar()")
        helpers.debug("[check_grammar_sintax.py] check_correct_grammar() | attempts: %s" % self.attempts)

        second_yacc_error_list = None
        grammar_errors = []

        if not self.yacc_error_list and self.__first_error and self.attempts < 3:
            helpers.debug("[check_grammar_sintax.py] check_correct_grammar() | There's no previous errors")
            yacc_error_list = yacc.LatexParse(self.latex_string)

            helpers.debug("[check_grammar_sintax.py] check_correct_grammar() | error: ")
            helpers.debug(yacc_error_list)

            self.pure_yacc_errors.append(yacc_error_list)
            self.yacc_error_list = yacc_error_list

            if self.yacc_error_list:

                # added
                if yacc_error_list[0]['lexpos'] == None: # EOF ? 
                    yacc_error_list[0].update({'lexpos': len(self.latex_string) -1})
                    yacc_error_list[0].update({'value': self.latex_string[-1]})

                grammar_errors, grammar_errors_history = self.__locate_grammar_error()
                self.grammar_errors_history.extend(grammar_errors_history)

                self.__first_error = False

                self.__attempt_to_fix_error(grammar_errors)

        elif self.yacc_error_list and not self.__first_error and self.attempts < 3:
            helpers.debug("\n[check_grammar_sintax.py] check_correct_grammar() | There were errors before\n")
            helpers.debug("\n[check_grammar_sintax.py] check_correct_grammar() | Before check for lexical errors again")
            helpers.debug("\n................FIND LEXICAL ERRORS................")
            self.__find_lexical_errors()
            helpers.debug("...................................................")

            helpers.debug("\n[check_grammar_sintax.py] check_correct_grammar() | After check for lexical errors again")

            helpers.debug("[check_grammar_sintax.py] check_correct_grammar() | Before check for syntactic errors again")
            second_yacc_error_list = yacc.LatexParse(self.latex_string)
            helpers.debug("[check_grammar_sintax.py] check_correct_grammar() | After check for syntactic errors again")

            self.pure_yacc_errors.append(second_yacc_error_list)
            helpers.debug("[check_grammar_sintax.py] check_correct_grammar() | After updating pure_yacc_errors")

            if second_yacc_error_list:

                if second_yacc_error_list[0]['lexpos'] == None: # EOF ? 
                    second_yacc_error_list[0].update({'lexpos': len(self.latex_string) -1})
                    second_yacc_error_list[0].update({'value': self.latex_string[-1]})
                    # second_yacc_error_list.reverse()
                    # second_yacc_error_list.pop()
                    # second_yacc_error_list.reverse()

                helpers.debug("[check_grammar_sintax.py] check_correct_grammar() | Syntactic errors: ")
                helpers.debug(second_yacc_error_list)

                self.yacc_error_list = second_yacc_error_list
                helpers.debug("[check_grammar_sintax.py] check_correct_grammar() | Syntactic errors self.yacc_error_list: ")
                helpers.debug(self.yacc_error_list)

                helpers.debug("[check_grammar_sintax.py] check_correct_grammar() | Before locating grammar error ")
                grammar_errors, grammar_errors_history = self.__locate_grammar_error()
                helpers.debug("[check_grammar_sintax.py] check_correct_grammar() | After locating grammar error ")
                helpers.debug("[check_grammar_sintax.py] check_correct_grammar() | Grammars errors ")
                helpers.debug(grammar_errors)

                helpers.debug("[check_grammar_sintax.py] check_correct_grammar() | Before trying to fix grammar error ")
                self.__attempt_to_fix_error(grammar_errors)
                helpers.debug("[check_grammar_sintax.py] check_correct_grammar() | After trying to fix grammar error ")

            helpers.debug("[check_grammar_sintax.py] check_correct_grammar() | NO pure_yacc_errors")

        elif self.yacc_error_list and self.attempts >= 3:
            helpers.debug("\n[check_grammar_sintax.py] check_correct_grammar() | GrammarError")

            raise GrammarError({
                'error': grammar_errors,
                'latex': self.latex,
                'latex_list': self.latex_list,
                'grammar_errors_history': self.grammar_errors_history,
                'latex_string': self.latex_string,
                'pure_yacc_errors_list': self.pure_yacc_errors
            })

        helpers.debug("[check_grammar_sintax.py] check_correct_grammar() | Returning...")
        return self.latex_string, grammar_errors, self.grammar_errors_history, self.latex, self.latex_list

    def __find_lexical_errors(self):
        cgl = check_grammar_lex.CheckLex()
        cgl.latex_string = self.latex_string
        cgl.latex = self.latex
        cgl.latex_list = self.latex_list
        cgl.attempts = 0

        new_latex_string, token_errors, token_errors_history, latex, latex_list = cgl.check_correct_lex()

        # Se chegou aqui é porque conseguiu solucionar
        self.latex_string = new_latex_string
        self.token_errors_history = token_errors_history
        self.latex = latex
        self.latex_list = latex_list

        if token_errors:
            for token in token_errors_history:
                self.symbols_attempts_in_lex.extend(token['attempts'])

    def __attempt_to_fix_error(self, grammar_errors):
        helpers.debug('[check_grammar_sintax.py] __attempt_to_fix_error()')
        bg = base_grammar.BaseGrammar()
        fix_attempts = self.symbols_attempts_in_lex.copy() # ?? 
        fix_attempts.extend(self.grammar_errors_history) # ??
        updated_latex_string, updated_grammar_error_list, self.index = bg.correct_grammar_lex(grammar_errors, self.latex, self.latex_list, self.index, fix_attempts)

        self.yacc_error_list = updated_grammar_error_list
        if updated_grammar_error_list:
            self.grammar_errors_history.extend(updated_grammar_error_list)

        if updated_latex_string:
            self.latex_string = updated_latex_string
            self.attempts += 1
            return self.check_correct_grammar()
