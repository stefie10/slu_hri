from sys import argv 

if __name__=="__main__":

    if(len(argv)==3):
        inwords = open(argv[1], 'r')
        finwords =[]
        outfile = open(argv[2], 'w')
        
        for line in inwords:
            if(not line in finwords):
                outfile.write(line)
                finwords.append(line)

    else:
        print "usage\n\tpython strip_repeats.py infile outfile"
    
        
