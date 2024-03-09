import graphviz
from pythonds.basic.stack import Stack


class Node:
    value: str
    leftChild = None
    rightChild = None

    def __init__(self, nodeNumber, letterNumber=None, value=None, leftNode=None, rightNode=None):
        self.nodeNumber = nodeNumber
        self.letterNumber = letterNumber
        self.value = value
        self.leftChild = leftNode
        self.rightChild = rightNode


class ParseTree():
    def __init__(self, regex: str):
        self.root = self.__buildTree(regex)

    def printTree(self):
        self.__printNode(self.root)

    def buildGraph(self):
        dot = graphviz.Digraph(comment='Синтаксическое дерево для регулярного выражения')

        self.__addNodeToGraph(self.root, dot)
        dot.render('../docs/parse-tree.gv', view=False)
    
    def __buildTree(self, regex: str):
        stack = Stack()
        nodeNumber = 1
        letterNumber = 0
        node = Node(nodeNumber=nodeNumber)

        for symbol in regex:
            if stack.isEmpty():
                nodeNumber += 1
                root = Node(leftNode=node, nodeNumber=nodeNumber)
                stack.push(root)

            if symbol == '(':
                nodeNumber += 1
                node.leftChild = Node(nodeNumber=nodeNumber)
                stack.push(node)
                node = node.leftChild

            elif symbol not in ['.', '|', '*', ')']:
                letterNumber += 1
                node.value = symbol
                node.letterNumber = letterNumber
                node = stack.pop()

            elif symbol in ['.', '|']:
                if node.value is not None:
                    node = stack.pop()
                nodeNumber += 1
                node.value = symbol
                node.rightChild = Node(nodeNumber=nodeNumber)
                stack.push(node)
                node = node.rightChild

            elif symbol == '*':
                if node.value is not None:
                    node = stack.pop()
                node.value = symbol

            elif symbol == ')':
                node = stack.pop()
        
        return root
    
    def __printNode(self, node: Node, end: str = ' '):
        if node is not None:
            if node.leftChild:
                print('(', end=end)
                self.__printNode(node.leftChild)

            print(node.value, end=end)

            if node.rightChild:
                self.__printNode(node.rightChild)
                print(')', end=end)
            elif node.leftChild: # для оператора *
                print(')', end=end)

    def __addNodeToGraph(self, node: Node, dot: graphviz.Digraph):
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