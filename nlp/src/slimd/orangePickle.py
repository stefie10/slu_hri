class PickleableClassifier:
    def __init__(self, table, learner):
        self.table = table
        self.learner = learner
        self._classifier = None
    def reloadClassifier(self):
        self._classifier = self.learner(self.table)
        
    def loadClassifier(self):
        if self._classifier == None:
            self.reloadClassifier()
    @property 
    def classVar(self):
        self.loadClassifier()
        return self.classifier.classVar

    @property 
    def distribution(self):
        self.loadClassifier()
        return self.classifier.distribution

        
    @property
    def name(self):
        self.loadClassifier()
        return self.classifier.name

    @property
    def classifier(self):
        self.loadClassifier()
        return self._classifier

    def __call__(self, *args, **margs):
        return self.classifier(*args, **margs)

