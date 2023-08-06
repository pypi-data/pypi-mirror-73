from os import path
import logging

if __package__ is None:
    import sys

    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
    from py_redact.pptx_redactor import PptxRedactor
else:
    from py_redact.pptx_redactor import PptxRedactor


def main():
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger("redact")
    if len(sys.argv) < 3:
        logger.error("Not Enough Arguments!")
    elif path.isfile(sys.argv[1]) == 0:
        logger.error("No such file : " + sys.argv[1])
    else:
        replace_char = '*'
        input_file = sys.argv[1]
        regexes = [r"""\d{3}-\d{2}-\d{4}""", r"""(([a-zA-Z0-9_\.+-]+)@([a-zA-Z0-9-]+)\.[a-zA-Z0-9-\.]+)"""]
        redactor = PptxRedactor(input_file, regexes, replace_char)
        redactor.redact(sys.argv[2])


if __name__ == "__main__":
    main()
