# Generated from EnvParser.g4 by ANTLR 4.7.2
from antlr4 import *

if __name__ is not None and "." in __name__:
    from .EnvParser import EnvParser
else:
    from EnvParser import EnvParser


# This class defines a complete listener for a parse tree produced by EnvParser.
class EnvParserListener(ParseTreeListener):

    # Enter a parse tree produced by EnvParser#entry.
    def enterEntry(self, ctx: EnvParser.EntryContext):
        pass

    # Exit a parse tree produced by EnvParser#entry.
    def exitEntry(self, ctx: EnvParser.EntryContext):
        pass

    # Enter a parse tree produced by EnvParser#path.
    def enterPath(self, ctx: EnvParser.PathContext):
        pass

    # Exit a parse tree produced by EnvParser#path.
    def exitPath(self, ctx: EnvParser.PathContext):
        pass

    # Enter a parse tree produced by EnvParser#single_entry.
    def enterSingle_entry(self, ctx: EnvParser.Single_entryContext):
        pass

    # Exit a parse tree produced by EnvParser#single_entry.
    def exitSingle_entry(self, ctx: EnvParser.Single_entryContext):
        pass
