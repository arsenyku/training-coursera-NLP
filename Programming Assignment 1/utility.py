    
    
def CategorizeRareWords(rareWords):
    
    numeric = []
    allCaps = []
    lastCap = []
    rare = []
    
    
    for rareWord in rareWords:
        
        if isNumericWord(rareWord):
            numeric.append(rareWord)
        
        elif isAllCapsWord(rareWord):
            allCaps.append(rareWord)
            
        elif endsInCap(rareWord):
            lastCap.append(rareWord)
            
        else:
            rare.append(rareWord)
            
    
    return numeric, allCaps, lastCap, rare
        


    
def GetRareTag(rareWord):
    
    tag = "_RARE_"
    
    if isNumericWord(rareWord):
        tag = "_NUMERIC_"
    
    elif isAllCapsWord(rareWord):
        tag = "_ALLCAPS_"
        
    elif endsInCap(rareWord):
        tag = "_LASTCAP_"
        
    return tag
        


def isNumericWord(word):
    digits = "0123456789"
    for c in word:
        if c in digits:
            return True
    
    return False


def isAllCapsWord(word):
    allCaps = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    allLetters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    
    for c in word:
        if c in allLetters and not c in allCaps:
            return False
        
    return True


def endsInCap(word):
    allCaps = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    return (word[-1] in allCaps)
            
