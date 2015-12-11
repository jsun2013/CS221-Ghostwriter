import poemClassification
import util
import random
import collections

class poem(util.CSP):
    def __init__(self, author):
        util.CSP.__init__(self)
        self.author = author['author']
        # self.token_num = util.weightedRandomChoice(author['typeTokenCount'])
        self.token_num = 70
        self.line_num = util.weightedRandomChoice(author['linesPerPoem'])
        self.word_num = {}
        self.domain = {}
        
        while(len(self.domain)<self.token_num):
            add_word = util.weightedRandomChoice(author['wordDomain'])
            if add_word != '' and add_word not in self.domain:
                self.domain[add_word] = author['wordDomain'][add_word]
        

        for line_id in xrange(self.line_num):
            word_num = util.weightedRandomChoice(author['wordsPerLine'])
            self.word_num[line_id] = word_num
        
class generator:
    def __init__(self):
        # Dictionary of authors
        self.authors = {}
        
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

        poem_assignment = self.gibbs(new_poem)

        for line in range(new_poem.line_num):
            string = str()
            for word in range(new_poem.word_num[line]):
                string += poem_assignment[(line,word)] + ' '
            print string
        
    def gibbs(self, poem):
        assignment = {}
        epsilon = 5
        
        # Assigns unweighted random words to each variable
        for variable in poem.variables:
            rand_word = random.choice(poem.domain.keys())
            assignment[variable] = rand_word
            print rand_word

        print "\n\n"
        
        

        num_changes = epsilon+1
        loop_count  = 0
        # while num_changes > epsilon:
        while loop_count < 10:
            num_changes = 0
            loop_count += 1
            #print "INFO: Gibbs Sampling, Loop {}".format(loop_count)
            
            for (line_id, word_id) in poem.variables:
                variable = (line_id, word_id)

                #print "\n\n"
                #print "INFO: Sampling word {}".format(variable)
                #print "INFO: Current assignment is {}".format(assignment)
                context = poem.get_neighbor_vars(variable)
                #print "\nINFO: Context for {}: {}".format((line_id, word_id), context)

                # Finding previous word
                prev = zip(*context)

                if (line_id, word_id-1) in context:
                    prev_var = (line_id, word_id-1)
                elif line_id-1 in prev[0]:
                    prev_var = context[prev[0].index(line_id-1)]
                else:
                    prev_var = None

                
                if (line_id, word_id+1) in context:
                    next_var = (line_id, word_id+1)
                elif (line_id+1, 0)  in context:
                    next_var = (line_id+1, 0)
                else:
                    next_var = None


                # try each word from our local domain as this variable
                prev_pairs = {}
                total_prev_pairs = 0
                next_pairs = {}
                total_next_pairs = 0
                assignment_values = {}

                # Try each word against its preceding and following word
                for word in poem.domain:

                    if prev_var != None:
                        count = self.authors[poem.author]['wordPairs'][(assignment[prev_var],word)]
                        if count > 0:
                            prev_pairs[word] = count + 1 # with smoothing
                            total_prev_pairs += count + 1 

                    if next_var != None:
                        count = self.authors[poem.author]['wordPairs'][(word, assignment[next_var])]
                        if  count > 0:
                            next_pairs[word] = count + 1
                            total_next_pairs += count + 1

                # combine keys
                for word in next_pairs:
                    if word not in prev_pairs:
                        prev_pairs[word] = 1
                        total_prev_pairs += 1
                for word in prev_pairs:
                    if word not in next_pairs:
                        next_pairs[word] = 1
                        total_next_pairs += 1


                # normalize and multiply
                for word in prev_pairs:
                    assignment_values[word] = (float(prev_pairs[word])/total_prev_pairs) * (float(next_pairs[word])/total_next_pairs)
                
                if assignment_values:
                    word_choice = util.weightedRandomChoice(assignment_values)
                else:
                    word_choice = random.choice(poem.domain.keys())

                assignment[variable] = word_choice
                num_changes += 1

        return assignment

            