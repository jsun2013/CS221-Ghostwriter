# -*- coding: utf-8 -*-
"""
Created on Wed Nov 11 19:56:19 2015

@author: James
"""
import codecs
import os
import string
import collections

def readMultTrainingData(path, author):
    '''
    Reads file with multiple poems. Each poem must be separated by "----"
    '''
    poems = []
    cur_poem = None
    for line in codecs.open(path, encoding = 'utf-8'):
        # Detect new poem:
        if line.strip()[0:4] == "----":
            if cur_poem is not None:
                poems.append((author, cur_poem))
            cur_poem = ""
        else:            
            line = clean(line)
            if line != "":
                cur_poem += line + "\n"
    print 'Read %d poems from %s' % (len(poems), path)
    return poems

def readSingleTrainingData(path, author):
    '''
    Reads file with single poem. 
    '''
    poem = ""
    for line in codecs.open(path, encoding = 'utf-8'):
        line = clean(line)
        if line != "":
            poem += line + "\n"
    print 'Read %s' % (path)
    return (author,poem)
    
    
def clean(line):
    line = line.strip(' \t\n\r')
    line = line.encode('ascii','ignore')
    line = line.translate(string.maketrans("",""),string.punctuation)
    asciiMap = {u'\u2019':u"'", u'\u2014':u"-", u'\u201d':u'"', u'\u201c':u'"', u'\u2013':'-'}
    for i,j in asciiMap.iteritems():
        line = line.replace(i,j)
    return line
    
def getTrainingData():
    '''
    Returns a list of tuples where each tuple is a (poet, string) Where each
    string is an entire poem. Assumes the following directory structure:
    Author/[Multiple or Single]/*.txt    
    Where the "Multiple" directory contains files with multiple poems per file
    and analogously for "Single" directory
    '''    
    authors = ["Coleridge", "Dante", "Frost", "Kerouac", "Seuss"]
    dTrain = collections.defaultdict(list)
    for author in authors:
        multpath = os.path.join(author,'Multiple')
        for fname in os.listdir(multpath):
            if fname.endswith('.txt'):
                fullpath = os.path.join(multpath,fname)
                dTrain[author].extend(readMultTrainingData(fullpath,author))
                
        
        singlepath = os.path.join(author,'Single')
        for fname in os.listdir(singlepath):
            if fname.endswith('.txt'):
                fullpath = os.path.join(singlepath,fname)
                dTrain[author].append(readSingleTrainingData(fullpath,author))
                
    return dTrain

#--------- Main -----------------
#data = getTrainingData()

