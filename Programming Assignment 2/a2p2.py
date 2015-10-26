from __future__ import division
from collections import namedtuple
import json
import a2p1, a2Util as u

Constituent = namedtuple('Constituent', 'SpanStart SpanEnd NonTerminal')
MaxProbability = namedtuple('MaxProbability', 'P RuleBackPointer SplitBackPointer')



class Grammar:
    
    '''*****************************************************************************
    Constructor - initializes class attributes
    *****************************************************************************'''
    def __init__(self, nonTerminalCounts, binaryCounts, unaryCounts, wordCounts):
        self.__PiTable = MaxProbabilityTable()
        self.__NonTerminalCounts = nonTerminalCounts
        self.__BinaryCounts = binaryCounts
        self.__UnaryCounts = unaryCounts
        self.__WordCounts = wordCounts
        
        self.RARETAG = "_RARE_"

        self.N = []
        self.RBinary = []
        self.RUnary = []
        self.T = []

        for nonTerminal in self.__NonTerminalCounts.Keys():
            if (False == (nonTerminal in self.N)):
                self.N.append(nonTerminal)

       
        for rule in self.__BinaryCounts.Keys():
            if (False == (rule in self.RBinary)):
                self.RBinary.append(rule)
        
        for rule in self.__UnaryCounts.Keys():
            if (False == (rule.Child in self.T)):
                self.T.append(rule.Child)

            if (False == (rule in self.RUnary)):
                self.RUnary.append(rule)
            

    def PiTable(self):
        return self.__PiTable

    def isRare(self, word):
        return not self.__WordCounts.HasCount(word)

    def q(self, rule):
        if (u.is_binaryRule(rule)):
            return self.__qBinary(rule)
        else:
            return self.__qUnary(rule)


    def __qBinary(self, binaryRule):
        
        if (False == (binaryRule in self.RBinary)):
            return 0
        
        numerator = self.__BinaryCounts.GetCount(binaryRule)
        denominator = self.__NonTerminalCounts.GetCount(binaryRule.Parent)
        
        return numerator/denominator
    
    
    def __qUnary(self, unaryRule):
        
        if (False == (unaryRule in self.RUnary)):
            return 0
        
        numerator = self.__UnaryCounts.GetCount(unaryRule)
        denominator = self.__NonTerminalCounts.GetCount(unaryRule.Parent)
        
        return numerator/denominator

    
    def ComputeParseTree(self, sentence):
        
        print u.now(), "Initializing tables"
        self.__PiTable.Initialize(sentence, self)
        print u.now(), "Tables initialized"
        
        splitSentence = sentence.split()
        n = len(splitSentence)
        
        for l in xrange(1, n):
            for i in xrange(1, n - l + 1):
                j = i + l

                bestPi = MaxProbability(0, None, None)
        
                for X in self.N:
                    
                    #print l, i, j, X
                    
                    pi = self.FindMaxPi(i, j, X, splitSentence)
                    
                    if bestPi.P <= pi.P:
                        bestPi = pi
                        
                #print bestPi
                    
        print u.now(), "Tables computed"
        
        tree = self.__BuildTree(splitSentence)

        print u.now(), tree
        
        return tree
                
                
    def FindMaxPi(self, spanStart, spanEnd, nonTerminal, splitSentence):
        
        if spanStart == spanEnd:
            return self.__PiTable.GetValue(spanStart, spanEnd, nonTerminal)

        maxPi = MaxProbability(0, None, None)
            
        for rule in self.RBinary:
            
            if rule.Parent != nonTerminal:
                continue
            
            for splitPoint in xrange(spanStart, spanEnd):
                
                qForSplit = self.q(rule)

                piForLeftSplit = self.__PiTable.GetValue(spanStart, splitPoint, rule.Left)
                if (piForLeftSplit.RuleBackPointer == None):
                    piForLeftSplit = self.FindMaxPi(spanStart, splitPoint, rule.Left, splitSentence)
                
                piForRightSplit = self.__PiTable.GetValue(splitPoint+1, spanEnd, rule.Right)
                if (piForRightSplit.RuleBackPointer == None):
                    piForRightSplit = self.FindMaxPi(splitPoint+1, spanEnd, rule.Right, splitSentence)

                piForSplit = qForSplit * piForLeftSplit.P * piForRightSplit.P
                
                if maxPi.P <= piForSplit:
                    maxPi = MaxProbability(piForSplit, rule, splitPoint)
        
        self.__PiTable.SetValue(spanStart, spanEnd, nonTerminal, maxPi.P, maxPi.RuleBackPointer, maxPi.SplitBackPointer)

        return maxPi
            

    def __BuildTree(self, splitSentence):
        
        n = len(splitSentence)
        
        return self.__BuildSubTree(1, n, "SBARQ", splitSentence)
    
    
    
    
    def __BuildSubTree(self, spanStart, spanEnd, nonTerminal, splitSentence):

        pi = self.__PiTable.GetValue(spanStart, spanEnd, nonTerminal)
        
        if u.is_unaryRule( pi.RuleBackPointer ):
            return [ pi.RuleBackPointer.Parent, pi.RuleBackPointer.Child ]
        
        try:
            leftTree = self.__BuildSubTree(spanStart, pi.SplitBackPointer, pi.RuleBackPointer.Left, splitSentence )
            rightTree = self.__BuildSubTree(pi.SplitBackPointer + 1, spanEnd, pi.RuleBackPointer.Right, splitSentence )
        except:
            print pi
            raise

        return [ pi.RuleBackPointer.Parent, leftTree, rightTree ]

    
    
class MaxProbabilityTable:
    
    '''*****************************************************************************
    Constructor - initializes class attributes
    *****************************************************************************'''
    def __init__(self):
        self.__MaxProbabilities = dict()


    def Initialize(self, sentence, grammar):
        self.__MaxProbabilities = dict()
        
        words = sentence.split()
        n = len(words)
        
        for i in xrange(1, n+1):
            for X in grammar.N:
                word = words[i-1]
                
                ruleBackPointer = u.UnaryRule(X, word)
                splitBackPointer = i
                
                if grammar.isRare(word):
                    word = grammar.RARETAG
                
                qValue = grammar.q(u.UnaryRule(X, word))
                
                self.SetValue(i, i, X, qValue, ruleBackPointer, splitBackPointer)


    def SetValue(self, spanStart, spanEnd, nonTerminal, p, ruleBackPointer, splitBackPointer):
        key = Constituent(spanStart, spanEnd, nonTerminal)
        val = MaxProbability(p, ruleBackPointer, splitBackPointer)
        
        if self.__MaxProbabilities.has_key(key):
            currentMax = self.__MaxProbabilities[key]
            
            if currentMax.P > val.P:
                print "WARNING: Overwriting current Max Probability %s for (%s, %s, %s) with a lower value %s" \
                    % ( currentMax.P, spanStart, spanEnd, nonTerminal, val.P )
                
        self.__MaxProbabilities[key] = val



    def GetValue(self, spanStart, spanEnd, nonTerminal):
        key = Constituent(spanStart, spanEnd, nonTerminal)
        result = MaxProbability(0, None, None)
        
        if self.__MaxProbabilities.has_key(key):
            result = self.__MaxProbabilities[key]

        return result




def ParseFile(fileToParse="", adjustedCountsFile="", resultFile=""):
    if fileToParse=="" or adjustedCountsFile=="" or resultFile=="":
        return
    
    counts = a2p1.readCounts(adjustedCountsFile)
    
    nonTerminalCounts = counts[0]
    binaryCounts = counts[1]
    unaryCounts = counts[2]
    wordCounts = counts[3]
    
    print u.now(), "Building Grammar"
    grammar = Grammar(nonTerminalCounts, binaryCounts, unaryCounts, wordCounts)
    print u.now(), "Grammar created"
    
    lines = u.readFromFile(fileToParse)
    
    outputLines = []

    progress = 0
    
    for sentence in lines:
        
        progress += 1
        print "%s Parsing (%s/%s): %s" % ( u.now(), progress, len(lines), sentence[:-1]) 
        
        tree = grammar.ComputeParseTree(sentence)
        outputLine = json.dumps(tree)
        outputLines.append(outputLine)
        
        
    outputText = '\n'.join(outputLines)

    print u.now(), "Saving output to", resultFile
    u.saveToFile(resultFile, outputText)
    
    print u.now(), "Done"
    
    

if __name__ == "__main__":
    import sys

    if len(sys.argv) == 4:
        targetFile = sys.argv[1] 
        adjustedCountsFile = sys.argv[2]
        outputFile = sys.argv[3]

        ParseFile(targetFile, adjustedCountsFile, outputFile)
        sys.exit()
        
    elif len(sys.argv) > 1:
        print "Usage: python a2p2.py <file to parse> <adjusted counts> <output file>"
        sys.exit()
        
    else:
  
    
        countsFile="cfg.counts"
        adjustedCountsFile = "parse_train.counts.out"
        targetFile = "parse_dev.dat"
        outputFile = "parse_dev.out"
        targetFile = "parse_test.dat"
        outputFile = "parse_test.p2.out"
#        targetFile = "test.dat"
#        outputFile = "test.out"
    
        ParseFile(targetFile, adjustedCountsFile, outputFile)

#        counts = a2p1.readCounts(adjustedCountsFile)
#        
#        nonTerminalCounts = counts[0]
#        binaryCounts = counts[1]
#        unaryCounts = counts[2]
#        wordCounts = counts[3]
#        
#        print u.now(), "Building Grammar"
#        grammar = Grammar(nonTerminalCounts, binaryCounts, unaryCounts, wordCounts)
#        print u.now(), "Grammar created"
#        
#        
#        
#        print grammar.q( u.UnaryRule("PP+PP+ADP", "in"))
#        print grammar.q( u.UnaryRule("WHNP+PRON", "What"))
#        print grammar.q( u.UnaryRule(".", "?"))
#        
#        wordCounts

