import sys

def main():
    outfile = sys.argv[1]

    results = [eval(line) for  line in open(outfile)]
    results = [(eval(srels), correct, resultfile) for srels, correct, resultfile in results]
    results.sort(key=lambda x: x[1], reverse=True)

    for srels, correct, resultfile in results:
        if len(srels) <= 1:
            print srels, correct, resultfile

    

if __name__== "__main__":
    main()
