# Name: Aarya Patil
# Project: Portfolio Chapter 5 (Word Guess Game)
# Date: 02/15/23

import sys
import os
import time
from random import randint
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer


# Function to check if a filepath was provided
def check_file_path():
	if len(sys.argv) < 2:  # in case no filename is given
		quit('ERROR: Filename not provided.')
	else:  # stores filepath and calls read_file function
		file_path = sys.argv[1]
		return read_file(file_path)  # return contents from file back to main()


# Function to read the contents of a file given a filepath
def read_file(file_path):
	current_dir: str = os.getcwd()  # gets current directory

	with open(os.path.join(current_dir, file_path), 'r') as f:  # joins current directory to filepath specified
		text_in = f.read()  # reads in content

	return text_in  # returns information from inside file


# Function to tokenize the provided text
def tokenize_text(text):
	file_tokenized = nltk.word_tokenize(text)  # tokenize the raw text from the file

	return file_tokenized  # return tokenized text


# Function to calculate the lexical diversity of the provided text
def calc_lex_diversity(text):
	tokenized_text = tokenize_text(text)  # call function to tokenize the file contents
	unique_tokens = set(tokenized_text)  # create a set to hold all unique tokens

	return len(unique_tokens) / len(tokenized_text)  # return the lexical diversity


# Function to preprocess the text
def preprocess_text(text):
	tokenized_text = tokenize_text(text)  # call function to tokenize the file contents

	# Make text lowercase and reduce tokens to those that are alpha, not in the NLTK stopword list, and have length > 5
	total_tokens = [t.lower() for t in tokenized_text]  # make all the tokens in the file lowercase
	processed_tokens = [t for t in total_tokens if t.isalpha() and
						t not in stopwords.words('english') and
						len(t) > 5]  # get rid of punctuation, stopwords, and words with less than 5 letters

	# Lemmatize the tokens and use set() to make a list of unique lemmas
	wnl = WordNetLemmatizer()
	total_lemmas = [wnl.lemmatize(t) for t in processed_tokens]  # get all the lemmas
	unique_lemmas = list(set(total_lemmas))  # create a set to hold all unique lemmas

	# Do pos tagging on the unique lemmas and print the first 20 tagged
	pos_tags = nltk.pos_tag(unique_lemmas)
	print("\nThe first 20 tagged lemmas in the text are:", pos_tags[:20])

	# Create a list of only those lemmas that are nouns
	nouns = [w for w, t in pos_tags if t == "NN" or
			 t == "NNS" or
			 t == "NNP" or
			 t == "NNPS"]

	# Print the number of tokens and the number of nouns
	print("\nTotal number of tokens in the file:", len(processed_tokens))
	print("\nTotal number of nouns in the file:", len(nouns))

	# Return processed tokens and nouns
	return processed_tokens, nouns


def guessing_game(words_list):
	# Print out starting screen of game with instructions
	print("\n----------Welcome to the Guessing Game!----------")
	print("Instructions:\n"
		  "You will start off with 5 points total.\n"
		  "For each wrong guess you will lose a point, and for every right guess you will gain one.\n"
		  "The game will end when your total score is negative, or you guess ‘!’ as a letter.\n"
		  "Have fun!")
	time.sleep(1)

	# Start running the actual game
	guess = ""  # variable to hold the user's guess
	score = 5  # variable to keep track of the user's score

	while guess != "!" and score > 0:  # will terminate only when the user guesses "!"
		# Starting values
		word_to_guess = words_list[randint(0, 49)]  # holds the randomly generated word
		letters_guessed = []  # list of letters guessed (will hold underscores in the beginning)
		past_guesses = []  # variable to keep track of past guesses

		# Display "word generation process"
		time.sleep(1)
		print("\nGenerating word...")
		time.sleep(.5)
		print(".")
		time.sleep(.5)
		print(".")
		time.sleep(.5)
		print(".")

		for i in range(len(word_to_guess)):  # stores underscores in place of all the letters
			letters_guessed.append("_")

		# Start the guessing loop that will continue as long as the user doesn't guess "!" and the score is above 0
		while score > 0 and guess != "!" and "_" in letters_guessed:
			print("\nLetters already guessed:", *past_guesses)  # print past guesses so user can track them

			print(*letters_guessed)  # prints the letters_guessed list
			guess = input("Guess a letter: ")  # ask user to enter a guess for a letter in the word

			# Check to see if the guess is already in the past guesses
			if guess in past_guesses:  # if letter has already been guessed
				print("You've already guessed this. Try another letter. Score is", score)
			else:  # if letter hasn't been guessed
				past_guesses.append(guess)  # update letters already guessed

				# Check to see if the letter guessed is in the word
				if guess in word_to_guess:  # if user guesses a letter in the word
					score = score + 1  # update score
					print("Right! Score is", score)  # print out response to answer and score

					# Update the letters_guessed list
					for i in range(len(word_to_guess)):  # stores underscores in place of all the letters
						if guess == word_to_guess[i]:
							letters_guessed[i] = guess
				elif guess == "!":  # if user quits the game
					print("\nGoodbye! See you next time.")
					quit()
				else:  # if user guesses a letter not in the word
					score = score - 1  # update score
					print("Sorry, guess again. Score is", score)  # print out response to answer and score

		if "_" not in letters_guessed:  # if user guesses the word correctly
			print(*letters_guessed)  # prints the letters_guessed list
			time.sleep(1)
			print("You solved it! Good job:)")
			print("\nCurrent score:", score)  # print out the current score
		elif score <= 0:  # if user is out of guesses
			print("\nYou're out of guesses!")
			print("The word was:", word_to_guess)
			print("Game over:( Better luck next time!")
		elif guess == "!":  # if user quits the game
			print("\nGoodbye! See you next time.")


# Main function
def main():
	file_info = check_file_path()  # calls function to check if user provided a filepath

	# Print out header for information section
	print("-----File information section-----")

	# Calculate the lexical diversity of the text from the file
	lex_diversity = calc_lex_diversity(file_info)
	print("\nThe lexical diversity is: {:2.2f}".format(lex_diversity))  # print lexical diversity rounded to 2 dec pts.

	# Preprocess the raw text
	tokens_and_nouns = preprocess_text(file_info)
	(tokens, nouns) = tokens_and_nouns  # unpack the tuple from the result and store into it's individual variables

	# Make a dictionary {noun:count} items from the nouns and tokens lists
	common_words_dict = {}
	for t in tokens:
		if t in nouns:
			if t not in common_words_dict:
				common_words_dict[t] = 1
			else:
				common_words_dict[t] += 1

	# Print out top 50 most common words and their counts; save those words to a list
	print("\nThe top 50 most common words in the file are:")
	number = 1  # counter variable
	for word in sorted(common_words_dict, key=common_words_dict.get, reverse=True)[:50]:
		print(str(number) + ')', word, ':', common_words_dict[word])
		number = number + 1

	top_50_words = sorted(common_words_dict, key=common_words_dict.get, reverse=True)[:50]  # store words to list

	# Start the guessing game
	guessing_game(top_50_words)  # calls function to start game; sends list of top 50 common words to use in the game

	time.sleep(1)  # stalls system for 1 second before terminating program


if __name__ == '__main__':  # uses double underscores
	main()
