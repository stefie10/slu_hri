import re
import xml.dom.minidom
import zipfile

def rowValues(row):
    results = []
    for elt in row.getElementsByTagName("table:table-cell"):
        if elt.hasChildNodes():
            results.append(" ".join([x.childNodes[0].data 
                                     for x in elt.getElementsByTagName("text:p")
                                     if x.hasChildNodes()]))
        else:
            results.append("")
    return results
    



def extractCommandType(headerText):
    m = re.match("Command \d+ \((.*)\):", headerText)
    if m == None:
        raise ValueError("Pattern didn't match:  " + `headerText`)
    else:
        return m.group(1)


class Annotation:
    @staticmethod
    def parse(text):
        try:
            if text.strip() == "":
                return ""
            def listToTuple(obj):

                if isinstance(obj, list):
                    if all(isinstance(x, str) for x in obj) and len(obj) > 1:
                        return (obj[0], " ".join(obj[1:]))
                    else:
                        return tuple([listToTuple(x) for x in obj])
                else:
                    return obj

            tokens = [t for t in re.split("(\w+)|([)(])", text) 
                      if t != None and t.strip() != '']

            out = ""
            for t in tokens:

                if t == "(":
                    out += "["
                elif t == ")":
                    out = out[:-1] + "],"
                else:
                    out += '"%s",' % t

            if out[-1] == ",":
                out = out[:-1]


            out = eval(out)

            out = listToTuple(out)

            return out
        except:
            print "Error parsing", text
            raise
    def __init__(self, command, text):
        self.command = command
        self.text = text
        self.obj = Annotation.parse(text)

        
                 

class Command:
    def __init__(self, idx, questionType, commandType, command):
        self.questionType = questionType
        self.commandType = commandType
        self.command = command
        self.idx = idx

class Session:
    def __init__(self, timestamp, subjectIdx, commands):
        self.timestamp = timestamp
        self.subjectIdx = subjectIdx
        self.commands = commands
        for c in commands:
            c.session = self

            

class Corpus:
    def __init__(self, fname):
        ziparchive = zipfile.ZipFile(fname)
        xmldata = ziparchive.read("content.xml")
        doc = xml.dom.minidom.parseString(xmldata)
        
        table = doc.getElementsByTagName("table:table")[0]        
    
        rows = table.getElementsByTagName("table:table-row")

        
        values = [rowValues(r) for r in rows]

        values = [v for v in values if len(v) != 0 and v[0] != '']

        headers = values[0]

        print len(values), "values"
        
        self.sessions = []
        commandIdx = 0
        for subjectIdx, v in enumerate(values[1:]):
            timestamp = v[0]
            rawCommands = v[1:-1] # last is empty string
            assert len(rawCommands) == 50, len(rawCommands)
            commands = []
            for i in range(0, len(rawCommands), 2):
                command = rawCommands[i]
                questionType = rawCommands[i+1]
                commandType = extractCommandType(headers[i+1])
                commands.append(Command(commandIdx,
                                        questionType, commandType, command))
                commandIdx += 1
            self.sessions.append(Session(timestamp, subjectIdx, commands))

        self.commands = []
        for session in self.sessions:
            for c in session.commands:
                self.commands.append(c)

        self.questionTypes = set([c.questionType for c in self.commands])
        self.commandTypes = set([c.commandType for c in self.commands])

    
    def commandsForType(self, type):
        assert type in self.commandTypes, (type, self.commandTypes)

        return [c for c in self.commands if c.commandType == type]

    def loadAnnotations(self, fname):
        
        currentCommand = None
        currentText = None
        annotations = []
        for i, line in enumerate(open(fname, "r")):
            try:
                if line[0] in [str(i) for i in range(0, 10)]:

                    if currentCommand != None:
                        annotations.append(Annotation(currentCommand, currentText))
                    m = re.match("(\d+)(.*)", line)
                    idx = int(m.group(1))
                    currentCommand = self.commands[idx]
                    currentText = ""
                else:
                    currentText += line
            except:
                print "line", i
                raise
        return annotations



def main():
    from environ_vars import TKLIB_HOME
    corpus = Corpus("%s/data/verbs/corpus-11-2009.ods" % TKLIB_HOME)
    for c in corpus.commandsForType("Guiding people"):
        print c.idx, c.command

                
if __name__ == "__main__":
    main()
