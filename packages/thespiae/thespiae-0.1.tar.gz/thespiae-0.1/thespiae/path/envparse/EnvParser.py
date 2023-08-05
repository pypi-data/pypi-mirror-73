# Generated from EnvParser.g4 by ANTLR 4.7.2
# encoding: utf-8
import sys
from io import StringIO

from antlr4 import *
from typing.io import TextIO


def serializedATN():
    with StringIO() as buf:
        buf.write("\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\3\7")
        buf.write("\36\4\2\t\2\4\3\t\3\4\4\t\4\3\2\3\2\3\3\3\3\3\3\3\3\7")
        buf.write("\3\17\n\3\f\3\16\3\22\13\3\3\3\5\3\25\n\3\3\3\3\3\5\3")
        buf.write("\31\n\3\3\4\3\4\3\4\3\4\2\2\5\2\4\6\2\3\3\2\4\5\2\35\2")
        buf.write("\b\3\2\2\2\4\30\3\2\2\2\6\32\3\2\2\2\b\t\t\2\2\2\t\3\3")
        buf.write("\2\2\2\n\31\7\2\2\3\13\20\5\2\2\2\f\r\7\6\2\2\r\17\5\2")
        buf.write("\2\2\16\f\3\2\2\2\17\22\3\2\2\2\20\16\3\2\2\2\20\21\3")
        buf.write("\2\2\2\21\24\3\2\2\2\22\20\3\2\2\2\23\25\7\6\2\2\24\23")
        buf.write("\3\2\2\2\24\25\3\2\2\2\25\26\3\2\2\2\26\27\7\2\2\3\27")
        buf.write("\31\3\2\2\2\30\n\3\2\2\2\30\13\3\2\2\2\31\5\3\2\2\2\32")
        buf.write("\33\5\2\2\2\33\34\7\2\2\3\34\7\3\2\2\2\5\20\24\30")
        return buf.getvalue()


class EnvParser(Parser):
    grammarFileName = "EnvParser.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [DFA(ds, i) for i, ds in enumerate(atn.decisionToState)]

    sharedContextCache = PredictionContextCache()

    literalNames = ["<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>",
                    "';'"]

    symbolicNames = ["<INVALID>", "WS", "UNQUOTED_STRING", "DOUBLE_QUOTED_STRING",
                     "DELIM", "UNRECOGNIZED"]

    RULE_entry = 0
    RULE_path = 1
    RULE_single_entry = 2

    ruleNames = ["entry", "path", "single_entry"]

    EOF = Token.EOF
    WS = 1
    UNQUOTED_STRING = 2
    DOUBLE_QUOTED_STRING = 3
    DELIM = 4
    UNRECOGNIZED = 5

    def __init__(self, input: TokenStream, output: TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.7.2")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None

    class EntryContext(ParserRuleContext):

        def __init__(self, parser, parent: ParserRuleContext = None, invokingState: int = -1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def UNQUOTED_STRING(self):
            return self.getToken(EnvParser.UNQUOTED_STRING, 0)

        def DOUBLE_QUOTED_STRING(self):
            return self.getToken(EnvParser.DOUBLE_QUOTED_STRING, 0)

        def getRuleIndex(self):
            return EnvParser.RULE_entry

        def enterRule(self, listener: ParseTreeListener):
            if hasattr(listener, "enterEntry"):
                listener.enterEntry(self)

        def exitRule(self, listener: ParseTreeListener):
            if hasattr(listener, "exitEntry"):
                listener.exitEntry(self)

    def entry(self):

        localctx = EnvParser.EntryContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_entry)
        self._la = 0  # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 6
            _la = self._input.LA(1)
            if not (_la == EnvParser.UNQUOTED_STRING or _la == EnvParser.DOUBLE_QUOTED_STRING):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class PathContext(ParserRuleContext):

        def __init__(self, parser, parent: ParserRuleContext = None, invokingState: int = -1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def EOF(self):
            return self.getToken(EnvParser.EOF, 0)

        def entry(self, i: int = None):
            if i is None:
                return self.getTypedRuleContexts(EnvParser.EntryContext)
            else:
                return self.getTypedRuleContext(EnvParser.EntryContext, i)

        def DELIM(self, i: int = None):
            if i is None:
                return self.getTokens(EnvParser.DELIM)
            else:
                return self.getToken(EnvParser.DELIM, i)

        def getRuleIndex(self):
            return EnvParser.RULE_path

        def enterRule(self, listener: ParseTreeListener):
            if hasattr(listener, "enterPath"):
                listener.enterPath(self)

        def exitRule(self, listener: ParseTreeListener):
            if hasattr(listener, "exitPath"):
                listener.exitPath(self)

    def path(self):

        localctx = EnvParser.PathContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_path)
        self._la = 0  # Token type
        try:
            self.state = 22
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [EnvParser.EOF]:
                self.enterOuterAlt(localctx, 1)
                self.state = 8
                self.match(EnvParser.EOF)
                pass
            elif token in [EnvParser.UNQUOTED_STRING, EnvParser.DOUBLE_QUOTED_STRING]:
                self.enterOuterAlt(localctx, 2)
                self.state = 9
                self.entry()
                self.state = 14
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input, 0, self._ctx)
                while _alt != 2 and _alt != ATN.INVALID_ALT_NUMBER:
                    if _alt == 1:
                        self.state = 10
                        self.match(EnvParser.DELIM)
                        self.state = 11
                        self.entry()
                    self.state = 16
                    self._errHandler.sync(self)
                    _alt = self._interp.adaptivePredict(self._input, 0, self._ctx)

                self.state = 18
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la == EnvParser.DELIM:
                    self.state = 17
                    self.match(EnvParser.DELIM)

                self.state = 20
                self.match(EnvParser.EOF)
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Single_entryContext(ParserRuleContext):

        def __init__(self, parser, parent: ParserRuleContext = None, invokingState: int = -1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def entry(self):
            return self.getTypedRuleContext(EnvParser.EntryContext, 0)

        def EOF(self):
            return self.getToken(EnvParser.EOF, 0)

        def getRuleIndex(self):
            return EnvParser.RULE_single_entry

        def enterRule(self, listener: ParseTreeListener):
            if hasattr(listener, "enterSingle_entry"):
                listener.enterSingle_entry(self)

        def exitRule(self, listener: ParseTreeListener):
            if hasattr(listener, "exitSingle_entry"):
                listener.exitSingle_entry(self)

    def single_entry(self):

        localctx = EnvParser.Single_entryContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_single_entry)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 24
            self.entry()
            self.state = 25
            self.match(EnvParser.EOF)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx
