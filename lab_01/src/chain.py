from color import *
from minDfa import MinDFA


def checkChain(chain: str, minDfa: MinDFA) -> bool:
    state = minDfa.initialState
    for symbol in chain:
        nextState = minDfa.minDstates[state].get(symbol)
        if nextState:
            print(f"{symbol}: {state} ---> {nextState}")
            state = nextState
        else:
            print(f"{symbol}: {state} ---> None")
            return False
    
    if state not in minDfa.finalStates:
        print(f"Состояние '{state}' не является конечным")
        return False
    
    return True


def inputСhainСheckСorrespondence(regex: str, minDFA: MinDFA) -> None:
    chain = input(f"\nВведите входную цепочку, которую хотите проверить на соответсвие регулярному выражению '{regex}': ")
    if checkChain(chain, minDFA):
        print(f"\nВходная цепочка '{chain}' {GREEN}соответствует{BASE} регулярному выражению '{regex}'.")
    else:
        print(f"\nВходная цепочка '{chain}' {RED}не соответствует{BASE} регулярному выражению '{regex}'.")
