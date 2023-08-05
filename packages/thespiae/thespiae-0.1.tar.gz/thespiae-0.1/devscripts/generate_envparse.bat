@ECHO OFF

ECHO Generating lexer and parser files...
SET B=%cd%
SET P=%~dp0..\thespiae\path
cd %P%
java org.antlr.v4.Tool -Dlanguage=Python3 -o envparse EnvLexer.g4 EnvParser.g4
cd %B%