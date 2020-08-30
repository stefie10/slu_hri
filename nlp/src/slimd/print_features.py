from spatialRelationClassifier import SpatialRelationClassifier

def print_features_for_engine(engine, ofile, processed_fnames):
    
    print "flist", engine.flist()

    all_added_fnames = set()
    for group in engine.flist().groups:
        groupstr = ""

        added_fnames = set()
        summary_fnames = []
        for fname in group.names():
            if fname in engine.masterList:
                groupstr += ("\item {\\bf %s}: %s\n" %
                             (fname, engine.flist().description(fname)))
                added_fnames.add(fname)
                #summary_fnames.append(fname)

        if groupstr != "" or len(summary_fnames) != 0:
            all_added_fnames.update(added_fnames)
            gname = str(group.__class__).split(".")[-1]
            #ofile.write("\subsubsection{%s}\n" % gname)
            #ofile.write(str(group.__class__.__doc__) + "\n")
            ofile.write("\\begin{itemize}\n");
            if groupstr != "":
                ofile.write(groupstr)
            if len(summary_fnames) != 0:
                ofile.write("\item {\\bf Others:} ")
                ofile.write(", ".join(["%s" % x for x in summary_fnames]))
                ofile.write("\n")
            ofile.write("\\end{itemize}\n");
    return all_added_fnames

def main():
    sr_class = SpatialRelationClassifier()
    ofile = open("features.tex", "w")
    processed_fnames = set()
    for e in sorted(sr_class.engineMap.values(), key=lambda e: e.name()):
        ofile.write("\\subsection{%s}\n" % e.name())
        doc = e.__class__.__doc__
        if doc != None:
            ofile.write(doc + "\n")
        print "e", e, len(e.masterList),len(e.domain())
        print processed_fnames
        added_fnames = print_features_for_engine(e, ofile, processed_fnames)
        processed_fnames.update(added_fnames)
        ofile.write("\n");
    ofile.close()
        
if __name__ == "__main__":
    main()

