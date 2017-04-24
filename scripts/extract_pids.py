import os
import sys


def main(filename, format):
    record = False
    topicid = ""
    rank = 0

    with open(filename, "r") as f:
        while f:
            line = f.readline()
            if not line:
                break
            if record:
                if format == 'TREC':
                    rank = rank + 1
                    score = -float(rank)+0.0
                    print("{0} NF {1} {2} {3} pubmed".format(topicid, line.strip(), rank, score ))
                else:
                    print("{0} {1}".format(topicid, line.strip()))

            if line.startswith("Topic:"):
                topicid = line.split()[1].strip()

            if line.startswith("Pids:"):
                record = True

if __name__ == "__main__":
    filename = None
    format = "TOP"
    if len(sys.argv) >= 2:
        filename = sys.argv[1]

    if len(sys.argv)==3:
        format = sys.argv[2].upper()

    if os.path.exists( filename ) and format in ['TREC', 'TOP']:
        main(filename,format)
    else:
        print("Usage: {0} <filename> <format> where <format> is TREC or TOP".format(sys.argv[0]))