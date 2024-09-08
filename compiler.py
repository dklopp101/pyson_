from parser import *
from node import *

def compile_source(input_path):
    # parse input file into token list.
    toklist = tokenize(input_path)