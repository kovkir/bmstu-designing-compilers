from regularExpression import checkRegex, convertToDesiredFormat
from parseTree import ParseTree
from dfa import DFA

SHOW_GRAPHS = False

def main():
    # regex = input("Введите регулярное выражение: ")
    regex = "(a|b)*abb"

    regex = regex.replace(" ", "").lower()
    checkRegex(regex)
    regex = convertToDesiredFormat(regex)

    parseTree = ParseTree(regex)
    parseTree.printTree()
    parseTree.buildGraph(view=SHOW_GRAPHS)
    
    dfa = DFA(parseTree)
    dfa.buildFirstposLastposGraph(view=SHOW_GRAPHS)
    dfa.buildFollowposGraph(view=SHOW_GRAPHS)

if __name__ == '__main__':
    main()
