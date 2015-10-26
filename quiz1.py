from __future__ import division
import math

M = 12

m1_p_values = [None] * 1
m2_p_values = [None] * 1

# the dog STOP
m1_p_values[0] = 1 * 1 * 1
m2_p_values[0] = .5 * 1 * 1

def Perplexity(p_values = [ ], corpusWordCount = 1):
    if corpusWordCount <= 0:
        raise "Word count must be greater than 0"
    
    logsum = 0

    for p in p_values:
        logsum += math.log(p, 2)
    
    l = logsum/corpusWordCount

    perplexity = 2 ** -l

    return perplexity


m1Perplexity = Perplexity(m1_p_values, 3)
m2Perplexity = Perplexity(m2_p_values, 3)

print m1Perplexity, m2Perplexity




