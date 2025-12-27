
import sys
from pylox import Lox

def main(args):
    lox = Lox()

    if len(args) > 1:
        raise ValueError("Lox takes at most one argument")

    if len(args) == 1:
        lox.run_file(args[0])
    else:
        lox.run_prompt()


if __name__ == "__main__":
    main(sys.argv[1:])
    
