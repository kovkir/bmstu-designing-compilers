from color import *
from regularExpression import convertRegexToDesiredFormat
from parseTree import ParseTree
from dfa import DFA
from minDfa import MinDFA
from chain import inputСhainСheckСorrespondence


MSG = f"""
    {YELLOW}\tМеню\n
    {YELLOW}1.{BASE}  Синтаксическое дерево для регулярного выражения;
    {YELLOW}2.{BASE}  Значения функций firstpos и lastpos в узлах синтаксического дерева;
    {YELLOW}3.{BASE}  Ориентированный граф для функции followpos;
    {YELLOW}4.{BASE}  ДКА для регулярного выражения;
    {YELLOW}5.{BASE}  Минимизированный ДКА алгоритмом Хопкрофта;
    {YELLOW}6.{BASE}  Проверка входной цепочки на соответсвие регулярному выражению;

    {YELLOW}0.{BASE}  Выход.\n
    {GREEN}Выбор:{BASE} """


def inputOption():
    try:
        option = int(input(MSG))
    except:
        option = -1
    
    if option < 0 or option > 6:
        print("%s\nОжидался ввод целого числа от 0 до 6%s" %(RED, BASE))

    return option


def main():
    regex = input(f"\n{BLUE}Введите регулярное выражение: {BASE}")
    # regex = "(a|b)*abb"
    # regex = "((abba)|(baab)|(baba)|(abab)|(bb)|(aa))*b((abba)|(baab)|(baba)|(abab)|(bb)|(aa))*"
    convertedRegex = convertRegexToDesiredFormat(regex)
    if convertedRegex is None:
        return

    parseTree = ParseTree(convertedRegex)
    parseTree.printTree()
    
    dfa = DFA(parseTree)
    dfa.printFirstposLastpos()
    dfa.printFollowpos()
    dfa.printDFA()

    minDFA = MinDFA(dfa)
    minDFA.printGroupList()
    minDFA.printMinDFA()

    option = -1
    while option != 0:
        option = inputOption()
        match option:
            case 1:
                parseTree.buildGraph(view=True)
            case 2:
                dfa.buildFirstposLastposGraph(view=True)
            case 3:
                dfa.buildFollowposGraph(view=True)
            case 4:
                dfa.buildDFAGraph(view=True)
            case 5:
                minDFA.buildMinDFAGraph(view=True)
            case 6:
                inputСhainСheckСorrespondence(regex, minDFA)


if __name__ == '__main__':
    main()
