import graphviz
from pythonds.basic.stack import Stack
from color import *
from regularExpression import findClosingBracketIndex


class Node:
    def __init__(self, leftNode=None, rightNode=None) -> None:
        self.nodeNumber = None
        self.letterNumber = None
        self.value = None
        self.leftChild = leftNode
        self.rightChild = rightNode

        self.nullable = None
        self.firstpos = set()
        self.lastpos = set()


class ParseTree():
    def __init__(self, regex: str) -> None:
        self.followpos = dict()
        self.letterNumbers = dict()
        self.root = self.__buildTree(regex)

    def printTree(self) -> None:
        print(f"{GREEN}Синтаксическое дерево для регулярного выражения:{BASE}")
        self.__printNode(self.root)
        print("\n")

    def buildGraph(self, view: bool = False) -> None:
        dot = graphviz.Digraph(
            comment='Синтаксическое дерево для регулярного выражения'
        )
        self.__addNodeToGraph(self.root, dot)
        dot.render('../docs/parse-tree.gv', view=view)
    
    def __buildTree(self, regex: str) -> Node:
        root, _, _ = self.__buildTreeRecursion(
            regex=regex,
            nodeNumber=0,
            letterNumber=0
        )
        if root.value is None:
            root = root.leftChild

        return root
    
    def __buildTreeRecursion(
            self, 
            regex: str, 
            nodeNumber: int, 
            letterNumber: int,
        ) -> list[Node, int, int]:
        stackNode = Stack()
        node = Node()

        i = 0
        while i < len(regex):
            symbol = regex[i]
            if stackNode.isEmpty():
                root = Node(leftNode=node)
                stackNode.push(root)

            if symbol == '(':
                closingBracketIndex = findClosingBracketIndex(regex, i)
                subtreeRoot, nodeCount, letterCount = self.__buildTreeRecursion(
                    regex=regex[i + 1: closingBracketIndex],
                    nodeNumber=nodeNumber,
                    letterNumber=letterNumber
                )
                if subtreeRoot.value is None:
                    subtreeRoot = subtreeRoot.leftChild
                node.leftChild = subtreeRoot.leftChild
                node.rightChild = subtreeRoot.rightChild
                node.value = subtreeRoot.value
                node.nodeNumber = subtreeRoot.nodeNumber
                nodeNumber = nodeCount
                letterNumber = letterCount
                i = closingBracketIndex
                node = stackNode.pop()
                
            elif symbol not in ['.', '|', '*', ')']:
                nodeNumber += 1
                letterNumber += 1
                node.nodeNumber = nodeNumber
                node.letterNumber = letterNumber
                node.value = symbol
                self.letterNumbers[letterNumber] = symbol
                self.followpos[letterNumber] = set()
                node = stackNode.pop()

            elif symbol in ['.', '|']:
                if node.value is not None:
                    node = stackNode.pop()
                nodeNumber += 1
                node.nodeNumber = nodeNumber
                node.value = symbol
                node.rightChild = Node()
                stackNode.push(node)
                node = node.rightChild

            elif symbol == '*':
                if node.value is not None:
                    node = stackNode.pop()
                nodeNumber += 1
                node.nodeNumber = nodeNumber
                node.value = symbol
                node.nullable = True

            i += 1
        
        return root, nodeNumber, letterNumber
    
    def __printNode(self, node: Node, end: str = ' ') -> None:
        if node is not None:
            if node.leftChild:
                print('(', end=end)
                self.__printNode(node.leftChild)

            print(node.value, end=end)

            if node.rightChild:
                self.__printNode(node.rightChild)
                print(')', end=end)
            elif node.leftChild: # для оператора '*'
                print(')', end=end)

    def __addNodeToGraph(self, node: Node, dot: graphviz.Digraph) -> None:
        if node is not None:
            if node.leftChild:
                self.__addNodeToGraph(node.leftChild, dot)
                dot.edge(str(node.nodeNumber), str(node.leftChild.nodeNumber))

            dot.node(
                name=str(node.nodeNumber), 
                label=f"{node.value}{f", {node.letterNumber}" if node.letterNumber else ""}"
            )

            if node.rightChild:
                self.__addNodeToGraph(node.rightChild, dot)
                dot.edge(str(node.nodeNumber), str(node.rightChild.nodeNumber))
