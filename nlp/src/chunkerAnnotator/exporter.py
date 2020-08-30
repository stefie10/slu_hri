from routeDirectionCorpusReader import readSession
from xml.dom.minidom import Document


def main():
    fname = "data/Direction understanding subjects Floor 8 (Final).ods"
    #fname = "data/Direction understanding subjects Floor 1 (Final).ods"
    sessions = readSession(fname, "crf_chunker")
    sent_num = 0
    doc = Document()

    routeInstructionsXml = doc.createElement("routeInstructions")
    for session in sessions:
        sessionXml = doc.createElement("session")
        sessionXml.setAttribute("subject", session.subject)
        for instructionIdx, instruction in enumerate(session.routeInstructions):
            
            instructionXml = doc.createElement("instruction")
            instructionXml.setAttribute("instruction_id", `sent_num`)
            
            textXml = doc.createElement("text")
            textXml.appendChild(doc.createTextNode(instruction))
            instructionXml.appendChild(textXml)

            sdcXml = doc.createElement("sdcs")
            for annotation in session.routeAnnotations[instructionIdx]:
                sdcXml.appendChild(annotation.toXml(doc))
            
            instructionXml.appendChild(sdcXml)
            
            sent_num += 1
            sessionXml.appendChild(instructionXml)
        routeInstructionsXml.appendChild(sessionXml)
    doc.appendChild(routeInstructionsXml)
    outfile = open("out.xml", "w")
    outfile.write(doc.toprettyxml())
    outfile.close()

if __name__ == "__main__":
    main()
