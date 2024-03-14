from pythonds.basic.stack import Stack


def checkRegex(regex: str):
    alphabet = "qwertyuiopasdfghjklzxcvbnm()*|"
    for symbol in regex:
        if symbol not in alphabet:
            raise ValueError(f"Недопустимый символ для регулярного выражения '{symbol}'")

    openBracketsCount = 0
    stack = Stack()
    lettersBetween = 0
    for symbol in regex:
        if symbol == '(':
            openBracketsCount += 1
            stack.push(lettersBetween + 1)
            lettersBetween = 0
        elif symbol == ')':
            if openBracketsCount > 0:
                openBracketsCount -= 1
            else:
                raise ValueError("Неверная постановка скобок в регулярном выражении")
            
            # в скобках должно быть только одно выражение
            if lettersBetween != 2:
                raise ValueError("Неверная постановка скобок в регулярном выражении")
            else:
                lettersBetween = stack.pop()
        elif symbol != '|':
            lettersBetween += 1

    if openBracketsCount > 0:
        raise ValueError("Не все скобки в регулярном выражении были закрыты")

    lenRegex = len(regex)
    for i in range(lenRegex):
        if regex[i] == '|' and (
            i == 0 or \
            i == lenRegex - 1 or \
            regex[i - 1] in ['|', '('] or \
            regex[i + 1] in ['|', '*', ')'] 
        ):
            raise ValueError("Недопустимое расположение символа '|'")
        
        if regex[i] == '*' and (
            i == 0 or \
            regex[i - 1] in ['|', '*', '(']
        ):
            raise ValueError("Недопустимое расположение символа '*'")


def convertToDesiredFormat(regex: str):
    resRegex = ""
    lenRegex = len(regex)
    for i in range(lenRegex):
        resRegex += regex[i]
        if regex[i] in "qwertyuiopasdfghjklzxcvbnm*)" and \
            i != lenRegex - 1 and \
            regex[i + 1] not in ['|', '*', ')']:
            resRegex += '.'

    # учет приоритета оператора '*'
    i = 1
    while i < len(resRegex) - 1:
        if resRegex[i] == "*" and resRegex[i - 1] != ")":
            resRegex = f"{resRegex[:i - 1]}({resRegex[i - 1:i + 1]}){resRegex[i + 1:]}"
            i += 2
        i += 1

    return resRegex + ".#"
