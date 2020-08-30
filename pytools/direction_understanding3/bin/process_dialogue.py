from du.dialogue_util import process_dialogue


def main():
    from optparse import OptionParser
    parser = OptionParser(usage="usage: dialog.py [options] top_n_file_name ,model_fn, gtruth_tag_fn, output_dir")
    parser.add_option("--num_to_generate", type="string")
    parser.add_option("--num_to_ask", type="string")
    parser.add_option("--sent_number", type="string")
    parser.add_option("--objective", type="string")
    
    (options, args) = parser.parse_args()
    print "args", args
    print "options", options.__dict__
    process_dialogue(*args, **options.__dict__)


if __name__=="__main__":
    main()




