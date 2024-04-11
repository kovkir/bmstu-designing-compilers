from color import *
from grammar import Grammar, reedGrammarFromFile


MSG = f"""
    {YELLOW}\tМеню\n
    {YELLOW}1.{BASE}  Исходная грамматика;
    {YELLOW}2.{BASE}  Грамматика после устранения левой рекурсии;
    {YELLOW}3.{BASE}  Грамматика после устранения левой факторизации;
    {YELLOW}4.{BASE}  Грамматика после устранения левой рекурсии и левой факторизации;

    {YELLOW}0.{BASE}  Выход.\n
    {GREEN}Выбор:{BASE} """


# INPUT_FILE_NAME = "../data/left_recursion_1.txt"
INPUT_FILE_NAME = "../data/left_factorization.txt"
OUTPUT_FILE_NAME = "../data/result.txt"


def inputOption(maxOptions):
    try:
        option = int(input(MSG))
    except:
        option = -1
    
    if option < 0 or option > maxOptions:
        print(f"{RED}\nОжидался ввод целого числа от 0 до {maxOptions}{BASE}")

    return option


def main():
    option = -1
    while option != 0:
        option = inputOption(4)
        match option:
            case 1:
                grammar: Grammar = reedGrammarFromFile(INPUT_FILE_NAME)
                grammar.printGrammar()
            case 2:
                grammar: Grammar = reedGrammarFromFile(INPUT_FILE_NAME)
                grammar.removeLeftRecursion()
                grammar.printGrammar()
            case 3:
                grammar: Grammar = reedGrammarFromFile(INPUT_FILE_NAME)
                grammar.removeLeftFactorization()
                grammar.printGrammar()
            case 4:
                grammar: Grammar = reedGrammarFromFile(INPUT_FILE_NAME)
                grammar.removeLeftRecursion()
                grammar.removeLeftFactorization()
                grammar.printGrammar()


if __name__ == '__main__':
    main()
