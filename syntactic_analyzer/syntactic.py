WORD = 0
CLASSIFICATION = 1


class Syntactic:
    def __init__(self, lexical_input=['token','classification',1]):
        self.lexical_input = lexical_input[::-1]

    def _get_next_token(self):
        if len(self.lexical_input) == 0:
            return False
        return self.lexical_input.pop()

    def _get_word(self, token=[]):
        return token[WORD]

    def _get_classification(self, token=[]):
        return token[CLASSIFICATION]

    def test(self):

        while True:
            token = self._get_next_token()
            if not token:
                break

            print(self._get_classification(token) + ' ' + self._get_word(token))




