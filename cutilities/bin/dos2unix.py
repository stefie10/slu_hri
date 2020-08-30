from sys import argv

def dos2unix(infilename, outfilename):
    infile = open(infilename, 'r')
    outfile = open(outfilename, 'w')

    current_line = infile.read();
    myfile = current_line.split(str(chr(13)))
    
    for line in range(len(myfile)):
        outfile.write(myfile[line]+"\n")
        
if __name__=="__main__":

    if(len(argv) == 3):
        filename_in = argv[1]
        filename_out = argv[2]

        dos2unix(filename_in, filename_out)

    else:
        print "usage\n\t>>python dos2unix filename_in filename_out"
