from ..externalAPIs import Gbif,Itis
from .constants import most_complete_ordering

def findDownstreamChildren(nameRankTuples,targetRank):
    realNames = list(map(lambda x: x[0],nameRankTuples))
    nameRankTuples = list(map(lambda x: x[1],nameRankTuples))
    remapper = dict(zip(list(map(lambda x: x[1],nameRankTuples)),realNames))
    targetRank = targetRank.lower()
    nameRankTuples = addWorkingBlockToNameRankTuples(nameRankTuples)
    finalRankMapping = prepareFinalRankMapping(nameRankTuples,targetRank)
    failsafe = 10
    while failsafe > 0 and len(nameRankTuples) > 0:
        for k,item in enumerate(nameRankTuples):
            rank,name,workingNames = item
            if len(workingNames) == 0: continue
            tsns = Itis.retrieveTSNs(workingNames)
            tsns = list(filter(lambda x: x[1] != '-1',tsns)) # error code is (name,-1)
            if len(tsns) == 0: 
                nameRankTuples[k] = (rank,name,[])
                continue
            fastCheckWorkingNames = set(list(map(lambda x: x.lower(),workingNames)))
            childrenWithTsns = Itis.downstreamToNextRank([x[1] for x in tsns])
            holding = []
            highestRank = rank
            for childrenResponsesWithTsn in childrenWithTsns:
                tsn, childrenWithRanks = childrenResponsesWithTsn
                childrenWithRanks = list(set(childrenWithRanks))
                childrenWithRanks = list(map(lambda x: (x[0].lower(),x[1]),childrenWithRanks))
                childrenWithRanks = list(filter(lambda x: validReturnedName(x,fastCheckWorkingNames,rank),childrenWithRanks))
                for childRank,childName in childrenWithRanks:
                    highestRank = getHighestChildRank(highestRank,childRank)
                    if childRank == targetRank:
                        finalRankMapping[name].append(childName)
                    else:
                        holding.append(childName)
            nameRankTuples[k] = (highestRank,name,holding)
        
        nameRankTuples = filterCompletedSpecies(nameRankTuples)
        failsafe = failsafe - 1

    preRealNameTranslation = finalRankMapping.items()
    return list(map(lambda x: (remapper[x[0]],x[1]),preRealNameTranslation))

def filterCompletedSpecies(nameRankTuples):
    newNameRankTuples = []
    for rank,name,workingNames in nameRankTuples:
        if len(workingNames) > 0:
            newNameRankTuples.append((rank,name,workingNames))
    return newNameRankTuples

def addWorkingBlockToNameRankTuples(nameRankTuples):
    nameRankTuples = list(set(nameRankTuples))
    nameRankTuples = list(map(lambda x: (x[0].lower(),x[1],[x[1]]),nameRankTuples))
    return nameRankTuples

def prepareFinalRankMapping(nameRankTuples,targetRank):
    finalRankMapping = {}
    for rank,name,workingNames in nameRankTuples:
        finalRankMapping[name] = []
        if rank == targetRank:
            finalRankMapping[name] = workingNames
    return finalRankMapping

def validReturnedName(singleAPITupleOutput,workingNames,rank):
    return singleAPITupleOutput[1].strip().lower() not in workingNames \
        and  transformChildRanks((singleAPITupleOutput[0],''))[0] != '' \
        and  transformChildRanks((rank,''))[0] != '' \
        and most_complete_ordering.index(transformChildRanks((singleAPITupleOutput[0],''))[0]) <= most_complete_ordering.index(transformChildRanks((rank,''))[0])
            
def getHighestChildRank(ORank1,ORank2):
    rank1 = transformChildRanks((ORank1,''))[0]
    rank2 = transformChildRanks((ORank1,''))[0]
    result = most_complete_ordering.index(rank1) < most_complete_ordering.index(rank2)
    if result: return ORank2
    return ORank1
            
def transformChildRanks(nameRankTuple):
    rank,name = nameRankTuple
    for item in most_complete_ordering:
        if item in rank:
            return (item,name)
    return ('',name)