#!/usr/bin/env python
# coding: utf-8

# In[79]:


from .word_score import OneWordScore
import re
from string import punctuation
from nltk.corpus import stopwords
import nltk
import numpy as np


class TextScore(OneWordScore):
    
    def __init__(self):
        
        OneWordScore.__init__(self)
        
        return
    
    
    def score_text(self, text, bigrams_in=False, trigrams_in=False):
    
        """
        Score different texts with opporunity to include one word, bigrams and trigrams(sentiment valuation)
        :type   text:   str
        :param  text:   text to value
        :type   bigrams_in:   bool
        :param  bigrams_in:   If True - bigrams include in scoring
        :type   trigrams_in:   bool
        :param  trigrams_in:   If True - trigrams include in scoring
        
        :returns:       sentiment value of text
        :rtype:         float
        """
        
        only_word_text = self.words_only(text).lower()         
        tokens_vector = [word for word in nltk.word_tokenize(only_word_text) 
                         if word not in stopwords.words('russian')]   
        
        tones_vector = []
        
        for word in tokens_vector:
            try:
                tones_vector.append(self.score(word))
            except:
                tones_vector.append(0)
                        
        
        if bigrams_in == True:
            
            bi_tones_vector = []
            
            for bg in nltk.bigrams(tokens_vector):
                
                try:
                    bi_tones_vector.append(self.score(" ".join(bg)))
                except:
                    bi_tones_vector.append(0)
            
            tones_vector += bi_tones_vector
            
    
        if trigrams_in == True:
            
            tri_tones_vector = []
            
            for bg in nltk.trigrams(tokens_vector):
                
                try:
                    tri_tones_vector.append(self.score(" ".join(bg)))
                except:
                    tri_tones_vector.append(0)
                
            tones_vector += tri_tones_vector
            
                
        
        return np.mean(tones_vector)
    
    def categorize_text(self, text, bigrams_in=False, trigrams_in=False):
    
        """
        Categorize different texts with opporunity to include one word, bigrams and trigrams(economic topics)
        :type   text:   str
        :param  text:   text to value
        :type   bigrams_in:   bool
        :param  bigrams_in:   If True - bigrams include in categorizing
        :type   trigrams_in:   bool
        :param  trigrams_in:   If True - trigrams include in categorizing
        
        :returns:       economic topic of text
        :rtype:         str
        """
        
        category_names = np.delete(self.all_word_tone_theme().Category.unique(),4)
        
        only_word_text = self.words_only(text).lower()         
        tokens_vector = [word for word in nltk.word_tokenize(only_word_text)]
        
        list_of_cats = []
        
        for word in tokens_vector:
            try:
                list_of_cats.append(self.categorize(word))
            except:
                list_of_cats.append('None')
                
        if bigrams_in == True:
            
            for bg in nltk.bigrams(tokens_vector):
                
                try:
                    list_of_cats += [self.categorize(" ".join(bg))]
                except:
                    list_of_cats += ['None']
            
    
        if trigrams_in == True:
                        
            for bg in nltk.trigrams(tokens_vector):
                
                try:
                    list_of_cats += [self.categorize(" ".join(bg))]
                except:
                    list_of_cats += ['None']
                
        list_of_cats = np.array(list_of_cats)
        
        cat_counter = []
        
        for cat in category_names:
            cat_counter.append(np.sum(list_of_cats==cat))
            
                
        return category_names[np.argmax(np.array(cat_counter))]   

