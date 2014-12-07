from ply import yacc
from src.type_checker import TypeChecker
from tests.with_mocked_stdout_test_class import BaseASTParsingTestClass

__author__ = 'novy'

with_undeclared_variable_usage = """
int a = 5;

while (a > b) {
    a = a + 1;
}
"""

with_duplicated_variable_declaration = """
int a = 5, b = 10;

while (a > b) {
    int c = 16;
    int c = 10;
    c = c + 2;
}
"""

with_wrong_operand_type = """
int a = 5, b = 10;

while (a > b) {
    a = a + 2.0;
}
"""

with_wrong_assignment_type = """
string s = "string";
int a = 45;

a = s;
"""


class SemanticErrorTest(BaseASTParsingTestClass):
    def test_should_detect_using_undeclared_variable(self):
        expected_error_message = """Symbol b in line 4 not declared before"""

        self._parse_expression(with_undeclared_variable_usage)

        self._assert_type_checker_prints_message(expected_error_message)

    def test_should_detect_duplicated_variable_declaration(self):
        expected_error_message = """Duplicated usage of symbol c in line 5"""

        self._parse_expression(with_duplicated_variable_declaration)

        self._assert_type_checker_prints_message(expected_error_message)

    def test_should_detect_wrong_operand_type(self):
        expected_error_message = """Value of type float cannot be assigned to symbol a of type int (line 5)"""

        self._parse_expression(with_wrong_operand_type)

        self._assert_type_checker_prints_message(expected_error_message)

    def test_should_detect_wrong_assignment_type(self):
        expected_error_message = """Value of type string cannot be assigned to symbol a of type int (line 5)"""

        self._parse_expression(with_wrong_assignment_type)

        self._assert_type_checker_prints_message(expected_error_message)