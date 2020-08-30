import cPickle
from sys import argv
from environ_vars import TKLIB_HOME
import cProfile

"""
This is designed to replace all the create model scripts. 
"""

if __name__ == "__main__":
    print "argv", len(argv), argv
    try:
        import psyco
        psyco.full()
    except:
        print "warning, no psyco"

    m = None
    outfilename = ""
    model_name = argv[1]
    try:
        print "importing"
        exec("import du.models.%s" % model_name)        
        model_class = eval("du.models.%s.model" % (model_name))
    except ImportError:
        print "import error"
        exec("import du.models_test.%s" % model_name)
        print "imported"
        model_class = eval("du.models_test.%s.model" % (model_name))
        print "evaled"
        
    print "---------->", model_class
    
    modelobj = {}
    def make_model():
        """ magic to use cProfile """
        m = model_class(*argv[2:-1])
        modelobj["model"] = m

    #cProfile.run('make_model()', 'out.prof')
    make_model()

    m = modelobj["model"]

    m.unload()
    if(not m == None):
        real_outfilename = argv[-1]
        print "saving", real_outfilename
        #cPickle.dump(m, open(real_outfilename, 'wb'))
        cPickle.dump(m, open(real_outfilename, 'wb'), 2)
