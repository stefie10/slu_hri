import os
from muri import tkloader
import spatialRelationClassifier
import tag_util
import yaml
import preposition
import layers


def makeAssignment(dirname, tagFile, mapFile, engineMap):
    os.mkdir(dirname)
    tagFile = tag_util.tag_file("../data/directions/direction_floor_3/log4_s3.tag", "../data/directions/direction_floor_3/log4_s3.cmf")
    tagLayer = tkloader.loadTagLayer(tagFile.as_slimd_polygons(), "%s/tags" % dirname)
    
    i = 0
    for landmarkId, feature in enumerate(layers.features(tagLayer)):
        for name, engine in engineMap.iteritems():
            if i >= 220:
                exfname = "%s/landmark.%d.ex.%d" % (dirname, landmarkId, i)
                pmap, fLayers = preposition.loadInstance(exfname, engineMap, engine)

                f = open("%s/properties.yaml" % (exfname), "w")
                f.write(yaml.dump({"preposition":engine.name()}))
                f.close()


                groundLayer, geom = fLayers["ground"]
                groundLayer.startEditing()
                layers.addNewFeature(groundLayer, layers.getGeometry(feature.geometry()))
                groundLayer.commitChanges()

                figureLayer, geom = fLayers["figure"]
                figureLayer.startEditing()
                #layers.addNewFeature(figureLayer, [(0, 0)])
                figureLayer.commitChanges()

            i += 1
        if i >= 320:
            break
    


def main():
    makeAssignment("scratch.assignment", 
                   "../data/directions/direction_floor_3/log4_s3.tag", "../data/directions/direction_floor_3/log4_s3.cmf",
                   spatialRelationClassifier.engineMap)

if __name__=="__main__":
    main()
