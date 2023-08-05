
def constructUrls(tsn):
    return 'https://www.itis.gov/ITISWebService/jsonservice/getHierarchyDownFromTSN?tsn='+tsn

def processIndividualResult(nameResTuple):
    try:
        name,result = nameResTuple
        if 'hierarchyList' not in result or len(result['hierarchyList']) == 0 or result['hierarchyList'][0] is None:
            return (name,[])
        
        return (name,list(map(lambda x: (x['rankName'].lower(),x['taxonName']),result['hierarchyList'])))
    except Exception as e:
        print("Caught fatal exception in downstream name API")
        print(str(e))
        return (name,[])

