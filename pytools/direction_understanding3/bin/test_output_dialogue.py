from du.dialogue_util import test_dialogue

#TODO
def main():
    from optparse import OptionParser
    parser = OptionParser(usage="usage: test_output_dialogue.py [options] output_fn")
#    parser.add_option("--sentence_number", type="string")
    
    (options, args) = parser.parse_args()
    print "args", args
    print "options", options.__dict__
    test_dialogue(*args, **options.__dict__)




if __name__=="__main__":
    main()

