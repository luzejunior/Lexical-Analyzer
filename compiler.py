from lexical_analyzer.lexical import Lexical
from syntactic_analyzer.syntactic import Syntactic


def main():
    lexical = Lexical('program.txt')
    lexical.analyze()
    syntactic = Syntactic(lexical.get_list())
    syntactic.test()



if __name__ == "__main__":
    main()
