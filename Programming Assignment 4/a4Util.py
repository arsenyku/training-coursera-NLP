import time
from collections import namedtuple


'''*****************************************************************************
saveToFile

Description:
    This function takes any string and writes it to a file.
    
Parameters:
    filename = the file to be written
    
    text = the text to be written into the file
    
Return Values:
    None 
*****************************************************************************'''
def saveToFile(filename="", text=""):
    if filename=="":
        return
    
    outFileHandle = open(filename,"w")
    outFileHandle.write(text)
    outFileHandle.close()
    
    
    
    
'''*****************************************************************************
readFromFile

Description:
    This function reads a text file and returns a list containing the lines of 
    the file
    
Parameters:
    filename = the file to be read
    
Return Values:
    A list of the lines of the file 
*****************************************************************************'''
def readFromFile(filename=""):
    if filename=="":
        return
    
    # Open and read the contents of the database
    inFileHandle = open(filename)
    lines = inFileHandle.readlines()
    inFileHandle.close()
    
    return lines





'''*****************************************************************************
now

Description:
    Returns a formatted string representing the current time
    
Parameters:
    formatString - a string describing how to format the time.  If not provided,
        a default format will be used.
    
Return Values:
    A formatted string representing the current time 
*****************************************************************************'''
def now(formatString=''):
    now = time.time()

    result = time.strftime("%H:%M:%S", time.localtime(now))
    
    if formatString != '':
        result = time.strftime(formatString, time.localtime(now))

    return result


def uniqueWords( wordList ):    
    return sorted(set(wordList), key=wordList.index)


def uniqueList( someList ):    
    return sorted(set(someList), key=someList.index)


def GetNextSentence(lines):

    sentence = []
    sentence.append("")

    lastWordIndex = -1
    
    for i in xrange(0,len(lines)):
        
        line = lines[i]
        
        word = line.strip()
        
        if word != "":
            sentence.append(word)
            lastWordIndex = i
                    
        else:
            lastWordIndex = i
            break;
    
    return sentence, lines[lastWordIndex+1:]
    
    

    

class Count:
    
    '''*****************************************************************************
    Constructor - initializes class attributes
    *****************************************************************************'''
    def __init__(self):
        self.__counts = dict()

    def Increment(self, item, quantity):
        
        if self.__counts.has_key(item):
            self.__counts[item] += quantity
            
        else:
            self.__counts[item] = quantity
            
            
    def GetCount(self, item):
        count = 0
        
        if self.__counts.has_key(item):
            count = self.__counts[item]
            
        return count
    

    def HasCount(self, item):
        return self.__counts.has_key(item)
    
    
    def Keys(self):
        return self.__counts.keys()
    
    
    def Items(self):
        return self.__counts.iteritems()



class Progress:

    def __init__(self, upperLimit, progressThresholdIncrement):
        self.__progress = 0
        self.__upperLimit = upperLimit
        self.__progressThresholdIncrement = progressThresholdIncrement
        self.__progressThreshold = progressThresholdIncrement
        self.PreText = "Processed"
        self.MidText = "of"
        self.PostText = ""
        
        
    def Reset(self):
        self.__progress = 0
        self.__progressThreshold = self.__progressThresholdIncrement
        
        
    def Increment(self):
        self.__progress += 1
        self.Check()
        
    def Check(self):
        if self.__progressThreshold <= self.__progress:
            print now(), "%s %s %s %s %s" % (self.PreText, self.__progress, self.MidText, self.__upperLimit, self.PostText)
            self.__progressThreshold += self.__progressThresholdIncrement
            




if (__name__ == "__main__"):
    
    d = dict()
    
    print len(d)
    
    print d.keys()
    







        
            