__author__ = "Leif Azzopardi"

import os
import sys


def main(filename):
    with open(filename, "r") as f:
        while f:
            line = f.readline()
            if not line:
                break

            parts = line.split()
            if parts[3].strip() == "1":
                print(line.strip())

if __name__ == "__main__":
    filename = None
    if len(sys.argv) == 2:
        filename = sys.argv[1]
    else:
        print("Usage: {0} <filename>".format(sys.argv[0]))
        print("Takes the qrel file and extracts only the relevant items marked 1")


    if os.path.exists( filename ):
        main(filename)
    else:
        print("File not found {0}".format(filename))