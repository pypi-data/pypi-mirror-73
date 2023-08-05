from .services import createIndex,\
                      crushIndexInput,\
                      writeApiResultsToIndex,\
                      ensureUniqueInIndex,\
                      findDownstreamChildren,\
                      tagInputWithTaxaLevel

def downstream(names,rank):
    index = createIndex(names)
    taggedInput = tagInputWithTaxaLevel([x[0] for x in crushIndexInput(index)])
    writeApiResultsToIndex(index,taggedInput) 
    nameAndRankTuple = crushIndexInput(index)
    results = list(findDownstreamChildren(nameAndRankTuple,rank))
    writeApiResultsToIndex(index,results)
    return index
    
def second(nameRankTuples):
    return list(map(lambda x: x[1], nameRankTuples))

def first(nameRankTuples):
    return list(map(lambda x: x[0], nameRankTuples))