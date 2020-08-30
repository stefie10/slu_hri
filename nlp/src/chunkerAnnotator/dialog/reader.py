import xml.dom.minidom
import zipfile
from environ_vars import TKLIB_HOME
from routeDirectionCorpusReader import rowValues

class Dialog:
    def __init__(self, dialog_id, turns):
        self.id = dialog_id
        self.turns = turns

class Turn:
    def __init__(self, speaker, utterance, start, end, duration):
        self.speaker = speaker
        self.utterance = utterance
        self.start = start
        self.end = end
        self.duration = duration
        self.sdcs = []

    def setSdcs(self, sdcs):
        self.sdcs = sdcs

def getText(nodelist):
    rc = ""
    for node in nodelist:
        if node.nodeType == node.TEXT_NODE:
            rc = rc + node.data
    return rc

def extractField(parent, childName):
    return getText(parent.getElementsByTagName(childName)[0].childNodes)
        

def read(fname):
    ziparchive = zipfile.ZipFile(fname)
    xmldata = ziparchive.read("content.xml")

    
    doc = xml.dom.minidom.parseString(xmldata)
    dialogs = []
    for dialog_id, dialogTable in enumerate(doc.getElementsByTagName("table:table")[:4]):
        
        rows = dialogTable.getElementsByTagName("table:table-row")
        turns = []
        for i, r in enumerate([r for r in rows[1:]
                               if r.getElementsByTagName("table:table-cell")[0].hasChildNodes()]):
            values = rowValues(r)
            if len(values) == 5:
                speaker, text, start, end, duration = values
            elif len(values) == 6:
                rowid, speaker, text, start, end, duration = values
            elif len(values) == 1:
                break
            else:
                raise ValueError("Unexpected row", values)

            start = float(start)
            end = float(end)
            duration = float(duration)
            turn = Turn(str(speaker), str(text), start, end, duration)
            turns.append(turn)
        dialogs.append(Dialog(dialog_id, turns))
    return dialogs


def readDialogs(fname):
    from xml.dom.minidom import parseString
    from routeDirectionCorpusReader import loadSdc
    print "Loading", fname
    doc = parseString(open(fname).read())
    dialogs = []
    
    for dialog in doc.getElementsByTagName("dialog"):

        dialog_id = int(dialog.getAttribute("id"))
        turns = []
        for txml in dialog.getElementsByTagName("turn"):
            speaker = str(extractField(txml, "speaker"))
            utterance = str(extractField(txml, "utterance"))

            start = float(extractField(txml, "start"))
            end = float(extractField(txml, "end"))
            duration = float(extractField(txml, "duration"))


            sdcs = [loadSdc(a, utterance) for a  in
                    txml.getElementsByTagName("annotation")]
            turn = Turn(speaker, utterance, start, end, duration)
            turn.setSdcs(sdcs)
            turns.append(turn)
        dialogs.append(Dialog(dialog_id, turns))

    return dialogs
                       
                   



def main():
    dialogs = read("%s/data/matthias/transcriptions.ods" % TKLIB_HOME)

    for d in dialogs:
        for t in d.turns:
            print t.speaker, t.utterance, t.start, t.end, t.duration


if __name__ == "__main__":
    main()
    

    
