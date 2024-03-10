import graphviz
from parseTree import ParseTree, Node


class DFA():
    def __init__(self, parseTree: ParseTree):
        self.root = parseTree.root
        self.followpos = parseTree.followpos
        self.__completeTree(self.root)

    def buildFirstposLastposGraph(self, view: bool = False) -> None:
        dot = graphviz.Digraph(
            comment='Значения функций firstpos и lastpos в узлах синтаксического дерева для регулярного выражения'
        )
        self.__addNodeToGraph(self.root, dot)
        dot.render('../docs/firstpos-lastpos.gv', view=view)

    def buildFollowposGraph(self, view: bool = False) -> None:
        dot = graphviz.Digraph(
            comment='Ориентированный граф для функции followpos'
        )
        for i in self.followpos:
            dot.node(str(i))
            for j in self.followpos[i]:
                dot.edge(str(i), str(j))

        dot.render('../docs/followpos.gv', view=view)

    def __completeTree(self, node: Node) -> None:
        if node is not None:
            if node.leftChild:
                self.__completeTree(node.leftChild)
            if node.rightChild:
                self.__completeTree(node.rightChild)

            node.nullable = self.__calcNullable(node)
            node.firstpos = self.__calcFirstpos(node)
            node.lastpos = self.__calcLastpos(node)

            if node.value == '.':
                for i in node.leftChild.lastpos:
                    for j in node.rightChild.firstpos:
                        self.followpos[i].add(j)
            elif node.value == '*':
                for i in node.lastpos:
                    for j in node.firstpos:
                        self.followpos[i].add(j)

    def __calcNullable(self, node: Node) -> bool:
        if node.value == '|':
            nullable = \
                node.leftChild.nullable or \
                node.rightChild.nullable
        elif node.value == '.':
            nullable = \
                node.leftChild.nullable and \
                node.rightChild.nullable
        elif node.value == '*':
            nullable = True
        else:
            nullable = False

        return nullable

    def __calcFirstpos(self, node: Node) -> set:
        if node.value == '|':
            firstpos = node.leftChild.firstpos.union(node.rightChild.firstpos)
        elif node.value == '.':
            firstpos = \
                node.leftChild.firstpos.union(node.rightChild.firstpos) \
                if node.leftChild.nullable else node.leftChild.firstpos
        elif node.value == '*':
            firstpos = node.leftChild.firstpos
        else:
            firstpos = {node.letterNumber}

        return firstpos

    def __calcLastpos(self, node: Node) -> set:
        if node.value == '|':
            lastpos = node.leftChild.lastpos.union(node.rightChild.lastpos)
        elif node.value == '.':
            lastpos = \
                node.leftChild.lastpos.union(node.rightChild.lastpos) \
                if node.rightChild.nullable else node.rightChild.lastpos
        elif node.value == '*':
            lastpos = node.leftChild.lastpos
        else:
            lastpos = {node.letterNumber}

        return lastpos
    
    def __addNodeToGraph(self, node: Node, dot: graphviz.Digraph) -> None:
        if node is not None:
            if node.leftChild:
                self.__addNodeToGraph(node.leftChild, dot)
                dot.edge(str(node.nodeNumber), str(node.leftChild.nodeNumber))

            dot.node(
                name=str(node.nodeNumber), 
                label=f"{node.firstpos}  {node.value}{f", {node.letterNumber}" if node.letterNumber else ""}  {node.lastpos}"
            )

            if node.rightChild:
                self.__addNodeToGraph(node.rightChild, dot)
                dot.edge(str(node.nodeNumber), str(node.rightChild.nodeNumber))
