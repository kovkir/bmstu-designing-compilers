import subprocess

from color import *
from grammar import Grammar, reedGrammarFromFile


MENU = f"""
    {YELLOW}\tМеню\n
    {YELLOW}1.{BASE}  Исходная грамматика;
    {YELLOW}2.{BASE}  Грамматика после устранения левой рекурсии;
    {YELLOW}3.{BASE}  Грамматика после устранения левой факторизации;
    {YELLOW}4.{BASE}  Грамматика после устранения левой рекурсии и левой факторизации;

    {YELLOW}0.{BASE}  Выход.\n
    {GREEN}Выбор:{BASE} """


SIZE_MENU = 4
OUTPUT_FILE_NAME = "../data/result.txt"


def inputOption(minOptions: int, maxOptions: int, msg: str):
    try:
        option = int(input(msg))
    except:
        option = -1
    else:
        if option < minOptions or option > maxOptions:
            option = -1
    
    if option == -1:
        print(f"{RED}\nОжидался ввод целого числа от {minOptions} до {maxOptions}{BASE}")

    return option


def chooseInputFile() -> str:
    with open("temp.txt", "w") as f:
        subprocess.run(["ls", "../data"], stdout=f)

    with open("temp.txt") as f:
        fileNames = [line[:-1] for line in f.readlines()]

    subprocess.run(["rm", "temp.txt"])

    msg = f"\n\t{YELLOW}Входные файлы:{BASE}\n\n"
    for i in range(len(fileNames)):
        msg += f"    {YELLOW}{i + 1}.{BASE}  {fileNames[i]};\n"
    msg += f"\n    {GREEN}Выбор:{BASE} "

    option = -1
    while option == -1:
        option = option = inputOption(
            minOptions=1,
            maxOptions=len(fileNames), 
            msg=msg,
        )
    
    return f"../data/{fileNames[option - 1]}"


def main():
    inputFile = chooseInputFile()
    option = -1
    while option != 0:
        option = inputOption(
            minOptions=0,
            maxOptions=SIZE_MENU, 
            msg=MENU,
        )
        match option:
            case 1:
                grammar: Grammar = reedGrammarFromFile(inputFile)
                grammar.printGrammar()
            case 2:
                grammar: Grammar = reedGrammarFromFile(inputFile)
                grammar.removeLeftRecursion()
                grammar.printGrammar()
                grammar.createFileFromGrammar(OUTPUT_FILE_NAME)
            case 3:
                grammar: Grammar = reedGrammarFromFile(inputFile)
                grammar.removeLeftFactorization()
                grammar.printGrammar()
                grammar.createFileFromGrammar(OUTPUT_FILE_NAME)
            case 4:
                grammar: Grammar = reedGrammarFromFile(inputFile)
                grammar.removeLeftRecursion()
                grammar.removeLeftFactorization()
                grammar.printGrammar()
                grammar.createFileFromGrammar(OUTPUT_FILE_NAME)


if __name__ == '__main__':
    main()
