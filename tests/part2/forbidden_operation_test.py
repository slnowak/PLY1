from tests.with_mocked_stdout_test_class import BaseASTParsingTestClass

__author__ = 'novy'


with_string_multiplication = """
string a = "aaaa";
string b = "bbbb";

a = a * b;
"""

with_string_division = """
string a = "aaaa";
string b = "bbbb";

a = a / b;
"""

with_string_subtraction = """
string a = "aaaa";
string b = "bbbb";

a = a - b;
"""

with_string_multiplication_by_float = """
string a = "aaaa";
float b = 3.0;

a = a * b;
"""

with_integer_added_to_string = """
string a = "aaaa";
int b = 3;

a = a + b;
"""

with_integer_subtracted_from_string = """
string a = "aaaa";
int b = 3;

a = a - b;
"""

with_string_divided_by_integer = """
string a = "aaaa";
int b = 3;

a = a + b;
"""

with_string_added_to_integer = """
string a = "aaaa";
int b = 3;

a = b + a;
"""

with_string_subtracted_from_integer = """
string a = "aaaa";
int b = 3;

a = b - a;
"""

with_integer_divided_by_string = """
string a = "aaaa";
int b = 3;

a = a + b;
"""

with_string_and_integer_comparison = """
string a = "aaaa";
int b = 3;

if (a == b) {
    int c = 2;
    c = c + 2;
}
"""

with_string_to_integer_assignment = """
string a = "aaaa";
int b = 3;

b = a;
"""

with_integer_to_string_assignment = """
string a = "aaaa";
int b = 3;

a = b;
"""

error_message = "Incompatible types in line 5"


class ForbiddenOperationTest(BaseASTParsingTestClass):

    def test_string_multiplication_should_be_forbidden(self):

        self._parse_expression(with_string_multiplication)
        self._assert_type_checker_prints_message(error_message)

    def test_string_division_should_be_forbidden(self):

        self._parse_expression(with_string_division)
        self._assert_type_checker_prints_message(error_message)

    def test_string_subtraction_should_be_forbidden(self):

        self._parse_expression(with_string_subtraction)
        self._assert_type_checker_prints_message(error_message)

    def test_string_multiplication_by_float_should_be_forbidden(self):

        self._parse_expression(with_string_multiplication_by_float)
        self._assert_type_checker_prints_message(error_message)

    def test_integer_addition_to_string_should_be_forbidden(self):

        self._parse_expression(with_integer_added_to_string)
        self._assert_type_checker_prints_message(error_message)

    def test_integer_subtraction_from_string_should_be_forbidden(self):

        self._parse_expression(with_integer_subtracted_from_string)
        self._assert_type_checker_prints_message(error_message)

    def test_string_division_by_integer_should_be_forbidden(self):

        self._parse_expression(with_string_divided_by_integer)
        self._assert_type_checker_prints_message(error_message)

    def test_string_addition_to_integer_should_be_forbidden(self):

        self._parse_expression(with_string_added_to_integer)
        self._assert_type_checker_prints_message(error_message)

    def test_string_subtraction_from_integer_should_be_forbidden(self):

        self._parse_expression(with_string_subtracted_from_integer)
        self._assert_type_checker_prints_message(error_message)

    def test_integer_division_by_string_should_be_forbidden(self):

        self._parse_expression(with_integer_divided_by_string)
        self._assert_type_checker_prints_message(error_message)

    def test_string_and_integer_comparison_should_be_forbidden(self):

        self._parse_expression(with_string_and_integer_comparison)
        self._assert_type_checker_prints_message(error_message)

    def test_assignment_integer_to_string_should_be_forbidden(self):

        self._parse_expression(with_integer_to_string_assignment)
        self._assert_type_checker_prints_message(
            "Value of type int cannot be assigned to symbol a of type string (line 5)"
        )

    def test_assignment_string_to_integer_should_be_forbidden(self):

        self._parse_expression(with_string_to_integer_assignment)
        self._assert_type_checker_prints_message(
            "Value of type string cannot be assigned to symbol b of type int (line 5)"
        )

