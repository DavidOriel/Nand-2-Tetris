import Tokenizer


class CompilationEngine:
    """
    this class will create a tokenizer and use it for parsing and ordering a text and compile it into a xmla file
    """
    """
    sets of operators and specials
    """
    op1 = {"+", "-", "*", "/", "|", "=", "&lt;", "&gt;", "&amp;"}
    op2 = {"-", "~"}
    words = {"true", "false", "null", "this"}

    def __init__(self, input, output):
        """

        :param input: input file name
        :param output: output file name whhere the text will be written
        """
        self.tokenizer = Tokenizer.Tokenizer(input)
        self.parsedrule = []
        self.output = open(output, "w")
        self.indent = ""

    def writestart(self, command):
        """
        write the beginning for a given command
        :param command: command which need to compile
        :return: none
        """
        self.output.write(self.indent + "<" + command + ">\n")
        self.parsedrule.append(command)
        self.indent += "    "

    def writelast(self):
        """
        write the end for a single compilation
        :return: none
        """
        self.indent = self.indent[:-4]
        command = self.parsedrule.pop()
        self.output.write(self.indent + "</" + command + ">\n")

    def writetext(self, token, value):
        """
        write a compilation main line
        :param token: given token
        :param value: given value
        :return: none
        """
        self.output.write(self.indent + "<" + token + "> " + value + " </" + token + ">\n")

    def advanced(self):
        """
        get next toke and value and writes them to the output file
        :return: none
        """
        token, value = self.tokenizer.advanced()
        self.writetext(token, value)

    def checkvaluein(self, list):
        """
        check if the value is in a given list
        :param list: the list to check
        :return: boolean
        """
        token, value = self.tokenizer.peek()
        return value in list

    def checkifvalue(self, val):
        """
        check if the next value is equal to a given param
        :param val: given param
        :return: boolean
        """
        token, value = self.tokenizer.peek()
        return value == val

    def checkiftoken(self, val):
        """
        checl if the next token is equal to a given param
        :param val: the given param
        :return: boolean
        """
        token, value = self.tokenizer.peek()
        return token == val

    def compileclass(self):
        """
        compiling class command
        :return: none
        """
        self.writestart("class")
        self.advanced()
        self.advanced()
        self.advanced()
        if self.existclassvardec():
            self.compileclassvardec()
        while self.existsubroutine():
            self.compilesubroutine()
        self.advanced()
        self.writelast()
        self.output.close()

    def existclassvardec(self):
        """
        check if the command is static or field
        :return: boolean
        """
        return self.checkifvalue("static") or self.checkifvalue("field")

    def existsubroutine(self):
        """
        check if the command is constructor method or function
        :return:
        """
        return self.checkifvalue("constructor") or self.checkifvalue("method") or self.checkifvalue("function")

    def compileclassvardec(self):
        """
        compile static or field class
        :return: none
        """
        while self.existclassvardec():
            self.writestart("classVarDec")
            self.writeclassvardec()
            self.writelast()

    def writeclassvardec(self):
        """
        write class static or field type
        :return: noen
        """
        self.advanced()
        self.advanced()
        self.advanced()
        while self.checkifvalue(","):
            self.advanced()
            self.advanced()
        self.advanced()

    def compilesubroutine(self):
        """
        compile constructor, method or function type
        :return:
        """
        self.writestart("subroutineDec")
        self.advanced()
        self.advanced()
        self.advanced()
        self.advanced()
        self.compileparameterlist()
        self.advanced()
        self.compilesubroutinebody()
        self.writelast()

    def compileparameterlist(self):
        """
        compile parameter type
        :return: none
        """
        self.writestart("parameterList")
        while not self.checkiftoken("symbol"):
            self.writeparam()
        self.writelast()

    def writeparam(self):
        """
        handle parameter option
        :return:
        """
        self.advanced()  # param name
        self.advanced()  # param type
        if self.checkifvalue(","):
            self.advanced()  # get ","

    def compilesubroutinebody(self):
        self.writestart("subroutineBody")
        self.advanced()
        while self.checkifvalue("var"):
            self.compilevar()
        self.compilestatments()
        self.advanced()
        self.writelast()

    def compilevar(self):
        """
        compiling a var type
        :return: none
        """
        self.writestart("varDec")
        self.advanced()
        self.advanced()
        self.advanced()
        while self.checkifvalue(","):
            self.advanced()
            self.advanced()
        self.advanced()
        self.writelast()

    def compilestatments(self):
        """
        compiling statments- if do let while and return
        :return: none
        """
        self.writestart("statements")
        while self.existstatments():
            if self.checkifvalue("do"):
                self.compiledo()
            elif self.checkifvalue("let"):
                self.compilelet()
            elif self.checkifvalue("if"):
                self.compileif()
            elif self.checkifvalue("while"):
                self.compilewhile()
            elif self.checkifvalue("return"):
                self.compilereturn()
        self.writelast()

    def existstatments(self):
        """
        check if a statement exists
        :return: boolean
        """
        return self.checkifvalue("do") or self.checkifvalue("let") or self.checkifvalue("if") \
               or self.checkifvalue("while") or self.checkifvalue("return")

    def compiledo(self):
        """
        compiling do statement
        :return:
        """
        self.writestart("doStatement")
        self.advanced()
        self.compilesubroutinecall()
        self.advanced()
        self.writelast()

    def compilesubroutinecall(self):
        self.advanced()
        if self.checkifvalue("."):
            self.advanced()
            self.advanced()
        self.advanced()
        self.compileexpressionlist()
        self.advanced()

    def compileexpressionlist(self):
        """
        compiling expression list type
        :return: none
        """
        self.writestart("expressionList")
        if self.existterm():
            self.compileexpression()
        while self.checkifvalue(","):
            self.advanced()
            self.compileexpression()
        self.writelast()

    def compilelet(self):
        """
        compiling let type
        :return: none
        """
        self.writestart("letStatement")
        self.advanced()
        self.advanced()
        if self.checkifvalue("["):
            self.writearray()
        self.advanced()
        self.compileexpression()
        self.advanced()
        self.writelast()

    def writearray(self):
        """
        compiling array type
        :return:
        """
        self.advanced()
        self.compileexpression()
        self.advanced()

    def compilewhile(self):
        """
        compiling while type
        :return: none
        """
        self.writestart("whileStatement")
        self.advanced()
        self.advanced()
        self.compileexpression()
        self.advanced()
        self.advanced()
        self.compilestatments()
        self.advanced()
        self.writelast()

    def compilereturn(self):
        """
        compiling return type
        :return: none
        """
        self.writestart("returnStatement")
        self.advanced()
        while self.existterm():
            self.compileexpression()
        self.advanced()
        self.writelast()

    def existterm(self):
        """
        check if a term exists
        :return: boolean
        """
        return self.checkiftoken("integerConstant") or self.checkiftoken("stringConstant") or \
               self.checkiftoken("identifier") or (self.checkvaluein(self.op2)) or \
               self.checkvaluein(self.words) or self.checkifvalue("(")

    def compileif(self):
        """
        compiling if type
        :return: none
        """
        self.writestart("ifStatement")
        self.advanced()
        self.advanced()
        self.compileexpression()
        self.advanced()
        self.advanced()
        self.compilestatments()
        self.advanced()
        if self.checkifvalue("else"):
            self.advanced()
            self.advanced()
            self.compilestatments()
            self.advanced()
        self.writelast()

    def compileexpression(self):
        """
        compile expression type
        :return: none
        """
        self.writestart("expression")
        self.compileterm()
        while self.checkvaluein(self.op1):
            self.advanced()
            self.compileterm()
        self.writelast()

    def compileterm(self):
        """
        compiling a term type
        :return: none
        """
        self.writestart("term")
        if self.checkiftoken("integerConstant") or self.checkiftoken("stringConstant") \
                or self.checkvaluein(self.words):
            self.advanced()
        elif self.checkiftoken("identifier"):
            self.advanced()
            if self.checkifvalue("["):
                self.writearray()
            if self.checkifvalue("("):
                self.advanced()
                self.compileexpressionlist()
                self.advanced()
            if self.checkifvalue("."):
                self.advanced()
                self.advanced()
                self.advanced()
                self.compileexpressionlist()
                self.advanced()
        elif self.checkvaluein(self.op2):
            self.advanced()
            self.compileterm()
        elif self.checkifvalue("("):
            self.advanced()
            self.compileexpression()
            self.advanced()
        self.writelast()
