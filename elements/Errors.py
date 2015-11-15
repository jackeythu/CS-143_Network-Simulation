

class ParaMissing(Exception):
    """
    Notify some parameters of an object are missing
    """
    def __init__(self, lineNum, objectType, objectID, missingPara):
        self.lineNum = lineNum
        self.objectType = objectType
        self.objectID = objectID
        self.missingPara = missingPara
        
    def __str__(self):
        return ('Line' + str(self.lineNum) + ': ParaMissing Error:' + self.missingPara + 'of' + self.objectType
                + self.objectID + 'is missing')
        
class unknownObject(Exception):
    """
    Notify the referenced hosts/links are invalid
    """
    def __init__(self, lineNum, message):
        self.lineNum = lineNum
        self.message = message
        
    def __str__(self):
        return ('Line' + str(self.lineNum) + ': unknownObject Error:' + self.message)   
    
class unknownKeyword(Exception):
    """
    Notify the input keyword is invalid
    """
    def __init__(self, lineNum, message):
        self.lineNum = lineNum
        self.message = message
        
    def __str__(self):
        return ('Line' + str(self.lineNum) + ': unknownKeyword Error:' + self.message)
        