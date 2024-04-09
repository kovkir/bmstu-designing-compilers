from functools import reduce
from copy import deepcopy


class Grammar:
    notTerminals: list[str]
    terminals: list[str]
    rules: dict[str, list[list[str]]]
    start: str
    
    def __init__(
        self, 
        notTerminals: list[str],
        terminals: list[str], 
        rules: dict[str, list[list[str]]], 
        start: str
    ) -> None:
        self.notTerminals = notTerminals
        self.terminals = terminals
        self.rules = rules
        self.start = start

    def printGrammar(self) -> None:
        notTerminals = Grammar.__joinListWithSymbol(self.notTerminals, ", ")
        terminals = Grammar.__joinListWithSymbol(self.terminals, ", ")

        print(f"\nG = ({{{notTerminals}}}, {{{terminals}}}, P, {self.start}), где P состоит из правил:\n")
        for  notTerminal in self.notTerminals:
            rightRules = self.rules[notTerminal]
            self.__printProduct(notTerminal, rightRules)

    def removeLeftRecursion(self) -> None:
        i = 0
        while i < len(self.notTerminals):
            copyRules = self.rules[self.notTerminals[i]].copy()
            for j in range(i):
                self.__replaceProducts(
                    notTerminal=self.notTerminals[i],
                    replaceableNotTerminal=self.notTerminals[j],
                )
            if self.__removeDirectLeftRecursion(self.notTerminals[i]):
                i += 2
            else:
                self.rules[self.notTerminals[i]] = copyRules
                i += 1

    def __replaceProducts(self, notTerminal: str, replaceableNotTerminal: str) -> None:
        flagReplace = False
        newRightRules = []
        rightRules = self.rules[notTerminal]
        for i in range(len(rightRules)):
            if replaceableNotTerminal not in rightRules[i]:
                newRightRules.append(rightRules[i])
                continue
            
            flagReplace = True
            j = rightRules[i].index(replaceableNotTerminal)
            for substitutedRightRule in self.rules[replaceableNotTerminal]:
                newRightRule = rightRules[i][:j]
                newRightRule.extend(substitutedRightRule)
                newRightRule.extend(rightRules[i][j + 1:])
                newRightRules.append(newRightRule)
        
        if flagReplace:
            self.rules[notTerminal] = newRightRules
            print(f"\nПосле замены {replaceableNotTerminal}: ", end="")
            self.__printProduct(notTerminal, newRightRules)

    def __removeDirectLeftRecursion(self, notTerminal: str) -> bool:
        self.rules[notTerminal].sort(
            key=lambda rightRule: rightRule[0] != notTerminal
        )
        newNotTerminal = notTerminal + "'"
        rightRulesForNewNotTerminal = []
        rightRules = []

        for rightRule in deepcopy(self.rules[notTerminal]):
            if rightRule[0] != notTerminal:
                if rightRule[0] == "Ɛ":
                    rightRule = [newNotTerminal]
                else:
                    rightRule.append(newNotTerminal)
                rightRules.append(rightRule)
            else:
                rightRule = rightRule[1:]
                rightRule.append(newNotTerminal)
                rightRulesForNewNotTerminal.append(rightRule)

        if len(rightRulesForNewNotTerminal):
            rightRulesForNewNotTerminal.append("Ɛ")
            indexNotTerminal = self.notTerminals.index(newNotTerminal[:-1])
            self.notTerminals = \
                self.notTerminals[:indexNotTerminal + 1] + [newNotTerminal] + \
                self.notTerminals[indexNotTerminal + 1:]
            self.rules[newNotTerminal] = rightRulesForNewNotTerminal
            self.rules[notTerminal] = rightRules

            removedFlag = True
        else:
            removedFlag = False

        return removedFlag
    
    def __printProduct(self, notTerminal: str, rightRules: list[list[str]]):
        print(f"{notTerminal} -> ", end="")
        for i in range(len(rightRules)):
            print(f"{" | " if i != 0 else ""}{Grammar.__joinListWithSymbol(rightRules[i], " ")}", end="")
        print()

    @staticmethod
    def __joinListWithSymbol(arr: list[str], symbol: str) -> str:
        return reduce(lambda elemPrev, elem: f"{elemPrev}{symbol}{elem}", arr)


def reedGrammarFromFile(fileName: str) -> Grammar:
    with open(fileName) as f:
        lines = [line[:-1] for line in f.readlines()]

    notTerminals = lines[0].split(" ")
    terminals = lines[1].split(" ")
    start = lines[-1]
    rules = {}
    for notTerminal in notTerminals:
        rules[notTerminal] = []

    for rule in lines[2:-1]:
        rule = rule.split(" ")
        rules[rule[0]].append(rule[2:])

    return Grammar(
        notTerminals=notTerminals, 
        terminals=terminals,
        rules=rules,
        start=start,
    )
