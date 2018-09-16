from lexical_analyzer.lexical import Lexical
from syntactic_analyzer.syntactic import Syntactic


def main():
    lexical = Lexical('program.txt')
    lexical.analyze()
    print(lexical.get_list())
    syntactic = Syntactic(lexical.get_list())
    syntactic.start()


if __name__ == "__main__":
    main()
