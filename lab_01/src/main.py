from regularExpression import checkRegex, convertToDesiredFormat
from parseTree import ParseTree
from dfa import DFA
from minDfa import MinDFA


SHOW_GRAPHS = False
REGEX_DEFAULT = True

def inputRegex(takeDefault: bool = False) -> str | None:
    if takeDefault:
        regex = "(a|b)*abb"
        # regex = "((abba)|(baab)|(baba)|(abab)|(bb)|(aa))*b((abba)|(baab)|(baba)|(abab)|(bb)|(aa))*"
    else:
        regex = input("Введите регулярное выражение: ")

    regex = regex.replace(" ", "").lower()
    try:
        checkRegex(regex)
    except ValueError as exc:
        print(exc, "\n")
        return None

    regex = convertToDesiredFormat(regex)
    print(f"\nОбработанное регулярное выражение:\n{regex}")

    return regex

def main():
    regex = inputRegex(takeDefault=REGEX_DEFAULT)
    if regex is None:
        return

    parseTree = ParseTree(regex)
    parseTree.printTree()
    parseTree.buildGraph(view=SHOW_GRAPHS)
    
    dfa = DFA(parseTree)
    dfa.printFirstposLastpos()
    dfa.printFollowpos()
    dfa.printDFA()
    dfa.buildFirstposLastposGraph(view=SHOW_GRAPHS)
    dfa.buildFollowposGraph(view=SHOW_GRAPHS)
    dfa.buildDFAGraph(view=SHOW_GRAPHS)

    minDFA = MinDFA(dfa)
    minDFA.printGroupList()
    minDFA.printMinDFA()
    minDFA.buildMinDFAGraph(view=SHOW_GRAPHS)

if __name__ == '__main__':
    main()
