from ply import yacc
from src.type_checker import TypeChecker

__author__ = 'novy'

from StringIO import StringIO
import unittest
import sys
from src.parser import Cparser


class BaseASTParsingTestClass(unittest.TestCase):

    def setUp(self):
        self.Cparser = Cparser()
        self.mocked_stdout = StringIO()
        sys.stdout = self.mocked_stdout

    def _assert_type_checker_prints_message(self, expected_error_message):
        error_messages = self._get_error_messages()

        self.assertNotEqual(len(error_messages), 0, "Error message should not be empty")
        self.assertIn(expected_error_message, error_messages)

    def _assert_no_errors_occurred(self):
        error_messages = self._get_error_messages()
        self.assertEqual(len(error_messages), 0, "There should be no error message")

    def _get_error_messages(self):
        return [error_message for error_message in self.mocked_stdout.getvalue().split("\n")
                if error_message]

    def _parse_expression(self, expression):
        parser = yacc.yacc(module=self.Cparser)
        ast = parser.parse(expression, lexer=self.Cparser.scanner)
        TypeChecker().visit(ast)
