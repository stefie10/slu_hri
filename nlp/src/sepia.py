#!/usr/bin/env python

import os
import sys
import popen2
import time

rake_path = "lexicon"
print "path", rake_path

#stdin, stdout = os.popen2("cd %s && rake -s parser" % (rake_path))
process = popen2.Popen3("cd %s && rake -s parser" % (rake_path))
stdin = process.tochild
stdout = process.fromchild
time.sleep(0.2)
if process.poll() != -1:
    raise RuntimeError("Sepia died for some reason, check logs.")



def parse(string):
    stdin.write(string.replace("\n", " ").encode("utf-8") + "\n")
    stdin.flush()
    parse = stdout.readline()[0:-1]
    offset, length = stdout.readline()[0:-1].split(" ")
    return parse, (int(offset), int(length))

if __name__ == "__main__":
    while True:
        s = sys.stdin.readline()
        print parse(s)


    
