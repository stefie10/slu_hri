from environ_vars import TKLIB_HOME
import annotation_reader
import orange
import orangeUtils
import orngEnsemble
import orngStat
import orngTest
import trainer

class PairwiseEngine():

    def __init__(self, training):
        self.training = training
        self.wnparents = trainer.WordnetParentsEngine(training)
        labels = ["Larger", "Smaller", "Equal", "None"]
        self.cls_variable = orange.EnumVariable("class", values=labels)
        
        alist = []
        for var in self.wnparents.domain.attributes:
            if isinstance(var, orange.FloatVariable):
                v1 = orange.FloatVariable(name="%s_w1" % var.name)
                v2 = orange.FloatVariable(name="%s_w2" % var.name)
                alist.append(v1)
                alist.append(v2)
            elif isinstance(var, orange.EnumVariable):
                v1 = orange.EnumVariable(name="%s_w1" % var.name, 
                                         values=var.values)
                v2 = orange.EnumVariable(name="%s_w2" % var.name, 
                                         values=var.values)
                alist.append(v1)
                alist.append(v2)
            else:
                raise ValueError("Unhandled attribute: " + `var`)
            
        self.domain = orange.Domain(alist,
                                    self.cls_variable)
        self.training_table = self.makeTable(self.training)

    def makeTable(self, annotations):
        table = orange.ExampleTable(self.domain)
        for i, (w1, l1) in enumerate(annotations.data):
            print "Doing", i, "of", len(annotations.data)
            for j, (w2, l2) in enumerate(annotations.data):
                ex = self.makeExample(w1, w2)
                cls = self.makeClass(l1, l2)
                table.append(ex)
        return table
    def makeExample(self, w1, w2):
        ex = orange.Example(self.domain)

        ex1 = self.wnparents.makeExample(w1)
        ex2 = self.wnparents.makeExample(w2)
        for var in self.wnparents.domain.attributes:
            ex["%s_w1" % var.name] = ex1[var.name]
            ex["%s_w2" % var.name] = ex2[var.name]

        return ex
    def makeClass(self, l1, l2):
        compare_l1_l2 = self.training.cmp(l1, l2)
        if compare_l1_l2 == 0:
            return "Equal"
        elif compare_l1_l2 == -1:
            return "Smaller"
        elif compare_l1_l2 == 1:
            return "Bigger"
        elif compare_l1_l2 == None:
            return "None"
        else:
            raise ValueError("Unexpected cmp result: "+`compare_l1_l2`)
            
def main():
    print "loading"
    annotations = annotation_reader.from_file("%s/data/directions/breadbox/nouns_stefie10.txt" % TKLIB_HOME)
    table = annotations.as_orange_table()
    cv_indices = orange.MakeRandomIndices2(table, p0=0.5)
    print "indices", set(cv_indices)
    print "splitting"
    training, testing = annotation_reader.split(annotations, cv_indices)
    print "features"

    engine = PairwiseEngine(training)
    
    training_table = engine.training_table
    testing_table = engine.makeTable(testing)
    print len(training_table), "training"
    print len(testing_table), "testing"
    
    learners = [orange.MajorityLearner(),
                orngEnsemble.RandomForestLearner(),
                ]
    results = orngTest.learnAndTestOnTestData(learners, 
                                              training_table, testing_table)

    for accuracy, cm in zip(orngStat.CA(results),
                            orngStat.confusionMatrices(results)):
        print orangeUtils.confusion_matrix_to_string(table.domain, cm)
        print "accuracy: %.2f%%" % (accuracy*100)

    
    

    
if __name__ == "__main__":
    main()    
    
    
