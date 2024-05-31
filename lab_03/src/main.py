from grammer_parser import tokenize, parse, PARSE_EXPRESSION, PARSE_PROGRAM


code = '''
begin 
    a := (-1800 + not(-56)) <> 18;
    b := (a * 2) and (88 mod 3);
    c := (-a and 0.007) <> not(b * (a - 45));
    d := not (100.0 / (25 + 46) - 28 * 0.001)
end
'''


def main():
    tokens = tokenize(code)
    print(tokens)
    parse(PARSE_PROGRAM, tokens)


if __name__ == '__main__':
    main()
