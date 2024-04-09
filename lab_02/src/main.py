from color import *
from grammar import Grammar, reedGrammarFromFile


MSG = f"""
    {YELLOW}\tМеню\n
    {YELLOW}1.{BASE}  Исходная грамматика для удаления левой рекурсии;
    {YELLOW}2.{BASE}  Грамматика после устранения левой рекурсии и левой факторизации;

    {YELLOW}0.{BASE}  Выход.\n
    {GREEN}Выбор:{BASE} """


INPUT_FILE_NAME = "../data/left_recursion_1.txt"
OUTPUT_FILE_NAME = "../data/output_left_recursion.txt"


def inputOption():
    try:
        option = int(input(MSG))
    except:
        option = -1
    
    if option < 0 or option > 6:
        print("%s\nОжидался ввод целого числа от 0 до 2%s" %(RED, BASE))

    return option


def main():
    option = -1
    while option != 0:
        option = inputOption()
        match option:
            case 1:
                grammar: Grammar = reedGrammarFromFile(INPUT_FILE_NAME)
                grammar.printGrammar()
            case 2:
                grammar: Grammar = reedGrammarFromFile(INPUT_FILE_NAME)
                grammar.removeLeftRecursion()
                grammar.printGrammar()


if __name__ == '__main__':
    main()
