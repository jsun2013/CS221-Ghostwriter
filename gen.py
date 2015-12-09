import poemClassification
import util
import random
import collections

class poem(util.CSP):
    def __init__(self, author):
        util.CSP.__init__(self)
        self.author = author['author']
        self.token_num = util.weightedRandomChoice(author['typeTokenCount'])
        self.line_num = util.weightedRandomChoice(author['linesPerPoem'])
        self.word_num = {}
        
        keys = random.sample(author['wordDomain'], self.token_num)
        self.domain = {key: author['wordDomain'][key] for key in keys}
        
        for line_id in xrange(self.line_num):
            word_num = util.weightedRandomChoice(author['wordsPerLine'])
            self.word_num[line_id] = word_num
        
class generator:
    def __init__(self):
        # Dictionary of authors
        self.authors = {}
        
        # Dictionary of poems
        self.poems = {}
        
        # Poem classifier
        self.classifier = {}
        
    """
        @PARAM author: String containing author's name
    """
    def add_authors(self, authorVectors):
        for name, vector in authorVectors.items():
            if name not in self.authors:
                self.authors[name] = vector

    """
        @PARAM author: String containing author's name
    """
    def generate_poem(self, author_name):
        if author_name not in self.authors:
            print "ERROR: Invalid author ({})".format(author_name)
            return
        
        author = self.authors[author_name]
        new_poem = poem(author)
        word_num = 0
        for line_id in xrange(new_poem.line_num):
            word_num = new_poem.word_num[line_id]
            for word_id in xrange(word_num):
                #print "INFO: Adding Word {} Line {})".format(word_id, line_id)
                new_poem.add_variable((line_id, word_id), new_poem.domain)
                # Adding transition binary factors between words
                if word_id > 0:
                    #print "INFO: Adding factor between Word {} and Word {} in Line {})".format(word_id-1, word_id, line_id)
                    new_poem.add_binary_factor((line_id, word_id-1), (line_id, word_id), \
                    lambda x,y: author['wordPairs'][(x,y)])
            
            #Adding beginning/ending unary factors
            #poem.add_unary_factor((line_id, 0), lambda x: True)
            #poem.add_unary_factor((line_id, word_num-1), lambda x: True)
            
            # Adding transition binary factors between lines
            if line_id > 0:
                #print "INFO: Adding factor between (Line {}, Word {}) and (Line {}, Word {})".format(line_id, 0, line_id-1, prev_word_num-1)
                new_poem.add_binary_factor((line_id, 0), (line_id-1, prev_word_num-1), \
                    lambda x,y: author['wordPairs'][(x,y)])
            prev_word_num = new_poem.word_num[line_id]
        
        self.gibbs(new_poem)

    def gibbs(self, poem):
        assignment = {}
        epsilon = 100
        # Assigns unweighted random words to each variable
        for variable in poem.variables:
            assignment[variable] = random.choice(poem.values[variable].keys())
            
        num_changes = epsilon+1
        loop_count  = 0
        while num_changes > epsilon:
            num_changes = 0
            loop_count += 1
            print "INFO: Gibbs Sampling, Loop {}".format(loop_count)
            
            for (line_id, word_id) in poem.variables:
                variable = (line_id, word_id)
                
                context = poem.binaryFactors[variable].keys()
                #print "\nINFO: Context for {}: {}".format((line_id, word_id), context)

                # Finding previous word
                prev = zip(*context)
                if (line_id, word_id-1) in context:
                    prev = (line_id, word_id-1)
                elif line_id-1 in prev[0]:
                    prev = context[prev[0].index(line_id-1)]
                # Previous word exists
                if type(prev) is tuple:
                    #print "INFO: Previous variable is {}".format(prev)
                    prev_counter = collections.Counter()
                    # Generating counter of previous word tuples
                    for word_pair, count in self.authors[poem.author]['wordPairs'].items():
                        if word_pair[1] == assignment[variable]:
                            prev_counter.update({word_pair: count})
                    # Choosing a value based on Gibbs Sampling
                    # if len(prev_counter) > 0:
                        # total = sum(prev_counter.values())
                        # for word_pair, count in prev_counter.items():
                            # prev_counter[word_pair] = float(count)
                    
                # Finding succeeding word
                succ = None
                if (line_id, word_id+1) in context:
                    succ = (line_id, word_id+1)
                elif (line_id+1, 0)  in context:
                    succ = (line_id+1, 0)
                # Succeeding word exists
                if type(succ) is tuple:
                    #print "INFO: Succeeding variable is {}".format(succ)
                    succ_counter = collections.Counter()