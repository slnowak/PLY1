import sys
import ply.yacc as yacc
from parser import Cparser
import tree_printer

if __name__ == '__main__':

    try:
        filename = sys.argv[1] if len(sys.argv) > 1 else "example.txt"
        f = open(filename, "r")
    except IOError:
        print("Cannot open {0} file".format(filename))
        sys.exit(0)

    Cparser = Cparser()
    parser = yacc.yacc(module=Cparser)
    text = f.read()
    parser.parse(text, lexer=Cparser.scanner)
