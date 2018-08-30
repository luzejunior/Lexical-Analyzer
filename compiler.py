from lexical_analyzer.lexical import Lexical


def main():
    lexical = Lexical('program.txt')
    lexical.analyze()

    print(lexical.get_list())


if __name__ == "__main__":
    main()
