import Tokenizer
import VMWriter
import SymbolTable


class CompilationEngine:
    """
    this class will create a tokenizer and use it for parsing and ordering a text and compile it into a vm file
    """
    """
    sets of operators and specialsA
    
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
        self.writer = VMWriter.VMWriter(output)
        self.symbolTable = SymbolTable.SymbolTable()
        self.classname = ""
        self.name = ""

    def advanced(self):
        """
              get next toke and value and writes them to the output file
              :return: none
              """
        return self.tokenizer.advanced()

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

    def compileClass(self):
        """
        compiling class command
        :return: none
        """
        self.advanced()
        self.className = self.advanced()[1]
        self.advanced()
        if self.existclassvardec():
            self.compileclassvardec()
        while self.existsubroutine():
            self.compilesubroutine()
        self.advanced()
        self.writer.close()

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
            self.writeclassvardec()

    def writeclassvardec(self):
        """
        write class static or field type
        :return: noen
        """
        kind = self.advanced()[1]
        type = self.advanced()[1]
        name = self.advanced()[1]
        self.symbolTable.define(name, type, kind)
        while self.checkvaluein(","):
            self.advanced()
            name = self.advanced()[1]
            self.symbolTable.define(name, type, kind)
        self.advanced()

    def compilesubroutine(self):
        """
        compile constructor, method or function type
        :return:
        """
        functionkind = self.advanced()
        self.advanced()
        self.name = self.className + "." + self.advanced()[1]
        self.symbolTable.startsubroutine(self.name)
        self.symbolTable.setScope(self.name)
        self.advanced()
        self.compileparameterlist(functionkind)
        self.advanced()
        self.compilesubroutinebody(functionkind)

    def compileparameterlist(self, type):
        """
        compile parameter type
        :return: none
        """
        if type[1] == "method":
            self.symbolTable.define("this", "self", "arg")
        while self.exist():
            self.writeparam()

    def exist(self):
        return not self.checkiftoken("symbol")

    def writeparam(self):
        """
        handle parameter option
        :return:
        """
        type = self.advanced()[1]
        name = self.advanced()[1]
        self.symbolTable.define(name, type, "arg")
        if self.checkifvalue(","):
            self.advanced()

    def compilesubroutinebody(self, type):
        self.advanced()
        while self.existvardec():
            self.compilevardec()
        vars = self.symbolTable.varcount("var")
        self.writer.write_function(self.name, vars)
        self.loadpointer(type)
        self.compilestatments()
        self.advanced()
        self.symbolTable.setScope("global")

    def loadpointer(self, functype):
        if functype[1] == "method":
            self.writer.write_push("argument", 0)
            self.writer.write_pop("pointer", 0)
        if functype[1] == "constructor":
            globalvars = self.symbolTable.globalscounts("field")
            self.writer.write_push("constant", globalvars)
            self.writer.write_call("Memory.alloc", 1)
            self.writer.write_pop("pointer", 0)

    def existvardec(self):
        return self.checkvaluein("var")

    def compilevardec(self):
        """
        compiling a var type
        :return: none
        """
        kind = self.advanced()[1]
        type = self.advanced()[1]
        name = self.advanced()[1]
        self.symbolTable.define(name, type, kind)
        while self.checkifvalue(","):
            self.advanced()
            name = self.advanced()[1]
            self.symbolTable.define(name, type, kind)
        self.advanced()

    def compilestatments(self):
        """
        compiling statments- if do let while and return
        :return: none
        """
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

    def existstatments(self):
        """
        check if a statement exists
        :return: boolean
        """
        return (self.checkifvalue("do") or self.checkifvalue("let") or self.checkifvalue("if")
                or self.checkifvalue("while") or self.checkifvalue("return"))

    def compilesubroutinecall(self):
        locals = 0
        first = self.advanced()[1]
        if self.checkifvalue("."):
            self.advanced()
            last = self.advanced()[1]
            if first in self.symbolTable.currscope or first in self.symbolTable.outscope:
                self.writer.write_push(first, last)
                full = self.symbolTable.checkType(first) + "." + last
                locals += 1
            else:
                full = first + "." + last
        else:
            self.writer.write_push("pointer", 0)
            locals += 1
            full = self.classname + "." + first
        self.advanced()
        locals += self.compileexpressionlist()
        self.writer.write_call(full, locals)
        self.advanced()

    def compileexpressionlist(self):
        """
        compiling expression list type
        :return: none
        """
        counter = 0
        if self.existterm():
            self.compileexpression()
            counter += 1
        while self.checkifvalue(","):
            self.advanced()
            self.compileexpression()
            counter += 1
        return counter

    def compilearrayindex(self, name):
        """
        compiling the array in the curr scope
        :param name: identifier
        :return: none
        """
        self.writearrayindex()
        if name in self.symbolTable.currscope:
            if self.symbolTable.checkKind(name) == "var":
                self.writer.write_push("local", self.symbolTable.checkIndex(name))
            elif self.symbolTable.checkKind(name) == "arg":
                self.writer.write_push("argument", self.symbolTable.checkIndex(name))
        else:
            if self.symbolTable.checkKind(name) == "static":
                self.writer.write_push("static", self.symbolTable.checkIndex(name))
            else:
                self.writer.write_push("this", self.symbolTable.checkIndex(name))
        self.writer.write_arythmetic("add")

    def writearrayindex(self):
        self.advanced()
        self.compileexpression()
        self.advanced()

    def compiledo(self):
        """
        compiling do statement
        :return:
        """
        self.advanced()
        self.compilesubroutinecall()
        self.writer.write_pop("temp", 0)
        self.advanced()

    def compilelet(self):
        """
         compiling let type
         :return: none
         """
        self.advanced()
        isarray = False
        name = self.advanced()[1]
        if self.checkifvalue("["):
            isarray = True
            self.compilearrayindex(name)
        self.advanced()
        self.compileexpression()
        if isarray:
            self.writer.write_pop("temp", 0)
            self.writer.write_pop("pointer", 1)
            self.writer.write_push("temp", 0)
            self.writer.write_pop("that", 0)
        else:
            self.writepop(name)
        self.advanced()

    def compilewhile(self):
        """
        compiling while type
        :return: none
        """
        counter = str(self.symbolTable.whilecounter)
        self.symbolTable.whilecounter += 1
        self.writer.write_label("WHILE_EXP" + counter)
        self.advanced()
        self.advanced()
        self.compileexpression()
        self.writer.write_arythmetic("not")
        self.writer.write_ifgoto("WHILE_END" + counter)
        self.advanced()
        self.advanced()
        self.compilestatments()
        self.writer.write_goto("WHILE_EXP" + counter)
        self.writer.write_label("WHILE_END" + counter)
        self.advanced()

    def compilereturn(self):
        """
        compiling return type
        :return: none
        """
        self.advanced()
        returnempty = True
        while self.existterm():
            returnempty = False
            self.compileexpression()
        if (returnempty):
            self.writer.write_push("constant", 0)
        self.writer.write_return()
        self.advanced()

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
        self.advanced()
        self.advanced()
        self.compileexpression()
        self.advanced()
        counter = self.symbolTable.ifcounter
        self.symbolTable.ifcounter += 1
        self.writer.write_ifgoto("IF_TRUE" + str(counter))
        self.writer.write_goto("IF_FALSE" + str(counter))
        self.writer.write_label("IF_TRUE" + str(counter))
        self.advanced()
        self.compilestatments()
        self.advanced()
        if self.checkifvalue("else"):
            self.writer.write_goto("IF_END" + str(counter))
            self.writer.write_label("IF_FALSE" + str(counter))
            self.advanced()
            self.advanced()
            self.compilestatments()
            self.advanced()
            self.writer.write_label("IF_END" + str(counter))
        else:
            self.writer.write_label("IF_FALSE" + str(counter))

    def compileexpression(self):
        """
        compile expression type
        :return: none
        """
        self.compileterm()
        while self.checkvaluein(self.op1):
            operator = self.advanced()[1]
            self.compileterm()
            if operator == "+":
                self.writer.write_arythmetic("add")
            elif operator == "-":
                self.writer.write_arythmetic("sub")
            elif operator == "*":
                self.writer.write_call("Math.multiply", 2)
            elif operator == "/":
                self.writer.write_call("Math.divide", 2)
            elif operator == "|":
                self.writer.write_arythmetic("or")
            elif operator == "&":
                self.writer.write_arythmetic("and")
            elif operator == "=":
                self.writer.write_arythmetic("eq")
            elif operator == "<":
                self.writer.write_arythmetic("lt")
            elif operator == ">":
                self.writer.write_arythmetic("gt")

    def compileterm(self):
        """
        compiling a term type
        :return: none
        """
        ar = False
        if self.checkiftoken("integerConstant"):
            value = self.advanced()[1]
            self.writer.write_push("constant", value)
        elif self.checkiftoken("stringConstant"):
            value = self.advanced()[1]
            self.writer.write_push("constant", len(value))
            self.writer.write_call("string.new", 1)
            for letter in value:
                self.writer.write_push("constant", ord(letter))
                self.writer.write_call("String.appendChar", 2)
        elif self.checkvaluein(self.words):
            value = self.advanced()[1]
            if value == "this":
                self.writer.write_push("pointer", 0)
            else:
                self.writer.write_push("constant", 0)
                if value == "true":
                    self.writer.write_arythmetic("not")
        elif self.checkiftoken("identifier"):
            var = 0
            name = self.advanced()[1]
            if self.checkifvalue("["):
                ar = True
                self.compilearrayindex(name)
            if self.checkifvalue("("):
                var += 1
                self.writer.write_push("pointer", 0)
                self.advanced()
                var += self.compileexpressionlist()
                self.advanced()
                self.writer.write_call(self.classname + "." + name, var)
            elif self.checkifvalue("."):
                self.advanced()
                last = self.advanced()[1]
                if name in self.symbolTable.currscope or name in self.symbolTable.outscope:
                    self.writepush(name, last)
                    var += 1
                else:
                    name = name + "." + last
                    self.advanced()
                    var += self.compileexpressionlist()
                    self.advanced()
                    self.writer.write_call(name, var)
            else:
                if ar:
                    self.writer.write_pop("pointer", 1)
                    self.writer.write_push("that", 0)
                elif name in self.symbolTable.currscope:
                    if self.symbolTable.checkKind(name) == "var":
                        self.writer.write_push("local", self.symbolTable.checkIndex(name))
                    elif self.symbolTable.checkKind(name) == "arg":
                        self.writer.write_push("argument", self.symbolTable.checkIndex(name))
                else:
                    if self.symbolTable.checkKind(name) == "static":
                        self.writer.write_push("static", self.symbolTable.checkIndex(name))
                    else:
                        self.writer.write_push("this", self.symbolTable.checkIndex(name))

        elif self.checkvaluein(self.op2):
            operator = self.advanced()[1]
            self.compileterm()
            if operator == "-":
                self.writer.write_arythmetic("neg")
            elif operator == "~":
                self.writer.write_arythmetic("not")
        elif self.checkifvalue("("):
            self.advanced()
            self.compileexpression()
            self.advanced()

    def writepush(self, name, last):
        if name in self.symbolTable.currscope:
            if self.symbolTable.checkKind(name) == "var":
                self.writer.write_push("local", self.symbolTable.checkIndex(name))
            elif self.symbolTable.checkKind(name) == "arg":
                self.writer.write_push("argument", self.symbolTable.checkIndex(name))
        else:
            if self.symbolTable.checkKind(name) == "static":
                self.writer.write_push("static", self.symbolTable.checkIndex(name))
            else:
                self.writer.write_push("this", self.symbolTable.checkIndex(name))

    def writepop(self, name):
        if name in self.symbolTable.currscope:
            if self.symbolTable.checkKind(name) == "var":
                self.writer.write_pop("local", self.symbolTable.checkIndex(name))
            elif self.symbolTable.checkKind(name) == "arg":
                self.writer.write_pop("argument", self.symbolTable.checkIndex(name))
        else:
            if self.symbolTable.checkKind(name) == "static":
                self.writer.write_pop("static", self.symbolTable.checkIndex(name))
            else:
                self.writer.write_pop("this", self.symbolTable.checkIndex(name))
