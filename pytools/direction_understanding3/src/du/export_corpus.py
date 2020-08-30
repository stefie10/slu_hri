from routeDirectionCorpusReader import readSession
from xml.dom.minidom import Document
from tag_util import tag_file
import cPickle
def toXml(extendedAnnotations, doc):

    extendedAnnotationsXml = doc.createElement("routeDirections")

    for instruction in extendedAnnotations:
        if not 'landmark' in instruction:
            raise ValueError("Expected landamrk: " + `instruction`)

        instructionXml = doc.createElement("routeDirection")
        instructionTextXml = doc.createElement("directionText")
        instructionTextXml.appendChild(doc.createTextNode(instruction['sentence']))
        instructionXml.appendChild(instructionTextXml)
                                   
        assert len(instruction['landmark']) == len(instruction['SDCs_gt'])
        assert len(instruction['path_end']) == len(instruction['SDCs_gt'])
        assert len(instruction['path_start']) == len(instruction['SDCs_gt'])            
        path = instruction['path']

        pathXml = doc.createElement("path")
        for x, y, yaw, timestamp in path:
            pointXml = doc.createElement("point")
            pointXml.setAttribute('x', str(x))
            pointXml.setAttribute('y', str(y))
            pointXml.setAttribute('yaw', str(yaw))
            pointXml.setAttribute('timestamp', str(timestamp))
            pathXml.appendChild(pointXml)
        instructionXml.appendChild(pathXml)

        annotationsXml = doc.createElement("annotations")
        instructionXml.appendChild(annotationsXml)

        for sdc, landmark, path_start, path_end in zip(instruction['SDCs_gt'],
                                                       instruction['landmark'],
                                                       instruction['path_start'],
                                                       instruction['path_end']):
        
            annotationXml = doc.createElement("annotation")
            annotationXml.setAttribute("pathStartIndex", str(path_start[-1]))
            annotationXml.setAttribute("pathEndIndex", str(path_end[-1]))
            annotationXml.appendChild(sdc.toXml(doc))

            

            landmarkXml = doc.createElement("landmark")
            annotationXml.appendChild(landmarkXml)
            for lx, ly in landmark:
                pointXml = doc.createElement("point")
                pointXml.setAttribute("x", str(lx))
                pointXml.setAttribute("y", str(ly))
                landmarkXml.appendChild(pointXml)

                
            annotationsXml.appendChild(annotationXml)
        extendedAnnotationsXml.appendChild(instructionXml)


    return extendedAnnotationsXml
    

def main():
    from sys import argv
    map_fname = argv[1]
    tag_fname = argv[2]
    region_tag_fname = argv[3]
    extended_annotation_fname = argv[4]
    out_fname = argv[5]


    
    tagFile = tag_file(tag_fname, map_fname)

    #regionTagFile = tag_file(region_tag_fname, map_fname)
    
    extendedAnnotations = cPickle.load(open(extended_annotation_fname))


    doc = Document()
    corpusXml = doc.createElement("corpus")

    tagFileXml = tagFile.toXml(doc)
    tagFileXml.setAttribute("name", "objects")
    corpusXml.appendChild(tagFileXml)

    #regionTagFileXml = regionTagFile.toXml(doc)
    #regionTagFileXml.setAttribute("name", "regions")
    #corpusXml.appendChild(regionTagFileXml)
    

    corpusXml.appendChild(toXml(extendedAnnotations, doc))
    doc.appendChild(corpusXml)

    
    outfile = open(out_fname, "w")
    outfile.write(doc.toprettyxml())
    outfile.close()

if __name__ == "__main__":
    main()
