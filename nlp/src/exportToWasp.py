from routeDirectionCorpusReader import readSession
from xml.dom.minidom import Document

def exportSdcAsWasp(sdc):
    result = "PATH("

    args = []
    if sdc.figure.text.strip() != "":
        args.append('f="%s"' % sdc.figure.text)
    if sdc.spatialRelation.text.strip() != "":
        args.append('r="%s"' % sdc.spatialRelation.text)
    elif sdc.verb.text.strip() != "":
        args.append('r="%s"' % sdc.verb.text)

    if sdc.landmark.text.strip() != "":
        args.append('l="%s"' % sdc.landmark.text)
        
    result += ",".join(args)
    result += ")"
    return result

def main():
    fname = "data/Direction understanding subjects Floor 8 (Final).ods"
    sessions = readSession(fname, "stefie10")
    doc = Document()
    examples = doc.createElement("examples")
    doc.appendChild(examples)

    exampleId = 0
    for session in sessions:
        for instructionIdx, sdcs in session.routeAnnotations.iteritems():
            for sdc in sdcs:
                if sdc.text.strip() != "":
                    example = doc.createElement("example")
                    example.setAttribute("id", "%d" % exampleId)
                    examples.appendChild(example)

                    nl = doc.createElement("nl")
                    nl.setAttribute("lang", "en")
                    nl.appendChild(doc.createTextNode(sdc.text))
                    example.appendChild(nl)

                    mrl = doc.createElement("mrl")
                    mrl.setAttribute("lang", "edu.mit.csail.ar.language.waspParser.SdcGrammar")

                    mrl.appendChild(doc.createTextNode(exportSdcAsWasp(sdc)))
                    example.appendChild(mrl)


                
                print sdc
                exampleId += 1

    output_fname = "out.xml"
    output_file = open(output_fname, "w")
    output_file.write(doc.toprettyxml(indent=" "))
    output_file.close()                
    
if __name__ == "__main__":
    main()
