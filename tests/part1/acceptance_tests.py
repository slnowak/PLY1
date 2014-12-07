from StringIO import StringIO
import unittest
import sys
from ply import yacc
from test_data import sample_input, expected_output
from src.parser import Cparser
import src.tree_printer
from tests.with_mocked_stdout_test_class import BaseASTParsingTestClass

__author__ = 'novy'


class TestASTParsing(BaseASTParsingTestClass):

    def test_printing_ast_tree(self):
        parser = yacc.yacc(module=self.Cparser)
        ast = parser.parse(sample_input, lexer=self.Cparser.scanner)
        ast.print_tree(0)

        self.assertEqual(
            self.mocked_stdout.getvalue(), expected_output
        )

    def test_should_display_syntax_error_line_and_column_given_incorrect_input(self):
        with_missing_semicolon = "int foo() { a = 5;  return a }"

        expected_result = """Syntax error at line 1, column 29: LexToken(}, '}')\n"""

        parser = yacc.yacc(module=self.Cparser)
        parser.parse(with_missing_semicolon, lexer=self.Cparser.scanner)
        self.assertEqual(
            self.mocked_stdout.getvalue(), expected_result
        )

if __name__ == '__main__':
    unittest.main()