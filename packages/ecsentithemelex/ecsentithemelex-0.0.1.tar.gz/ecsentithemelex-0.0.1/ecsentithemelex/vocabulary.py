#!/usr/bin/env python
# coding: utf-8

# In[19]:


import pandas as pd
import pkg_resources


class Vocabulary(object):
    
    def __init__(self):
            
        return
    
    def all_phrase_tone(self):
    
        """
        Make data frame with words, bigrams and trigrams and their scores.
        
        :returns:       data frame with words and tones
        :rtype:         frame
        """
    
        stream = pkg_resources.resource_stream(__name__, 'data/all_phrase_tone_lem.csv')
        
        return pd.read_csv(stream).iloc[:,1:]
    
    def all_word_tone_theme(self):
        
        """
        Make data frame with words, bigrams and trigrams, their scores and categories.
        
        :returns:       data frame with words, tones and categories
        :rtype:         frame
        """
        
        stream = pkg_resources.resource_stream(__name__, 'data/all_word_tone_theme_lem.csv')
        
        return pd.read_csv(stream).iloc[:,1:]
    
    def all_forms_tone_theme(self):
    
        """
        Make data frame with words, bigrams and trigrams, their scores and categories (includes all forms of each word).
        
        :returns:       data frame with words, tones and categories
        :rtype:         frame
        """
    
        stream = pkg_resources.resource_stream(__name__, 'data/all_forms_tone_th.csv')
        
        return pd.read_csv(stream).iloc[:,1:]

