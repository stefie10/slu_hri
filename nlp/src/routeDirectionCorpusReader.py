import xml.dom.minidom
from xml.dom.minidom import Document, parse 

import zipfile
import os.path
def wordcount(str):
    return len(str.split())


def textFromNode(node):
    text = ""
    for textNode in node.getElementsByTagName("text:p"):
        for child in textNode.childNodes:
            if hasattr(child, "data"):
                text += child.data
                break
    return str(text)

def rowValues(row):
    return [textFromNode(elt)
            for elt in row.getElementsByTagName("table:table-cell")
            if elt.hasChildNodes()]

def descendentMap(sdcs):
    """
    Take a list of sdcs and return a map of ancestors to descendents,
    using the contains relation.  An SDC is a child of another SDC if
    it is completely contained in one of its fields.  A child SDC will
    appear with its parent, grandparent, etc.
    """
    sdc_to_descendents = dict([(sdc, []) for sdc in sdcs])
    for sdc in sdcs:
        for possible_ancestor in sdc_to_descendents:
            if possible_ancestor.contains(sdc):
                sdc_to_descendents[possible_ancestor].append(sdc)
    return sdc_to_descendents

def ancestorMap(sdcs):
    """
    Take a list of sdcs and return a map of descendents to ancestors
    using the contains relation.  An SDC is a child of another SDC if
    it is completely contained in one of its fields.  A child SDC will
    appear with its parent, grandparent, etc.
    """
    sdc_to_ancestors = dict([(sdc, []) for sdc in sdcs])
    for sdc in sdcs:
        for possible_descendent in sdc_to_ancestors:
            if sdc.contains(possible_descendent):
                sdc_to_ancestors[possible_descendent].append(sdc)
    return sdc_to_ancestors

def childrenMap(sdcs):
    """
    Take a list of SDCs and return a map of parents to children. A
    child SDC will not appear with its grandparent, only its parent.
    """
    sdc_to_descendents = descendentMap(sdcs)
    sdc_to_children = dict([(sdc, []) for sdc in sdcs])

    for sdc in sdcs:
        potentialParent = None
        for parent, children in sdc_to_descendents.iteritems():
            if sdc in children:
                if potentialParent == None:
                    potentialParent = parent
                else:
                    if potentialParent.contains(parent):
                        potentialParent = parent
                    else:
                        assert parent.contains(potentialParent)
        if potentialParent != None:
            sdc_to_children[potentialParent].append(sdc)
    return sdc_to_children


def loadSdc(xmlElement, text):
    argMap = {}
    for field in xmlElement.childNodes:
        if isinstance(field, xml.dom.minidom.Element):
            start = int(field.getAttribute("start"))
            end = int(field.getAttribute("end"))
            argMap[str(field.nodeName)] = TextStandoff(text,(start, end))

    return Annotation(**argMap)

class Session:
    """
    A session is a set of instructions from a single subject. 
    
    A session consists of a list of route instructions. Each route
    instruction is a string consisting of natural language directions
    between two points in the map.
    """    
    def __init__(self, fname, quadrant, annotationSource, rowIdx, row, wasFollowed, columnLabels=None):
        self.fname = fname
        dirname, basename = os.path.split(fname)
        self.annotationSource = annotationSource
        self.row = row
        self.rowIdx = rowIdx
        self.columnLabels = columnLabels

        
        self.annotationFname = "%s/annotations.%s.%s.%d.xml" %  \
            (dirname, annotationSource, basename, self.rowIdx)

        values = rowValues(row)
        self.timestamp, self.subject, self.floor = values[0:3]
            
        self.routeInstructions = values[3:]
        self.startRegionTags = []
        self.endRegionTags = []
        
        for i, r in enumerate(self.routeInstructions):
            self.routeInstructions[i]=r.strip()
            startRegionTag, endRegionTag = self.columnLabels[i].split("to")
            self.startRegionTags.append(startRegionTag.strip())
            self.endRegionTags.append(endRegionTag.strip())
            

        self.followed = [None for x in range(len(self.routeInstructions))]
        if wasFollowed != None:
            followedValues = rowValues(wasFollowed)
            followed = followedValues[1:len(self.routeInstructions)]
            
            for i, f in enumerate(followed):
                f = f.strip()
                if f == '-1':
                    value = "not followed"
                elif f == '1':
                    value = "followed"
                elif f == '0':
                    value = "questionable"
                else:
                    raise ValueError("Unexpected value: " + `f`)

                self.followed[i] = value
            


        if quadrant != None:
            split = len(self.routeInstructions)/2
            if quadrant in (0, 2):
                self.routeInstructions = self.routeInstructions[:split]
                self.columnLabels = columnLabels[:split]
                self.followed = self.followed[:split]
            elif quadrant in (1, 3):
                self.routeInstructions = self.routeInstructions[split:]
                self.columnLabels = columnLabels[split:]
                self.followed = self.followed[split:]
            else:
                raise ValueError("Quadrant: " + `quadrant`)



        # got to load.

        if os.path.exists(self.annotationFname):
            self.loadAnnotations(self.annotationFname)
        else:
            self.clearAnnotations()
    @property
    def key(self):
        return "%s[%d]" % (self.fname, self.rowIdx)

    def __str__(self):
        mystr= "*******************************\n"
        mystr += "-->timestamp:"+ str(self.timestamp)+"\n"
        mystr += "-->subject:"+ str(self.subject)+"\n"
        
        for elt in self.routeInstructions:
            currelt = elt.replace("\n", " ")
            mystr += "-->elt:"+ str(currelt)+"\n"
            
        return mystr

    def __repr__(self):
        return self.__str__()

    def addAnnotation(self, instructionIdx, annotation):
        self.routeAnnotations[instructionIdx].append(annotation)

    def deleteAnnotation(self, instructionIdx, i):
        print "i", i
        del self.routeAnnotations[instructionIdx][i]
    def clearAnnotations(self):
        self.routeAnnotations = dict([(i, []) for i, instruction 
                                      in enumerate(self.routeInstructions)])


    def saveAnnotations(self):
        file = open(self.annotationFname, "w")
        doc = Document()
        session = doc.createElement("session")
        for id, annotations in self.routeAnnotations.iteritems():
            instruction = doc.createElement("instruction")
            for annotation in annotations:
                instruction.appendChild(annotation.toXml(doc))
            session.appendChild(instruction)
        doc.appendChild(session)
        # print "xml", doc.toprettyxml(indent="  ")
        file.write(doc.toprettyxml(indent="  "))
        file.close()
        
    def loadAnnotations(self, fname):
        self.clearAnnotations()
        document = parse(fname)
        for i, instruction in enumerate(document.getElementsByTagName("instruction")):
            for j, annotation in enumerate(instruction.getElementsByTagName("annotation")):
                argMap = {}
                for field in annotation.childNodes:
                    if isinstance(field, xml.dom.minidom.Element):
                        start = int(field.getAttribute("start"))
                        end = int(field.getAttribute("end"))
                        argMap[str(field.nodeName)] = Standoff(self, i, (start, end))

                self.addAnnotation(i, Annotation(**argMap))
        return []


def parent_in_set(candidate, sdcs):
    for possible_parent in sdcs:
        if possible_parent.range.contains(candidate.range):
            if possible_parent.range != candidate.range:
                return True
    return False
                

def makeProperty(key):
    def getx(self):
        return self.annotationMap[key]
    def setx(self, x):
        print "setter!!!"
        self.annotationMap[key] = x
    return property(getx, setx)    

class Annotation:

    keys = ["figure", "verb", "spatialRelation", "landmark", "landmark2"]
    abbrvKeys = ["F", "V", "SR", "L", "L2"]
    
    
    for key in keys:
        exec("%s = makeProperty(\"%s\")" % (key, key))

    def __init__(self, **args):
        self.annotationMap = args
        self.entireText = None
        self.instructionIdx = None


        for key, value in self.annotationMap.iteritems():
            if not(value is None):
                if self.entireText is None:
                    self.entireText = value.entireText
                else:
                    assert self.entireText == value.entireText, (self.entireText, value.entireText)                
        
        for key in Annotation.keys:
            if not (key in self.annotationMap) or self.annotationMap[key] is None:
                self.annotationMap[key] = TextStandoff(self.entireText, (0, 0))
         

        self.range = TextStandoff(self.entireText, 
                                  enclosingRange(self.annotationMap.values()))
        
    def asPrimitives(self):
        return dict((key, value.asPrimitives()) 
                    for key, value in self.annotationMap.iteritems())
    @staticmethod
    def fromPrimitives(args):
        args = dict([(str(key), TextStandoff.fromPrimitives(value)) 
                     for key, value in args.iteritems()])
        return Annotation(**args)
        
        
    @property
    def text(self):
        return self.range.text

    def __getitem__(self, key):
        return self.annotationMap[key]

    @property
    def standoffs(self):
        return [self.annotationMap[key] for key in Annotation.keys]

    def __str__(self):
        out = ""
        for i, k in enumerate(self.keys):
            keyName = self.abbrvKeys[i]
            out += "%s='%s', " % (keyName, self.annotationMap[k].text)

        return out

    def __repr__(self):
        return self.__str__()
    def toXml(self, doc):
        annotation = doc.createElement("sdc")
        for key in Annotation.keys:
            element = doc.createElement(key)
            self.annotationMap[key].toXml(element)
            annotation.appendChild(element)
        return annotation

    """
    Return true if any single standoff in self completely contains all
    of annotation.  Note that this is not the same as
    self.range.contains(standoff.range).
    An annotation never contains itself. 
    """
    def contains(self, annotation):
        if self == annotation:
            return False
        else:
            for standoff in self.annotationMap.values():
                if standoff.contains(annotation.range):
                    return True
            return False

    def fieldForChild(self, annotation):
        """
        Retrun the field that this annotation is a child of, or None.
        """
        if self == annotation:
            return False
        else:
            for name, standoff in self.annotationMap.iteritems():
                if standoff.contains(annotation.range):
                    return name
            return None
        
    def degreeOfOverlap(self, annotation):
        """
        Returns the total overlap between each corresponding field. 
        """ 
        overlaps = [self.annotationMap[key].degreeOfOverlap(annotation.annotationMap[key]) 
                    for key in Annotation.keys]
        return sum(overlaps)
    
            


def makeNullStandoff(session, instructionIdx):
    return Standoff(session, instructionIdx, (0, 0))

def makeNullTextStandoff(text):
    return TextStandoff(text, (0, 0))

def enclosingRange(standoffs):
    starts = [standoff.start for standoff in standoffs if not standoff.isNull()]
    ends = [standoff.end for standoff in standoffs if not standoff.isNull()]
    if len(starts) == 0 or len(ends) == 0:
        return 0,0
    else:
        return min(starts), max(ends)

from standoff import TextStandoff

class Standoff(TextStandoff):
    def isNull(self):
        return self.range == (0, 0)

    def __init__(self, session, instructionIdx, range):
        self.session = session
        self.instructionIdx = instructionIdx
        self.range = range
        self.entireText = self.session.routeInstructions[self.instructionIdx]




class Direction:
    """
    Okay.  So I should have designed a direction class from the
    begining but I didn't. This will go on top of the original API so
    we can pretend we have that layer.
    """
    def __init__(self, session_idx, instruction_idx, overall_idx, txt, was_followed, subject, start, end):
        self.session_idx = session_idx
        self.instruction_idx = instruction_idx
        self.overall_idx = overall_idx
        self.was_followed = was_followed
        self.subject = subject
        self.start = start
        self.end = end


class SessionGroup:
    def __init__(self, sessions):
        self.sessions = sessions
        self.sessionMap = dict((session.key, session) for session in self.sessions)
        self.annotationSource = None
        self.fname = None
        for s in sessions:
            if self.annotationSource == None:
                self.annotationSource = s.annotationSource
            else:
                assert self.annotationSource == s.annotationSource

        for s in sessions:
            if self.fname == None:
                self.fname = s.fname
            else:
                if self.fname != s.fname:
                    self.fname = None
                    break
        self.directions = []
        idx = 0
        for session_idx, session in enumerate(self.sessions):
            for instruction_idx in range(len(session.routeInstructions)):
                start, end = session.columnLabels[instruction_idx].split("to")
                dir = Direction(session_idx, instruction_idx, idx, 
                                session.routeInstructions[instruction_idx],
                                session.followed[instruction_idx],
                                session.subject, start.strip(), end.strip())
                self.directions.append(dir)
                idx += 1
    def __iter__(self):
        return iter(self.sessions)
    def __getitem__(self, idx):
        if isinstance(idx, Session):
            return self.sessionMap[idx.key]
        else:
            return self.sessions[idx]

    def __len__(self):
        return len(self.sessions)

    def __str__(self):
        mystr = ""
        for elt in self.sessions:
            mystr += str(elt)

        return mystr
            
    def sdcs(self):
        for session in self.sessions:
            for instructionIdx, instruction in enumerate(session.routeInstructions):
                sdcs = session.routeAnnotations[instructionIdx]
                yield session, instructionIdx, instruction, sdcs
    def __repr__(self):
        return self.__str__()




def readSession(fname, annotationPrefix, quadrant=None):
    ziparchive = zipfile.ZipFile(fname)
    xmldata = ziparchive.read("content.xml")

    doc = xml.dom.minidom.parseString(xmldata)



    worksheets = doc.getElementsByTagName("table:table")

    corpusRows = worksheets[0].getElementsByTagName("table:table-row")
    header = corpusRows[0]
    data = corpusRows[1:]

    if len(worksheets) >= 2:
        correctnessSheet = doc.getElementsByTagName("table:table")[1]
        correctness_rows = worksheets[1].getElementsByTagName("table:table-row")[1:]
        print correctness_rows[0]
    else:
        correctness_rows = [None for d in data]

    headerValues = rowValues(header)
    #print "hv:", headerValues

    all_sessions = [Session(fname, quadrant, 
                            annotationPrefix, i, r, correctness_rows[i], 
                            headerValues[3:])
                    for i, r in enumerate(data) 
                    if r.getElementsByTagName("table:table-cell")[0].hasChildNodes()]
    if quadrant != None:
        split = len(all_sessions)/2
        print "split", split
        if quadrant in (0, 1):
            sessions = all_sessions[:split]
        elif quadrant in (2, 3):
            sessions = all_sessions[split:]
        else:
            raise ValueError("Bad value for quadrant: " + `quadrant`)
    else:
        sessions = all_sessions
    
    return SessionGroup(sessions)
