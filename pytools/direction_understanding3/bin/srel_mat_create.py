import du
from sys import argv

def main():
    import cPickle
    try:
        import psyco
        psyco.full()
    except:
        print "warning, no psyco"
    if len(argv) == 2:
        try:
            dg_model = cPickle.load(open(argv[1], 'r'))
        except:
            print argv[1]
            raise
            
        dg_model.create_srel_given_lmark_vpts_matrix()
    else:
        print "usage: srel_mat_create.py model_file.pck"


if __name__ == "__main__":
    main()
