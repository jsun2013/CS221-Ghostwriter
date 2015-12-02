import collections

"""
poemCharacter takes a poem (as a string) and its author.
It outputs a vector of characteristics for that poem.
""" 

# Task: Ignore uppercase
# Task: Treat multiple spaces in a row as one space
# Task: Deal with empty string as poem

def poemCharacter(poemTuple, outputPairs=False):
    author = poemTuple[0]
    poem = poemTuple[1]

    poemVector = {}
    numLetters = 0 # total number of none-whitespace letters
    numWords = 0 # total number of words
    numLines = 0 # total number of lines
    lineEnd = [] # keeps track for rhyming
    rhymes = 0 # number of lines that rhyme
    wordPairs = collections.Counter() # keeps track of how many times a word comes after another
    prevWord = str()
    curWord = str()
    
    ### GENERATION CHARACTERISTICS ###
    word_line_dist    = collections.Counter()
    word_domain       = collections.Counter()
    type_token_count  = 0
    ### FOR FUTURE USE ###

    numWords = poem.count(' ')
    numLines = poem.count('\n')+1
    numWords += numLines
    
    # Letter, Word, Line counting and Rhyme listing
    word_line = 0
    poem_lines = 0
    prev_word = str()
    for word in poem.split(' '):
        word_line += 1
        numLetters += len(word)
        if '\n' in word:
            word_line_dist[word_line] += 1
            word_line = 1
            numLetters -= word.count('\n')
            
            for end_word in word.split('\n'):
                word_domain[end_word] += 1
                if len(prev_word) > 0:
                    wordPairs[(prev_word, end_word)] += 1
                else:
                    poem_start[end_word] += 1
                prev_word = end_word
        else:
            word_domain[word] += 1
            if len(prev_word) > 0:
                wordPairs[(prev_word, word)] += 1
            prev_word = word
    word_line_dist[word_line] += 1
    type_token_count = len(word_domain)

    # Rhyme counting
    for ind in range(len(lineEnd)):
        # if last line
        if ind == len(lineEnd)-1:
            if (lineEnd[ind] == lineEnd[ind-1]) | (lineEnd[ind] == lineEnd[ind-2]):
                rhymes += 1
        # if second-to-last line
        elif ind == len(lineEnd)-2:
            if (lineEnd[ind]==lineEnd[ind+1]) | (lineEnd[ind] == lineEnd[ind-1]) | (lineEnd[ind] == lineEnd[ind-2]):
                rhymes += 1
        # ordinarily check 1 and 2 lines ahead and 1 and 2 lines behind
        else:
            if (lineEnd[ind] == lineEnd[ind+1]) | (lineEnd[ind] == lineEnd[ind+2]) | (lineEnd[ind] == lineEnd[ind-1]) | (lineEnd[ind] == lineEnd[ind-2]):
                rhymes += 1

    rhymePercent = float(rhymes)/numLines
    avgWordLength = float(numLetters)/numWords
    avgLineLength = float(numWords)/numLines

    poemVector['author'] = author # CHARACTERISTIC: Surname of author
    poemVector['numLines'] = numLines # CHARACTERISTIC: Total number of lines in poem
    poemVector['avgWordLength'] = avgWordLength # CHARACTERISTIC: Average length of words in poem
    poemVector['avgLineLength'] = avgLineLength # CHARACTERISTIC: Average length of line in poem
    poemVector['rhymePercent'] = rhymePercent # CHARACTERISTIC: Percentage of lines that rhyme
    poemVector['wordsPerLine'] = word_line_dist
    poemVector['typeTokenCount'] = type_token_count
    poemVector['wordDomain'] = word_domain
    
    if outputPairs:
         return poemVector, wordPairs   
    else:
         return poemVector
