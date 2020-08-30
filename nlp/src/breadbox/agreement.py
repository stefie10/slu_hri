from environ_vars import TKLIB_HOME
import glob
import annotation_reader
import interannotatorAgreement
import orange
import orangeUtils

class WizardOfOzLearner(orange.Learner):
    def __init__(self, answers):
        self.answers = answers
    def __call__(self, training_data, learnweight):
        return WizardOfOzClassifier(self.answers)
    

class WizardOfOzClassifier(orangeUtils.PythonClassifier):
    def __init__(self, training_table):
        self.training_table = training_table
        self.key_to_ex = dict([(ex["word"].value, ex) 
                               for i, ex in enumerate(training_table)])
    def classify(self, ex):
        answer = self.key_to_ex[ex["word"].value]
        return answer["class"]


def main():
    
    dirname = "%s/data/directions/breadbox" % TKLIB_HOME
    f1 = annotation_reader.from_file("%s/nouns_stefie10.txt" % dirname)
    f2 = annotation_reader.from_file("%s/nouns_dlaude.partial.txt" % dirname)
    assert f1.labels == f2.labels
    data = []
    for (w1, l1), (w2, l2) in zip(f1.data, f2.data):
        if l1 == "None" or l2 == "None":
            #continue
            pass
        if l1 != l2:
            print w1, l1, w2, l2

        data.append((l1, l2))
    print "rows", len(data)
    print "     raw:", interannotatorAgreement.A_o(data)
    print "multi pi:", interannotatorAgreement.MultiPi(data)
    print "   kappa:", interannotatorAgreement.Kappa(data)


    
if __name__ == "__main__":
    main()
