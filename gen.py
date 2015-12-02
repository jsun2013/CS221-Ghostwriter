#import classifier
import util
import random

class poet:
    def __init__(self, name="", line_dict={}, word_dict={}, token_dict={}, domain=[]):
        self.name = name
        self.line_dict = line_dict
        self.word_dict = word_dict
        self.token_dict = token_dict
        self.domain = domain

class poem(util.CSP):
    def __init__(self, poet):
        util.CSP.__init__(self)
        self.line_num = util.weightedRandomChoice(poet.line_dict)
        self.word_dict = poet.word_dict
        self.token_num = util.weightedRandomChoice(poet.token_dict)
        self.domain = random.sample(poet.domain, self.token_num)
        
class generator:
    def __init__(self):
        # Dictionary of poets
        self.poets = {}
        
        # Dictionary of poems
        self.poems = {}
        
        # Poem classifier
        self.classifier = {}
        
    """
        @PARAM poet: String containing poet's name
    """
    def add_poet(self, poet):
        # TBD
        pass
        
    """
        @PARAM poem:    Object containing current poem information
        @PARAM line_id: Integer containing current line number
    """
    def generate_line(self, poem, line_id, word_num):
        # Adding variables in line
        for word_id in xrange(word_num):
            poem.add_variable((line_id, word_id), poem.domain)
            
            # Adding transition binary factors between words
            if word_id > 0:
                poem.add_binary_factor((line_id, word_id-1), (line_id, word_id), lambda x,y: True)
        
        # Adding beginning/ending unary factors
        poem.add_unary_factor((line_id, 0), lambda x: True)
        poem.add_unary_factor((line_id, word_num-1), lambda x: True)
    """
        @PARAM poet: String containing poet's name
    """
    def generate_poem(self, poet):
        if poet not in self.poets:
            self.add_poet(poet)
            
        new_poem = poem(self.poets[poet])
        word_num = 0
        for line_id in xrange(new_poem.line_num):
            # Generating random number of words per line
            prev_word_num = word_num
            word_num = self.token_num = util.weightedRandomChoice(new_poem.word_dict)
            self.generate_line(new_poem, line_id, word_num)
            
            # Adding transition binary factors between lines
            if line_id > 0:
                new_poem.add_binary_factor((line_id, 0), (line_id-1, prev_word_num-1), lambda x,y: True)