from du.models import hri2010_global
from environ_vars import TKLIB_HOME
from flickrLda.ldaModel import LdaModel

class model(hri2010_global.model):

    def p_can_see_tag(self, tag, vtags, itags):
        if not hasattr(self, "_ldamodel"):
            self._ldamodel = LdaModel("%s/nlp/data/flickrLda.keywords/model-01800" % TKLIB_HOME)
        model = self._ldamodel
                
        if tag in vtags:
            O_mat_entry = 1 - 1e-6
        elif tag in itags:
            O_mat_entry = 1e-8
        else:                
            vtags = [t for t in vtags
                     if t in model.model.wordToIdx]

            if len(vtags) != 0 and tag in model.model.wordToIdx:
                O_mat_entry = model.p_obj1_given_objects_marginalize_topics(tag,
                                                                            vtags)
            else:
                O_mat_entry = 1e-8
                        
        return O_mat_entry
        
