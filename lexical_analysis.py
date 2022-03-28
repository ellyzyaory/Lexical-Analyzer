import re

tokens = []
arithmetic = {'*': "math-times", '-': "math-minus", '+': "math-plus", '/': "math-divide"}


file = open('phpfile.txt', 'r')

prev_line = 0

for line_count, line in enumerate(file):
    for column_count, letter in enumerate(line):

        if "<?php" in line and line[column_count] == '<' and line[column_count + 1] == '?' and line[column_count + 2] == 'p' and line[column_count + 3] == 'h' and line[column_count + 4] == 'p':
            tokens.append([line_count+1, column_count+1, "php-opening-tag"])

        if "?>" in line and line[column_count] == '?' and line[column_count + 1] == '>':
            tokens.append([line_count + 1, column_count + 1, "php-closing-tag"])

        if "class" in line:
            split_line = line.split(" ")
            if "class" in split_line and line[column_count] == 'c' and line[column_count + 1] == 'l' and line[column_count + 2] == 'a' and line[column_count + 3] == 's' and line[column_count + 4] == 's':
                tokens.append([line_count + 1, column_count + 1, "class"])

            if split_line and letter == split_line[1][0]:
                tokens.append([line_count + 1, column_count + 1, "type-identifier", split_line[1]])

        if '{' in line and letter == '{':
            tokens.append([line_count + 1, column_count + 1, "opening-curly-bracket"])

        if '}' in line and letter == '}':
            tokens.append([line_count + 1, column_count + 1, "closing-curly-bracket"])

        if '(' in line and letter == '(':
            tokens.append([line_count + 1, column_count + 1, "opening-bracket"])

        if ')' in line and letter == ')':
            tokens.append([line_count + 1, column_count + 1, "closing-bracket"])

        for operator in arithmetic:
            if operator in line and letter == operator:
                tokens.append([line_count + 1, column_count + 1, arithmetic.get(operator)])

        if "function" in line:
            split_line = line.strip().split("()")
            results = re.search("function (.*)", split_line[0])
            function_name = results.group(1)

            if split_line and letter == function_name[0]:
                tokens.append([line_count + 1, column_count + 1, "type-identifier", function_name])

        if "function" in line:
            split_line = line.strip().split(" ")
            if "function" in split_line and line[column_count] == 'f' and line[column_count + 1] == 'u' and line[column_count + 2] == 'n' and line[column_count + 3] == 'c' and line[column_count + 4] == 't' and line[column_count + 5] == 'i' and line[column_count + 6] == 'o' and line[column_count + 7] == 'n':
                tokens.append([line_count + 1, column_count + 1, "function"])

        if '$' in line and letter == '$' and line[column_count+1] != '=':
            tokens.append([line_count + 1, column_count + 1, 'variable'])
            split_line = line.strip().split(" ")
            for word in split_line:
                if '$' in word:
                    word = word.strip('\n')
                    assignment = word.split("=")
                    if prev_line != line_count+1:
                        variable_unfiltered = assignment[0]
                        variable_filtered = re.sub('[^A-Za-z0-9]+', '', variable_unfiltered)
                        variable = re.sub('\d+', '', variable_filtered)
                        if variable != "":
                            tokens.append([line_count + 1, column_count + 2, "type-identifier", variable])
                            prev_line = line_count+1

                    elif prev_line == line_count+1:
                        variable_unfiltered = assignment[1]
                        variable_filtered = re.sub('[^A-Za-z0-9]+', '', variable_unfiltered)
                        variable = re.sub('\d+', '', variable_filtered)
                        if variable != "":
                            tokens.append([line_count + 1, column_count + 2, "type-identifier", variable])
                            prev_line = line_count + 1

        if '=' in line and letter == '=' and line[column_count-1] != '$':
            tokens.append([line_count + 1, column_count + 1, 'assign'])
            line_split = line.split()
            for sepr in line_split:
                if '=' in sepr:
                    assign = sepr.split('=')

        if letter.isdigit():
            tokens.append([line_count + 1, column_count + 1, 'number', int(letter)])

        if ';' in line and letter == ';':
            tokens.append([line_count + 1, column_count + 1, 'semicolon'])

        if 'echo' in line and line[column_count] == 'e' and line[column_count + 1] == 'c' and line[column_count + 2] == 'h' and line[column_count + 3] == 'o':
            tokens.append([line_count + 1, column_count + 1, 'print-out'])

        if '.' in line and letter == '.':
            tokens.append([line_count + 1, column_count + 1, 'concate'])

        if '"' in line and letter == '"':
            if prev_line != line_count+1:
                split_line = line.split('"')
                nbsp_checked = []
                replace = "&nbsp\\'"
                for word in split_line:
                    nbsp_checked.append(word.replace(" ", replace))
                tokens.append([line_count + 1, column_count + 1, 'string-literal', nbsp_checked[1]])
                prev_line = line_count + 1


for token in tokens:
    print(token)