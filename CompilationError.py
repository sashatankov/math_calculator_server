import sys


class CompilationError(Exception):

    def __init__(self, msg):
        sys.stderr.write(msg)


