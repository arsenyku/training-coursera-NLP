import time
from collections import namedtuple

BinaryRule = namedtuple('BinaryRule', 'Parent Left Right')
UnaryRule = namedtuple('UnaryRule', 'Parent Child')


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
is_sequence

Description:
    True if arg is an array or list or other "sequence" data structure with 
    whe exception of strings.  False otherwise.
    
    Python duck typing requires we check attributes.  If it has a __getitem__
    or __iter__ attribute, assume it's a "sequence".  However, we exclude 
    strings by checking if it has the "strip" attribute.
    
Parameters:
    arg - the object to be inspected
    
Return Values:
    True if arg is not a string and is a "sequence" data type.  
    False otherwise.
    
Source Reference:
    http://stackoverflow.com/questions/1835018/python-check-if-an-object-is-a-list-or-tuple-but-not-string/1835259#1835259 
    
*****************************************************************************'''
def is_sequence(arg):
    return (not hasattr(arg, "strip") and
            hasattr(arg, "__getitem__") or
            hasattr(arg, "__iter__"))



def is_binaryRule(arg):
    return (hasattr(arg, "Parent") and
            hasattr(arg, "Left") and
            hasattr(arg, "Right"))


def is_unaryRule(arg):
    return (hasattr(arg, "Parent") and
            hasattr(arg, "Child"))



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





if (__name__ == "__main__"):
    
    b1 = BinaryRule("V", "VP", "V")
    b2 = BinaryRule("V", "VP", "V")
    b3 = BinaryRule("V", "VP", "NP")
    
    u1 = UnaryRule("DT", "The")
    
    d = dict()
    
    d[b1] = "hello"
    d[b2] = "there"
    d[b3] = "foo"
    
    print is_binaryRule(b2)
    print is_binaryRule(u1)
    
    print is_unaryRule(b2)
    print is_unaryRule(u1)
    
    print len(d)
    
    print d[b1]
    print d[b2]
    print d[b3]
    
    print b1 == b2
    print b1 == b3
    
    print d.keys()
    







        
            