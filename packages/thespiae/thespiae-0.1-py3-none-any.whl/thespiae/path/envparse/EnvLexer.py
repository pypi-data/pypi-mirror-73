# Generated from EnvLexer.g4 by ANTLR 4.7.2
import sys
from io import StringIO

from antlr4 import *
from typing.io import TextIO


def serializedATN():
    with StringIO() as buf:
        buf.write("\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\2\7")
        buf.write("+\b\1\4\2\t\2\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\3\2\6\2")
        buf.write("\17\n\2\r\2\16\2\20\3\2\3\2\3\3\3\3\7\3\27\n\3\f\3\16")
        buf.write("\3\32\13\3\3\4\3\4\7\4\36\n\4\f\4\16\4!\13\4\3\4\3\4\3")
        buf.write("\5\3\5\3\6\6\6(\n\6\r\6\16\6)\3)\2\7\3\3\5\4\7\5\t\6\13")
        buf.write("\7\3\2\6\4\2\13\13\"\"\6\2\13\13\"\"$$==\4\2$$==\3\2$")
        buf.write("$\2.\2\3\3\2\2\2\2\5\3\2\2\2\2\7\3\2\2\2\2\t\3\2\2\2\2")
        buf.write("\13\3\2\2\2\3\16\3\2\2\2\5\24\3\2\2\2\7\33\3\2\2\2\t$")
        buf.write("\3\2\2\2\13\'\3\2\2\2\r\17\t\2\2\2\16\r\3\2\2\2\17\20")
        buf.write("\3\2\2\2\20\16\3\2\2\2\20\21\3\2\2\2\21\22\3\2\2\2\22")
        buf.write("\23\b\2\2\2\23\4\3\2\2\2\24\30\n\3\2\2\25\27\n\4\2\2\26")
        buf.write("\25\3\2\2\2\27\32\3\2\2\2\30\26\3\2\2\2\30\31\3\2\2\2")
        buf.write("\31\6\3\2\2\2\32\30\3\2\2\2\33\37\7$\2\2\34\36\n\5\2\2")
        buf.write("\35\34\3\2\2\2\36!\3\2\2\2\37\35\3\2\2\2\37 \3\2\2\2 ")
        buf.write("\"\3\2\2\2!\37\3\2\2\2\"#\7$\2\2#\b\3\2\2\2$%\7=\2\2%")
        buf.write("\n\3\2\2\2&(\13\2\2\2\'&\3\2\2\2()\3\2\2\2)*\3\2\2\2)")
        buf.write("\'\3\2\2\2*\f\3\2\2\2\7\2\20\30\37)\3\b\2\2")
        return buf.getvalue()


class EnvLexer(Lexer):
    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [DFA(ds, i) for i, ds in enumerate(atn.decisionToState)]

    WS = 1
    UNQUOTED_STRING = 2
    DOUBLE_QUOTED_STRING = 3
    DELIM = 4
    UNRECOGNIZED = 5

    channelNames = [u"DEFAULT_TOKEN_CHANNEL", u"HIDDEN"]

    modeNames = ["DEFAULT_MODE"]

    literalNames = ["<INVALID>",
                    "';'"]

    symbolicNames = ["<INVALID>",
                     "WS", "UNQUOTED_STRING", "DOUBLE_QUOTED_STRING", "DELIM", "UNRECOGNIZED"]

    ruleNames = ["WS", "UNQUOTED_STRING", "DOUBLE_QUOTED_STRING", "DELIM",
                 "UNRECOGNIZED"]

    grammarFileName = "EnvLexer.g4"

    def __init__(self, input=None, output: TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.7.2")
        self._interp = LexerATNSimulator(self, self.atn, self.decisionsToDFA, PredictionContextCache())
        self._actions = None
        self._predicates = None
