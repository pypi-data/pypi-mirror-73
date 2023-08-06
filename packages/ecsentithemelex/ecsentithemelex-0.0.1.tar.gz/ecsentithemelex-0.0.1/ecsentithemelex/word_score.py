#!/usr/bin/env python
# coding: utf-8

# In[11]:


from .vocabulary import Vocabulary
from pymystem3 import Mystem
import re

class OneWordScore(Vocabulary):
    
    def __init__(self, lem_dicts=False):
            
            if lem_dicts==True:
            
                self.m = Mystem()

                self.dict_tones = self.lem_dict(dict(zip(self.all_word_tone_theme().Phrase,
                                                         self.all_word_tone_theme().Score)))
                self.dict_cats = self.lem_dict(dict(zip(self.all_word_tone_theme().Phrase,
                                                        self.all_word_tone_theme().Category)))
            
            else:
                
                self.dict_tones = dict(zip(self.all_forms_tone_theme().Phrase,
                                          self.all_forms_tone_theme().Score))
                self.dict_cats = dict(zip(self.all_forms_tone_theme().Phrase,
                                          self.all_forms_tone_theme().Category))
            
            return
    
    def words_only(self, text):
    
        """
        Make text without any symbols (only words).
        :type   text:   str
        :param  text:   text to clear
        
        :returns:       clear text
        :rtype:         str
        """
        
        regex = re.compile("[А-Яа-я:=!\)\()\_\%/|]+")
        try:
            return " ".join(regex.findall(text))
        except:
            return ""
    
    def lem_dict(self, dictionary):
    
        """
        Make dictionary with lemotized words.
        :type   dictionary:   str
        :param  dictionary:   dict with words to lem
        
        :returns:       lemmatized dict
        :rtype:         dict
        """
    
        lem_phrases = []
        lem_tones = []
        for tup in list(dictionary.items()):
            lem_phrases.append(self.words_only(''.join(self.m.lemmatize(tup[0]))))
            lem_tones.append(tup[1])

        return dict(zip(lem_phrases,lem_tones))
        
    
    def score(self, word):
    
        """
        Score only one word (sentiment valuation).
        :type   word:   str
        :param  word:   word to sentiment value
        
        :returns:       score of word
        :rtype:         int
        """
        
        try:
            return int(float(self.dict_tones.get(word)))
        except:
            return 0
    
    def categorize(self, word):
    
        """
        Categorize only one word (economic themes).
        :type   word:   str
        :param  word:   word to theme
        
        :returns:       ecnomic category
        :rtype:         str
        """
        
        try:
            return self.dict_cats.get(word)
        except:
            return 'None'

