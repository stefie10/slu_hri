from eventLogic.expressions import Primitive, Or, Not, AndR, Tense
from eventLogic.spanningInterval import SpanningInterval, SpanningIntervalSet, \
    allIntervals


def inference(model, expression):
    """
    Perform inference, finding the set of intervals where expression is true in model 
    """
    
    if isinstance(expression, Primitive):
        results = []
        for entry in model.entries:
            if entry.primitive == expression:
                results.append(entry.spanningInterval)
    elif isinstance(expression, Or):
        results = []
        results.extend(inference(model, expression.e1))
        results.extend(inference(model, expression.e2))

    elif isinstance(expression, Not):
        results = []
        
        iprimes = [i.complement().condensed() for i in inference(model, expression.e)]
        indices = [0 for x in iprimes]
        if len(iprimes) == 0:
            return allIntervals
        cnt = 0
        while indices[0] < len(iprimes[0]):
            #print "indices", indices
            currentArgs = []            
            for i, j in enumerate(indices):
                currentArgs.append(iprimes[i][j])
            result = currentArgs[0]
            for interval in currentArgs[1:]:
                result = SpanningInterval.intersection(result, interval)
            #print "result", result
            results.append(result)
            for i, idx in reversed(list(enumerate(indices))):
                newIdx = idx + 1
                indices[i] = idx + 1
                if indices[i] >= len(iprimes[i]) and i != 0:
                    indices[i] = 0
                else:
                    break
    elif isinstance(expression, AndR):
        results = []
        for i in inference(model, expression.e1):
            for j in inference(model, expression.e2):
                for r in expression.allenRelations:
                    results.extend(SpanningInterval.I(i, r, j))
        
    elif isinstance(expression, Tense):
        results = []
        for i in inference(model, expression.e):
            for relation in expression.allenRelations:
                results.extend(i.D(relation))
    else:
        raise ValueError("Unexpected type for " + `expression`)
    
    return SpanningIntervalSet(results).condensed()
