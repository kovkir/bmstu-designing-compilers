import graphviz
from dfa import DFA


class MinDFA():
    def __init__(self, dfa: DFA):
        self.alphabet = "qwertyuiopasdfghjklzxcvbnm"
        self.dStates = dfa.dStates

        self.groupList = self.__minimizeNumberOfStates(dfa.finalStates.copy())
        self.initialState = self.__findInitialState(dfa.initialState)
        self.finalStates = self.__findFinalStates(dfa.finalStates)
        self.minDstates = self.__findMinDstates()
        
    def printGroupList(self) -> None:
        print("Группы состояний, полученные после минимизации ДКА алгоритмом Хопкрофта:")
        for i in range(len(self.groupList)):
            print(f"{i + 1}: {self.groupList[i]}")
        print()

    def printMinDFA(self) -> None:
        print("Минимизированный ДКА алгоритмом Хопкрофта:")
        for key, value in self.minDstates.items():
            print(f"{key}: {value}")
        print()

    def buildMinDFAGraph(self, view: bool = False) -> None:
        dot = graphviz.Digraph(
            comment='Минимизированный ДКА алгоритмом Хопкрофта'
        )
        dot.node("", peripheries="0")
        dot.edge("", self.initialState, label="start")

        for state in self.minDstates.keys():
            if state in self.finalStates:
                linesCount = '2'
            else:
                linesCount = '1'

            dot.node(state, peripheries=linesCount)
            for key, value in self.minDstates[state].items():
                dot.edge(state, value, label=key, constraint='true')

        dot.render('../docs/min-dfa.gv', view=view)

    def __minimizeNumberOfStates(self, finalStates: list) -> list:
        nonFinalStates = []
        for state in self.dStates.keys():
            if state not in finalStates:
                nonFinalStates.append(state)

        groupList = [nonFinalStates, finalStates]
        groupListLen = len(groupList)
        while True:
            for group in groupList:
                newGroup = []
                groupDict = {}
                for state in group:
                    for letter in self.alphabet:
                        nextState = self.dStates[state].get(letter)
                        firstGroupIndex = groupDict.get(letter)
                        groupIndex = \
                            self.__getGroupIndexOfState(nextState, groupList)
                        if firstGroupIndex is None:
                            groupDict[letter] = groupIndex
                        elif firstGroupIndex != groupIndex:
                            newGroup.append(state)
                            group.remove(state)
                            break

                if len(newGroup):
                    groupList.append(newGroup)

            if groupListLen != len(groupList):
                groupListLen = len(groupList)
            else:
                break

        return groupList
    
    def __findInitialState(self, dfaInitialState: str) -> str:
        for group in self.groupList:
            if dfaInitialState in group:
                return group[0]
            
    def __findFinalStates(self, dfaFinalStates: list) -> list:
        finalStates = []
        for group in self.groupList:
            state = group[0]
            if state in dfaFinalStates:
                finalStates.append(state)
        
        return finalStates
    
    def __findMinDstates(self) -> dict:
        minDstates = {}
        for group in self.groupList:
            state = group[0]
            minDstates[state] = {}
            for letter, nextState in self.dStates[state].items():
                groupIndex = self.__getGroupIndexOfState(nextState, self.groupList)
                minDstates[state][letter] = self.groupList[groupIndex][0]
        
        return minDstates

    def __getGroupIndexOfState(self, nextState: str | None, groupList: list) -> int:
        if nextState is None:
            return -1
        
        for i in range(len(groupList)):
            for state in groupList[i]:
                if state == nextState:
                    return i
    