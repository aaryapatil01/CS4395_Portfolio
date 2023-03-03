# Names: Austin Girouard and Aarya Patil
# Project: Portfolio Assignment 4 (Ngrams)
# Date: 02/04/23


import os
import pickle
from nltk import word_tokenize
from nltk.util import ngrams


'''
 This function reads data from a file and returns the text as a string
 Input: File name
 Output: A string holding the contents of the file
'''
def read_file(filename):
    # Read data from specified file
    with open(os.path.join(os.getcwd(), filename), 'r', encoding="utf-8") as f:
        text_in = f.read()

    return text_in


'''
 This function calculates the probabilities of possible languages for a given line of text
 Input: Unigram and Bigram dictionaries for English, French, and Italian
 Output: A string holding the guessed language
'''
def calc_lang_prob(text, english_unigram_dict, english_bigram_dict, french_unigram_dict,
                   french_bigram_dict, italian_unigram_dict, italian_bigram_dict):
    print(text)
    # Calculate probability for each possible language
    eng_prob = compute_prob(text, english_unigram_dict, english_bigram_dict, len(english_unigram_dict))
    print("Eng probability:", eng_prob)
    french_prob = compute_prob(text, french_unigram_dict, french_bigram_dict, len(french_unigram_dict))
    print("French probability:", french_prob)
    italian_prob = compute_prob(text, italian_unigram_dict, italian_bigram_dict, len(italian_unigram_dict))
    print("Italian probability:", italian_prob)

    # Find the highest probability, return corresponding language
    max_ = max(eng_prob, french_prob, italian_prob)
    result = ""
    if max_ == eng_prob:
        print("English wins!")
        result = "English"
    if max_ == french_prob:
        print("French wins!")
        result = "French"
    if max_ == italian_prob:
        print("Italian Wins!")
        result = "Italian"
    return result


'''
 This function computes the probability that a line of text can be made given a unigram and bigram dictionary of a given
 language. 
 Input: Text to calculate probability for, unigram dictionary, bigram dictionary, number of unique tokens
 Output: The probability that the given line can be made from the language's dictionaries
'''
def compute_prob(text, unigram_dict, bigram_dict, V):
    # V is the vocabulary size in the training data (unique tokens)
    unigrams_test = word_tokenize(text)
    bigrams_test = list(ngrams(unigrams_test, 2))

    p_laplace = 1   # calculate p using Laplace smoothing

    for bigram in bigrams_test:
        n = bigram_dict[bigram] if bigram in bigram_dict else 0
        d = unigram_dict[bigram[0]] if bigram[0] in unigram_dict else 0
        p_laplace = p_laplace * ((n + 1) / (d + V))

    return p_laplace


def main():
    # Unpickle unigram and bigram dicts
    with open('english_unigram_dict_pickle', 'rb') as handle:
        english_unigram_dict = pickle.load(handle)
    with open('english_bigram_dict_pickle', 'rb') as handle:
        english_bigram_dict = pickle.load(handle)
    with open('french_unigram_dict_pickle', 'rb') as handle:
        french_unigram_dict = pickle.load(handle)
    with open('french_bigram_dict_pickle', 'rb') as handle:
        french_bigram_dict = pickle.load(handle)
    with open('italian_unigram_dict_pickle', 'rb') as handle:
        italian_unigram_dict = pickle.load(handle)
    with open('italian_bigram_dict_pickle', 'rb') as handle:
        italian_bigram_dict = pickle.load(handle)

    # Read test data file name from user
    fp = input("Enter input filename for test data: ")
    # Read data from test data file
    test_data = read_file(fp)
    # Split on newline
    lines = test_data.split('\n')

    # Make list to store all guesses
    all_guesses = []
    # Read output file name from user
    output_file_name = input("Enter output file name: ")
    # Open output file for writing the highest language probabilities for each line
    output_file = open(output_file_name, "w")
    # Read solution file name from user
    sol_file_name = input("Enter solution file name: ")
    # Open solution file for checking language guesses
    solutions = read_file(sol_file_name)

    # Loop through each line, find probability of each language
    for line in lines:
        if line:
            # Guess language
            language_guess = calc_lang_prob(line, english_unigram_dict, english_bigram_dict, french_unigram_dict, french_bigram_dict,
                           italian_unigram_dict, italian_bigram_dict)
            # Store guessed language in all guesses list
            all_guesses.append(language_guess)
            # Write guess to output file
            out_str = str(len(all_guesses)) + ' ' + language_guess + '\n'
            output_file.write(out_str)

    # Close output file
    output_file.close()

    # Make variable to store total correct guesses
    correct_guesses = 0
    # Make variable to store total guesses
    total_guesses = 0
    # Split solutions by newline
    all_solutions = solutions.split('\n')
    # Loop through list of solutions to calculate accuracy
    for solution_line in all_solutions:
        if solution_line:
            # Get line number from solution_line
            line_num = solution_line.split(' ')[0]
            # Get correct language guess from solution_line
            sol = solution_line.split(' ')[1]
            # If guessed correctly, add 1 to total correct score
            if sol == all_guesses[int(line_num)-1]:
                correct_guesses += 1
            # If guessed incorrectly, print the incorrect guess and its line number
            else:
                print("Incorrect guess at line", line_num, ". Guessed =", all_guesses[int(line_num)-1], ", Correct =", sol)
            # Add 1 to total guesses
            total_guesses += 1

    # Print overall accuracy
    print("\n\nOverall guessing accuracy is: %.2f%%" % (correct_guesses/total_guesses*100))


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
