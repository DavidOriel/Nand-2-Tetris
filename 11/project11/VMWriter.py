
class VMWriter:
    """
    this class will write for us a vm file, the comp engine is using the functionality here
    """
    def __init__(self,output):
        self.outputFile = open(output,"w")

    def write_arythmetic(self,ary):
        """
        write arytmetic command
        :param ary:
        :return:
        """
        self.outputFile.write(ary+"\n")

    def write_pop(self,word,index):
        """
        write pop command
        :param word: the word command
        :param index: the index
        :return: none
        """
        self.outputFile.write("pop " +word+  " "+ str(index)+ "\n")

    def write_push(self,word,index):
        """
        write push command
        :param word: the word command
        :param index: the index
        :return: none
        """
        self.outputFile.write("push " +word+ " "+ str(index)+ "\n")

    def write_label(self,word):
        """
        write label
        :param word: word
        :return: none
        """
        self.outputFile.write("label " + word+ "\n")

    def write_goto(self,word):
        """
        write go to command
        :param word: word
        :return: none
        """
        self.outputFile.write("goto "+word+"\n")

    def write_ifgoto(self,word):
        """
        write if go to command
        :param word: word
        :return: none
        """
        self.outputFile.write("if-goto "+word+"\n")

    def write_call(self,word,index):
        """
        write call command
        :param word: word
        :param index: index
        :return: none
        """
        self.outputFile.write("call "+ word+ " "+ str(index)+"\n")

    def write_function(self,word,index):
        """
        write a vm function
        :param word: word
        :param index: index
        :return: none
        """
        self.outputFile.write("function "+word+ " "+ str(index)+ "\n")

    def write_return(self):
        """
        write return command
        :return: none
        """
        self.outputFile.write("return\n")

    def close(self):
        """
        close the file
        :return: none
        """
        self.outputFile.close()