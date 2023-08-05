# -*- coding: utf-8 -*-
"""
Created on Mon May 20 03:06:51 2019

@author: karigor
"""

from pathlib import Path
script_location = Path(__file__).absolute().parent

from .word_lemma import WordLemma
from . import edit_distance as ed


class Lemmatizer:
    def __init__(self, root_file=None, mapping_file=None):
        """
        In Python a BnLemma is typically written as:

        ## Usage:
        ```python
        >>>  import BnLemma as lm
        >>>  s = "মানুষের জীবনটা পাচ্ছেন তাই কাজে লাগানো দরকার আমাদেরকে"  
        >>>  bl = lm.Lemmatizer()
        >>>  s = bl.lemma(s)
        >>>  print(s)

        ```
        Output:
        ```
        মানুষ জীবন পাওয়া তাই কাজ লাগা দরকার আমাদের
        ```
        If you want to use your own Root Word List/Word Mapping just load it while initiaizing thw BnLemma class

        ## Usage:
        ```python
        >>>  import BnLemma as lm
        >>>  s = "মানুষের জীবনটা পাচ্ছেন তাই কাজে লাগানো দরকার আমাদেরকে"  
        >>>  bl = lm.Lemmatizer(root_file='root.txt', mapping_file='map.txt')
        >>>  s = bl.lemma(s)
        >>>  print(s)

        ```
        Output:
        ```
        মানুষ জীবন পাওয়া তাই কাজ লাগা দরকার আমাদের
        ```
        """

        self.lm = WordLemma(root_file)
        if mapping_file is None:
            with open(script_location / 'mapvg.txt', 'r', encoding = 'utf-8') as datav:
                self.datav = [word for line in datav for word in line.split()]
        else:
            with open(mapping_file, 'r', encoding = 'utf-8') as datav:
                self.datav = [word for line in datav for word in line.split()]
            

        self.map_vg = {}
        for i in range(len(self.datav)):
          if self.datav[i] == "=":
            self.map_vg [self.datav[i-1]] = self.datav[i+1]

    def lemma(self, sn):
        """
        In Python a BnLemma is typically written as:

            ## Usage:
            ```python
            >>>  import BnLemma as lm
            >>>  s = "মানুষের জীবনটা পাচ্ছেন তাই কাজে লাগানো দরকার আমাদেরকে"  
            >>>  bl = lm.Lemmatizer()
            >>>  s = bl.lemma(s)
            >>>  print(s)

            ```
            Output:
            ```
            মানুষ জীবন পাওয়া তাই কাজ লাগা দরকার আমাদের
            ```
            If you want to use your own Root Word List/Word Mapping just load it while initiaizing thw BnLemma class

            ## Usage:
            ```python
            >>>  import BnLemma as lm
            >>>  s = "মানুষের জীবনটা পাচ্ছেন তাই কাজে লাগানো দরকার আমাদেরকে"  
            >>>  bl = lm.Lemmatizer(root_file='root.txt', mapping_file='map.txt')
            >>>  s = bl.lemma(s)
            >>>  print(s)

            ```
            Output:
            ```
            মানুষ জীবন পাওয়া তাই কাজ লাগা দরকার আমাদের
            ```
        """
        
        qs = sn.split()
        for i in range(len(qs)):
            if qs[i] in self.map_vg.keys():
                qs[i] =  self.map_vg[qs[i]]
        
        qs_list = ""
        for tar_word in qs:
            b = self.lm.DBSRA(tar_word)
            c = self.lm.trie_lemma(tar_word)
          
        
            un = 0
            if b == c:
                val =  b
            
            else:
            
               
                d2 = ed.min_dis(b,tar_word)
                d3 = ed.min_dis(c, tar_word)
            
                mi = min( d2, d3)
               
                if d2 == mi:
                    val = b
                else:
                    val =  c
            
                ln = len(tar_word)
                ln2 = len(val)
                
            
                ck = (mi/ln)*100
               
            
                if ck > 50:
                    val = tar_word
                    un = 1
         
            reval =val
        
            if un ==1:
                c_corpus = ['র','রে','রা','কে','দের','কে','তে']
                for i in range(len(val)):
                    
                    if val in c_corpus:
                        break
        
                    val = val[1:]
                le_val= len(val)     
        
                val = reval[:len(reval)-le_val]  
            qs_list += " " + val
            
        return qs_list.strip(' ')