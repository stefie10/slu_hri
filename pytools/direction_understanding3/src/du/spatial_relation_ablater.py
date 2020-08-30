import evaluate_model
import math2d



def main():
    from sys import argv
    corpus_fname = argv[1]
    model_fname = argv[2]
    groundtruth_tag_fn = argv[3]
    map_fname = argv[4]

    evaluator = evaluate_model.Evaluator(corpus_fname, model_fname, groundtruth_tag_fn, map_fname, 
                                         evaluation_mode="specialized")
    evaluate_model.evaluator = evaluator
    
    sr_classifier = evaluator.dg_model.sr_class
    engineMap = sr_classifier.engineMap
    out = []    

    #for subset in [set(engineMap.keys()) - set(["through"])]:
    
    #for subset in [[x] for x in engineMap.keys()]:
    for subset in math2d.powerset(engineMap.keys()):
        if len(subset) > 3 or "turnRight" in subset or "turnLeft" in subset or "straight" in subset:
            continue
        subset_engine_map = dict([(key, None) for key in engineMap.keys()])

        for key in subset:
            subset_engine_map[key] = engineMap[key]
        
        print "expect to call setter"
        print 'cls', sr_classifier
        print 'cls', sr_classifier.engineMap
        sr_classifier.set_engine_map(subset_engine_map)
        run_description = str(subset)
        

        evaluator.run_description = run_description

        print "starting", evaluator.run_description
        correct_count, out_fname = evaluator.evaluateParallel()
        out.append((run_description, correct_count, out_fname))
        break
    out.sort(key=lambda x: x[1], reverse=True)
    for x in out:
        print x

        

    

    

    
if __name__== "__main__":
    main()
