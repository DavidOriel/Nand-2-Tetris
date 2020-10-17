class SymbolTable:

    def __init__(self):
        self.outscope = {}
        self.subroutinescope = {}
        self.currscope = self.outscope
        self.varcounter = 0
        self.argcouter = 0
        self.fieldcounter = 0
        self.staticcounter = 0
        self.ifcounter = 0
        self.whilecounter = 0

    def startsubroutine(self, name):
        """
        start a subroutine new scope, setting all parameters to 0
        :param name: name of the scope
        :return:none
        """
        self.subroutinescope[name] = {}
        self.argcounter = 0
        self.ifcounter = 0
        self.ifcounter = 0
        self.whilecounter = 0

    def define(self, name, type, kind):
        """
        define a new indentifier by name type and kind
        :param name:name
        :param type:type
        :param kind:kind
        :return: none
        """
        if kind == "static":
            self.outscope[name] = (type, kind, self.staticcounter)
            self.staticcounter += 1
        if kind == "arg":
            self.currscope[name] = (type, kind, self.argcounter)
            self.argcounter += 1
        if kind == "field":
            self.outscope[name] = (type, kind, self.fieldcounter)
            self.fieldcounter += 1
        if kind == "var":
            self.currscope[name] = (type, kind, self.argcounter)
            self.varcounter += 1

    def globalscounts(self, glob):
        """
        counts how many items in the outer scope
        :param glob: glob
        :return: int
        """
        counter = 0
        for (k, v) in self.outscope.items():
            if v[1] == glob:
                counter += 1
        return counter

    def varcount(self, var):
        """
        counts how many variables in the scope
        :param var: the variable
        :return: int
        """
        counter = 0
        for (k, v) in self.currscope.items():
            if v[1] == var:
                counter += 1
        return counter

    def checkType(self, name):
        """
        return the type of the identifier in the scope
        :param name:the name
        :return: the type
        """
        if name in self.currscope:
            return self.currscope[name][0]
        if name in self.outscope:
            return self.outscope[name][0]
        else:
            return "NOTHING"

    def checkKind(self, name):
        """
        check the kind of the identifier
        :param name: the name to check
        :return: the name else None
        """
        if name in self.currscope:
            return self.currscope[name][1]
        if name in self.outscope:
            return self.outscope[name][1]
        else:
            return

    def checkIndex(self, name):
        """
        check the index o the identifier
        :param name: name
        :return: int, alse None
        """
        if name in self.currscope:
            return self.currscope[name][2]
        if name in self.outscope:
            return self.outscope[name][2]
        else:
            return

    def setScope(self, name):
        """
        set the scope
        :param name:the name
        :return:none
        """
        if name == "global":
            self.currscope = self.outscope
        else:
            self.currscope = self.subroutinescope[name]
