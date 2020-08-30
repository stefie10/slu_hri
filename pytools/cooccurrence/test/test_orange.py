from os import *
'''import orange


dom = ["test1", "test2"]

 
mydomain = orange.Domain(map(orange.FloatVariable, dom), 
                         orange.EnumVariable("class", values=["-1","1"]))

table = orange.ExampleTable(mydomain)

ex1 = orange.Example(mydomain, [0,2,"-1"])
ex2 = orange.Example(mydomain, [1,2,"1"])
ex3 = orange.Example(mydomain, [0,10,"1"])
ex4 = orange.Example(mydomain, [0,0,"-1"])

table.append(ex1)
table.append(ex2)

print table.domain.attributes
print table.domain.classVar

classifier = orange.BayesLearner(table)
classifier.show()'''


# Description: Shows how to convert ExampleTable into matrices
# Category:    basic classes, preprocessing
# Classes:     ExampleTable
# Uses:        iris, heart_disease
# Referenced:  ExampleTable.htm

import orange
import orange, random

random.seed(0)
values = ["0", "1"]
mynames = ["orange", "green", "red", "yellow", "black", "magenta"]
attributes = [orange.EnumVariable(mynames[i], values = values)
              for i in range(6)]
classattr = orange.EnumVariable("classname", values = ["0", "1"])
domain = orange.Domain(attributes + [classattr])


print "attributes", attributes
print "classattr", classattr
print "domain:", domain

card = [1, 1, 1, 1, 1, 1]
data = orange.ExampleTable(domain)
for i in range(5):
    ex = [random.randint(0, c) for c in card]
    ex.append(ex[0]==ex[1] or ex[4]==0)
    data.append(ex)

for ex in data:
    print ex

classifier = orange.BayesLearner(data)
print classifier(data[0], orange.GetBoth)



