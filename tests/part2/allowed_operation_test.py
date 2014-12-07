__author__ = 'novy'

from tests.with_mocked_stdout_test_class import BaseASTParsingTestClass


with_binary_arithmetic = """
int a = 5;
a = a | 5;
a = a & 5;
a = a ^ 5;
a = a << 5;
a = a >> 5;
"""

with_float_arithmetic = """
float a = 5.0, b = 6.0;
a = a + b;
a = a - b;
a = a * b;
a = a / b;
"""

with_integer_comparison = """
int a = 5, b = 10;

if (a < b || a <= b || a == b || a >= b || a >b || a != b) {
    int c = 10;
    c = c + 2;
}
"""

with_string_addition = """
string a = "string1", b = "string2";
string c = "";

c = a + b;
"""

with_string_multiplied_by_integer = """
string a = "string1";
string b = "";

b = a * 666;
"""

with_string_comparison = """
string a = "string1";
string b = "string2";

if (a < b || a <= b || a == b || a >= b || a >b && a != b) {
    int a = 5;
    a = a + 5;
}
"""


class AllowedOperationTest(BaseASTParsingTestClass):
    def test_binary_arithmetic_should_be_allowed(self):
        self._parse_expression(with_binary_arithmetic)

        self._assert_no_errors_occurred()

    def test_float_arithmetic_should_be_allowed(self):
        self._parse_expression(with_float_arithmetic)

        self._assert_no_errors_occurred()

    def test_integer_comparison_should_be_allowed(self):
        self._parse_expression(with_integer_comparison)

        self._assert_no_errors_occurred()

    def test_string_addition_should_be_allowed(self):
        self._parse_expression(with_string_addition)

        self._assert_no_errors_occurred()

    def test_string_multiplication_by_integer_should_be_allowed(self):
        self._parse_expression(with_string_multiplied_by_integer)

        self._assert_no_errors_occurred()

    def test_string_comparison_should_be_allowed(self):
        self._parse_expression(with_string_comparison)

        self._assert_no_errors_occurred()