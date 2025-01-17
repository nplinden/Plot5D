import argparse as ap

parser = ap.ArgumentParser(
    prog="Plot5D",
    description="A plotting tool for your favorite dataframes"
)
parser.add_argument("-p", "--port", help="A port for the debug server", type=int)
parser.add_argument("-f", "--file", help="A csv file to analyse", type=str)