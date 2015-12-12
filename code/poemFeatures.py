import collections

"""
poemCharacter takes a poem (as a string) and its author.
It outputs a vector of characteristics for that poem.
""" 

# Notes:
# 1. We could probably calculate word_domain from wordPairs, numLines from word_line_dist, etc., but it doesn't make a difference.
# 2. Should we use a type-token ratio instead?
# 3. What does poem_start keep track of? Words that start a poem or start a new line?

def poemCharacter(poemTuple):
    author = poemTuple[0]
    poem = poemTuple[1]

    poemVector = {}
    numLetters = 0 # total number of none-whitespace letters
    numWords = 0 # total number of words
    numLines = 0 # total number of lines
    lineEnd = [] # keeps track for rhyming
    rhymesAA = 0 # number of lines that rhyme
    rhymesABA = 0
    wordPairs = collections.Counter() # keeps track of how many times a word comes after another
    
    ### GENERATION CHARACTERISTICS ###
    word_line_dist    = collections.Counter()
    word_domain       = collections.Counter()
    poem_start        = collections.Counter()
    type_token_count  = 0
    ### FOR FUTURE USE ###
    
    # Letter, Word, Line counting and Rhyme listing
    numWords = poem.count(' ')
    numLines = poem.count('\n')+1
    numWords += numLines

    word_line = 0
    poem_lines = 0
    prev_word = str()

    # break up text by spaces
    # for each word we add it to word domain, add it to wordPairs or poem_start, and make it the new prev_word
    for word in poem.split(' '):
        word_line += 1
        numLetters += len(word)
        word = word.lower()
        
        # word with newline character is really end of previous line and beginning of next line
        # add the length of the ending line to the distribution and check line ending for rhyming
        if '\n' in word:
            word_line_dist[word_line] += 1
            word_line = 1
            numLetters -= word.count('\n')
            
            end_words = word.split('\n')
            for ind in range(len(end_words)):
                end_word = end_words[ind]

                # if end_word is the end of a line, and at least two letters long, record its last two letters for rhyme checking
                if ind != len(end_words) - 1:
                    if len(end_word) > 1:
                        lineEnd.append(end_word[-2:])

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
            # Should there be an else for poem_start here?
            prev_word = word
    word_line_dist[word_line] += 1 # for the last line which has no newline character
    type_token_count = len(word_domain)

    # AA Rhyme Counting - start from second line
    for ind in range(1,len(lineEnd)):
        if lineEnd[ind] == lineEnd[ind-1]:
            rhymesAA += 1

    # ABA Rhyme Counting - start from third line
    for ind in range(2,len(lineEnd)):
        if lineEnd[ind] == lineEnd[ind-2]:
            rhymesABA += 1


    rhymePercentAA = float(rhymesAA)/numLines
    rhymePercentABA = float(rhymesABA)/numLines
    avgWordLength = float(numLetters)/numWords
    avgLineLength = float(numWords)/numLines

    poemVector['author'] = author # CHARACTERISTIC: Surname of author
    poemVector['numLines'] = numLines # CHARACTERISTIC: Total number of lines in poem
    poemVector['avgWordLength'] = avgWordLength # CHARACTERISTIC: Average length of words in poem
    poemVector['avgLineLength'] = avgLineLength # CHARACTERISTIC: Average length of line in poem
    poemVector['rhymePercentAA'] = rhymePercentAA # CHARACTERISTIC: Percentage of lines that rhyme with a line one before
    poemVector['rhymePercentABA'] = rhymePercentABA # CHARACTERISTIC: Percentage of lines that rhyme with a line two before
    poemVector['wordPairs'] = wordPairs # GENERATION: Counter of how many times a pair of words is used in a row
    poemVector['wordsPerLine'] = word_line_dist # GENERATION: Distribution counter of how many times a certain number of words is used in one line
    poemVector['typeTokenCount'] = type_token_count # GENERATION: How many unique words are used (length of word domain)
    poemVector['wordDomain'] = word_domain # GENERATION: Counter of how many times a word is used
    poemVector['poemStart'] = poem_start # GENERATION: Counter of how many times a word is used to start a poem
    
    return poemVector
