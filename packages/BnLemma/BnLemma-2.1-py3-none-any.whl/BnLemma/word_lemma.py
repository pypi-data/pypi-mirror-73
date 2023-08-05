# -*- coding: utf-8 -*-
"""
Created on Sun Dec  9 17:47:35 2018

@author: karigor
"""
from pathlib import Path
script_location = Path(__file__).absolute().parent

class WordLemma:
    def __init__(self, rootfile=None):
        if rootfile is None:
            with open(script_location / "RootWords_bnlemma_ekushey.yaml",'r',encoding = 'utf-8') as corpus:
                self.c_words = [word for line in corpus for word in line.split()]
                self.c_words_len = len(self.c_words)
        else:
            with open(rootfile,'r',encoding = 'utf-8') as corpus:
                self.c_words = [word for line in corpus for word in line.split()]
                self.c_words_len = len(self.c_words)
            
        
        self.mp_word = {}
        for w in self.c_words:
            self.mp_word[w]=1
            

        with open(script_location / "iden.yaml",'r',encoding = 'utf-8') as ide:
            self.id_id = [word for line in ide for word in line.split()]

        from . import trie
        for words in self.c_words:
            trie.dictionary.add(words)

    #Trie distanace
    def trie_lemma(self, word):
        from . import trie        
        return trie.dictionary.search(word)



    #using SRA
    def DBSRA(self,word):
        from . import SRA   
        return SRA.RA(word, self.mp_word)
      


