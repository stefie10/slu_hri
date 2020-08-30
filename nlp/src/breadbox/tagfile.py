import annotation_reader
import sys
import datatypes_lmap
import cPickle

def main():
    flickr_fname = sys.argv[1]
    annotation_fname = sys.argv[2]
    out_fname = sys.argv[3]

    annotations = annotation_reader.from_file(annotation_fname)
    tags = annotations.tags()

    prior = cPickle.load(open(flickr_fname))
    lt = datatypes_lmap.flickr_cache(prior, tags)
    print "saving", out_fname
    cPickle.dump(lt, open(out_fname, 'wb'), 2)

if __name__ == "__main__":
    main()
