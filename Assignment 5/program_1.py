# Names: Austin Girouard and Aarya Patil
# Project: Portfolio Assignment 4 (Ngrams)
# Date: 02/04/23


import os
import pickle
from nltk import word_tokenize
from nltk.util import ngrams


'''
 This function reads in a file and creates a dictionary of unigrams and bigrams from the text
 Input: File name
 Output: Tuple containing (unigram dictionary, bigram dictionary)
'''
def build_language_model(filename):
    # Read data from specified file
    with open(os.path.join(os.getcwd(), filename), 'r', encoding="utf-8") as f:
        text_in = f.read()

    # Remove newlines from text
    tokens = ''.join([t for t in text_in if not t == '\n'])

    # Make unigrams from text using nltk.word_tokenize library
    unigrams = word_tokenize(tokens)

    # Make bigrams from text using nltk
    bigrams = list(ngrams(unigrams, 2))

    # Make unigram_dict
    unigram_dict = {t:unigrams.count(t) for t in set(unigrams)}

    # Make bigram_dict
    bigram_dict = {b:bigrams.count(b) for b in set(bigrams)}

    return unigram_dict, bigram_dict


def main():
    # Read in file english name
    fp = input("Enter filename for English data: ")
    # Build language model for English data
    english_data = build_language_model(fp)
    # Split tuple into unigram and bigrams
    (english_unigram_dict, english_bigram_dict) = english_data
    # pickle unigram and bigram dicts
    with open('english_unigram_dict_pickle', 'wb') as handle:
        pickle.dump(english_unigram_dict, handle)
    with open('english_bigram_dict_pickle', 'wb') as handle:
        pickle.dump(english_bigram_dict, handle)

    fp = input("Enter filename for French data: ")
    # Build language model for French data
    french_data = build_language_model(fp)
    # Split tuple into unigram and bigrams
    (french_unigram_dict, french_bigram_dict) = french_data
    # pickle unigram and bigram dicts
    with open('french_unigram_dict_pickle', 'wb') as handle:
        pickle.dump(french_unigram_dict, handle)
    with open('french_bigram_dict_pickle', 'wb') as handle:
        pickle.dump(french_bigram_dict, handle)

    fp = input("Enter filename for Italian data: ")
    # Build language model for Italian data
    italian_data = build_language_model(fp)
    # Split tuple into unigram and bigrams
    (italian_unigram_dict, italian_bigram_dict) = italian_data
    # pickle unigram and bigram dicts
    with open('italian_unigram_dict_pickle', 'wb') as handle:
        pickle.dump(italian_unigram_dict, handle)
    with open('italian_bigram_dict_pickle', 'wb') as handle:
        pickle.dump(italian_bigram_dict, handle)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
