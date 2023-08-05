
from ..externalAPIs import Itis

def scientificToCommon(names):
    try:
        return Itis.scientificToCommonName(names)
    except Exception as e:
        print("Caught fatal exception in scientific name resolver")
        print(str(e))
        return list(map(lambda x: (x[0],[]),names))


