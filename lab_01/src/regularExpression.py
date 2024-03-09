def checkRegex(regex: str):
    alphabet = "qwertyuiopasdfghjklzxcvbnm()*|"
    for symbol in regex:
        if symbol not in alphabet:
            raise ValueError(f"Недопустимый символ для регулярного выражения '{symbol}'")

    openBracketsCount = 0
    for symbol in regex:
        if symbol == '(':
            openBracketsCount += 1
        elif symbol == ')':
            if openBracketsCount > 0:
                openBracketsCount -= 1
            else:
                raise ValueError("Неверная постановка скобок в регулярном выражении")

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
        if regex[i] in "qwertyuiopasdfghjklzxcvbnm*" and \
            i != lenRegex - 1 and \
            regex[i + 1] not in ['|', '*', ')']:
            resRegex += '.'

    return resRegex + ".#"
