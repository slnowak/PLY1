__author__ = 'novy'

sample_input = """
float a = 0, b = 0, c = 0;

int gcd(int m, int n) {

int res = 0;
if (m!=n) {
    if (m > n)
        res = gcd(m-n, n);
    else
        res = gcd(n-m, m);
}
else
    res = m;

print res;
return res;
}

while(a >= b ) {
    a = 1/2*(a+b/a);
}
"""

expected_output = """DECL
| =
| | a
| | 0
| =
| | b
| | 0
| =
| | c
| | 0
FUNDEF
| gcd
| RET int
| ARG m
| ARG n
| DECL
| | =
| | | res
| | | 0
| IF
| | !=
| | | m
| | | n
| | IF
| | | >
| | | | m
| | | | n
| | | =
| | | | res
| | | | FUNCALL
| | | | | gcd
| | | | | -
| | | | | | m
| | | | | | n
| | | | | n
| | ELSE
| | | =
| | | | res
| | | | FUNCALL
| | | | | gcd
| | | | | -
| | | | | | n
| | | | | | m
| | | | | m
| ELSE
| | =
| | | res
| | | m
| PRINT
| | res
| RETURN
| | res
WHILE
| >=
| | a
| | b
| =
| | a
| | *
| | | /
| | | | 1
| | | | 2
| | | +
| | | | a
| | | | /
| | | | | b
| | | | | a
"""