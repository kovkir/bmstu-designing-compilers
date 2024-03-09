from regularExpression import checkRegex, convertToDesiredFormat
from parseTree import ParseTree


def main():
    # regex = input("Введите регулярное выражение: ")
    regex = "(a|b)*abb"

    regex = regex.replace(" ", "").lower()
    checkRegex(regex)
    regex = convertToDesiredFormat(regex)

    parseTree = ParseTree(regex)
    parseTree.printTree()
    parseTree.buildGraph()


if __name__ == '__main__':
    main()