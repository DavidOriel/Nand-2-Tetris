import re


class Tokenizer:
    """
    parsing and create a token list from a given file, the compilation engine will use that class
    to order the inputs.
    """
    """
    sets and regex for clearing the text
    """
    words = {"class", "constructor", "function", "method", "static", "field", "int", "var", "char",
             "boolean", "void", "true", "false", "null", "this", "let", "do", "if", "else", "while", "return"}
    symbols = {"{", "}", "(", ")", "[", "]", ".", ",", ";", "+", "-", "*", "/", "&", "<", ">", "=", "~"}
    keyword = '(?!\w)|'.join(words) + '(?!\w)'
    symbolsre = "[" + re.escape('|'.join(symbols)) + ']'
    integer = r'\d+'
    strings = r'"[^"\n]*"'
    identifiers = r'[\w]+'
    word = re.compile(keyword + "|" + symbolsre + "|" + integer + "|" + strings + "|" + identifiers)

    def __init__(self, filename):
        """
        constructor for the class
        :param filename:
        """
        self.file = open(filename)
        self.currToken = ""
        self.lines = self.file.read()
        self.remove_comments()
        self.tokens = self.tokenize()
        self.tokens = self.replacesymbols()

    def remove_comments(self):
        """
        parsing and ordering the text
        :return: none
        """
        currentindex = 0
        filteredtext = ""
        while currentindex < len(self.lines):
            currentchar = self.lines[currentindex]
            if currentindex == "\"":  # string - adds int to the filtered text
                endindex = self.lines.fined("\"", currentindex + 1)
                filteredtext += self.lines[currentindex:endindex + 1]
                currentindex = endindex + 1
            elif currentchar == "/":  # single line comment - remove it
                if self.lines[currentindex + 1] == "/":
                    endindex = self.lines.find("\n", currentindex + 1)
                    currentindex = endindex + 1
                    filteredtext += " "
                elif self.lines[currentindex + 1] == "*":  # multi line comment- remove it
                    endindex = self.lines.find("*/", currentindex + 1)
                    currentindex = endindex + 2
                    filteredtext += " "
                else:
                    filteredtext += self.lines[currentindex]
                    currentindex += 1
            else:
                filteredtext += self.lines[currentindex]
                currentindex += 1

        self.lines = filteredtext
        return

    def tokenize(self):
        """
        :return: get the procceced tokens
        """
        return [self.token(word) for word in self.split(self.lines)]

    def token(self, word):
        """
        anylizing the the type of the token
        :param word: combination
        :return: the anilizing token pair
        """
        if re.match(self.keyword, word) != None:
            return "keyword", word
        elif re.match(self.symbolsre, word) != None:
            return "symbol", word
        elif re.match(self.integer, word) != None:
            return "integerConstant", word
        elif re.match(self.strings, word) != None:
            return "stringConstant", word[1:-1]
        else:
            return "identifier", word

    def split(self, line):
        return self.word.findall(line)

    def replacesymbols(self):
        return [self.replace(pair) for pair in self.tokens]

    def replace(self, pair):
        token, value = pair
        if value == "<":
            return token, '&lt;'
        elif value == ">":
            return token, '&gt;'
        elif value == '"':
            return token, '&quot;'
        elif value == '&':
            return token, '&amp;'
        else:
            return token, value

    def hasmoretokens(self):
        """
        :return: boolean that represent if there is more tokens
        """
        return self.tokens != []

    def peek(self):
        """
        :return: retrieve the next token without advancing
        """
        if self.hasmoretokens():
            return self.tokens[0]
        else:
            return

    def advanced(self):
        """
        :return: returning the next token from the file if there are any..
        """
        self.currToken = self.tokens.pop(0)
        return self.currToken

    def gettokens(self):
        """
        :return:the current token
        """
        return self.currToken[0]

    def getValue(self):
        """
        :return: the current value
        """
        return self.currToken[1]
