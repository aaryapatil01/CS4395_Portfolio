# Names: Austin Girouard and Aarya Patil
# Project: Portfolio Assignment 6 (Finding or Building a Corpus)
# Date: 03/11/23

import nltk
import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urlparse
from nltk import sent_tokenize
import os
from nltk.corpus import stopwords
import pickle


# This function finds all links embedded in a given webpage (URL).
def get_urls(url):
    # Send a GET request to the URL
    response = requests.get(url)

    # Parse the HTML content of the page using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Get the domain of the input URL
    parsed_url = urlparse(url)
    domain = parsed_url.netloc

    # Find all the urls (stored as 'a href', usually) in the HTML content
    links = soup.find_all('a')

    # Create an empty list to store the relevant URLs
    relevant_urls = []

    # Loop through each link and check if it matches the internal domain
    for link in links:
        href = link.get('href')
        if href is not None:
            # Append https:// and/or domain to front of href if the href's are internally linked
            if href.find('/wiki/') == 0:
                href = 'https://' + domain + href
            elif href.find('//') == 0:
                href = 'https:' + href
            relevant_urls.append(href)

    # Return the list of relevant URLs
    return relevant_urls


# This function finds external links embedded in a given webpage (URL). This is done by
# finding pages that do NOT share the same domain as the given URL.
def get_external_links(url):
    # Send a GET request to the URL
    response = requests.get(url)

    # Parse the HTML content of the page using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Get the domain of the input URL
    parsed_url = urlparse(url)
    domain = parsed_url.netloc

    # Find all the urls (stored as 'a href', usually) in the HTML content
    links = soup.find_all('a')

    # Create an empty list to store the external links
    external_links = []

    # Loop through each link and check if it is external
    for link in links:
        href = link.get('href')
        # Make sure links are external
        if href is not None and re.match(r'^https?://', href):
            parsed_href = urlparse(href)
            if parsed_href.netloc != domain and parsed_href.netloc.find('wikipedia') == -1 and parsed_href.netloc.find(
                    'wikimedia') == -1 and parsed_href.netloc.find('wikidata') == -1 and parsed_href.netloc.find(
                    'wikiquote') == -1 and parsed_href.netloc.find('web.archive') == -1:
                external_links.append(href)

    # Return the list of external links
    return external_links


# This function scrapes URLs and stores the uncleaned output into files
def scrape_urls(all_urls):
    # Scrape internal links for data
    for i in range(15):
        # Create output file for each webpage
        output_file_name = 'unclean_output_file_' + str(i + 1) + '.txt'
        output_file = open(output_file_name, "w", encoding="utf-8")

        # Send a GET request to the URL
        page = requests.get(all_urls[i])

        # Parse the HTML content of the page using BeautifulSoup
        soup = BeautifulSoup(page.content, 'html.parser')

        # Find all text (stored as '<p>', usually) in the HTML content
        results = soup.findAll('p')
        for post in results:
            # Write uncleaned scrape data to input file
            post = post.get_text()
            output_file.write(post)
            output_file.write('\n')

        output_file.close()


# This function cleans the scraped text stored in text files
def clean_files():
    for i in range(15):
        # Open all uncleaned files for cleaning
        with open(os.path.join(os.getcwd(), ('unclean_output_file_' + str(i + 1) + '.txt')), 'r',
                  encoding="utf-8") as f:
            text_in = f.read()
        # Create output file for each webpage (cleaned)
        output_file_name = 'clean_output_file_' + str(i + 1) + '.txt'
        output_file = open(output_file_name, "w", encoding="utf-8")
        # Replace special spaces with regular spaces
        text_in = text_in.replace('\u00A0', ' ')
        # Get rid of new lines and tabs
        post = ''.join([p for p in text_in if not p == '\n' and not p == '\t'])
        # Tokenize using sentence tokenizer
        post = sent_tokenize(post)
        # Clean out inline references and missing spaces after periods
        for p in post:
            # Remove inline references (numerical)
            p = re.sub(r'(\[[0-9]{1,3}\])+ ?', '', p)
            # Remove inline notes (alpha)
            p = re.sub(r'(\[[a-z]\])+ ?', '', p)
            # Get rid of any missing spaces after a period
            p = re.sub(r'\.', '. ', p)
            # Get rid of any duplicate spaces made by the last substitution
            p = re.sub(r'  ', ' ', p)

            # Write to file
            output_file.write(p)
            output_file.write('\n')
        output_file.close()


# This function extracts important terms from a list scraped text pages from URLs
def extract_imp_terms():
    all_words = []
    for i in range(15):
        # Open all cleaned files
        with open(os.path.join(os.getcwd(), ('clean_output_file_' + str(i + 1) + '.txt')), 'r', encoding="utf-8") as f:
            text_in = f.read()

        # Lowercase everything
        text_in = ''.join([t.lower() for t in text_in])
        # Tokenize words from text data
        tokens = nltk.word_tokenize(text_in)
        # Remove stopwords and punctuation
        tokens = [t for t in tokens if t not in stopwords.words('english') and t != '\n' and t.isalpha()]
        # Create a list of all words from all web pages to find most frequent
        all_words += tokens

    # Get term frequencies
    token_set = set(all_words)
    tf_dict = {t: all_words.count(t) for t in token_set}

    # normalize tf by number of tokens
    for t in tf_dict.keys():
        tf_dict[t] = tf_dict[t] / len(all_words)

    # Sort and store the top 30 words by term frequency
    sorted_tf = sorted(tf_dict.items(), key=lambda x: x[1], reverse=True)[:30]

    # Print top 30 words
    for term, freq in sorted_tf:
        print(term, ':', freq)
    print('\n')


# This function creates a knowledge base for important terms sourced from URLs and returns it as a dict
def create_kb():
    kb_dict = {}
    kb_dict['film'] = 'A film – Also called a movie, motion picture, moving picture, picture, photoplay or flick – is ' \
                      'a work of visual art that simulates experiences and otherwise communicates ideas, stories, ' \
                      'perceptions, feelings, beauty, or atmosphere through the use of moving images.'
    kb_dict['christopher nolan'] = 'Christopher Edward Nolan CBE is a British-American filmmaker. Known for his ' \
                                   'Hollywood blockbusters with complex storytelling, Nolan is considered a leading ' \
                                   'filmmaker of the 21st century. His films have grossed $5 billion worldwide.'
    kb_dict['space'] = 'Space is a three-dimensional continuum containing positions and directions. In classical ' \
                       'physics, physical space is often conceived in three linear dimensions. Modern physicists ' \
                       'usually consider it, with time, to be part of a boundless four-dimensional continuum known as ' \
                       'spacetime.'
    kb_dict['role'] = 'A role is one of the characters that an actor or singer can play in a film, play, or opera.'
    kb_dict['matt damon'] = 'Matthew Paige Damon is an American actor, film producer, and screenwriter. Ranked among ' \
                            'Forbes\' most bankable stars, the films in which he has appeared have collectively ' \
                            'earned over $3.88 billion at the North American box office, making him one of the ' \
                            'highest-grossing actors of all time.'
    kb_dict['time'] = 'Time is the continued sequence of existence and events that occurs in an apparently ' \
                      'irreversible succession from the past, through the present, into the future.'
    kb_dict['drama'] = 'Drama is the specific mode of fiction represented in performance: a play, opera, mime, ' \
                       'ballet, etc., performed in a theatre, or on radio or television.'
    kb_dict['actress'] = 'A woman whose profession is acting on the stage, in movies, or on television.'
    kb_dict['world'] = 'The world can be used to reference Earth. In its most general sense, the term "world" refers ' \
                       'to the totality of entities, to the whole of reality or to everything that is. The nature of ' \
                       'the world has been conceptualized differently in different fields. Some conceptions see the ' \
                       'world as unique while others talk of a "plurality of worlds".'
    kb_dict['character'] = 'A character (or speaker, in poetry) is a human or other entity in a narrative (such as a ' \
                           'novel, play, radio or television series, music, film, or video game).'
    return kb_dict


def main():
    # url holds original web crawler source
    url = 'https://en.wikipedia.org/wiki/Interstellar_(film)'
    relevant_urls = get_urls(url)[180:190]
    print(relevant_urls)
    external_urls = get_external_links(url)[56:61]
    print(external_urls)

    # Write uncleaned scrape data to input file
    scrape_urls(relevant_urls + external_urls)

    # Clean scraped files, store in clean_output_file_<#>.txt
    clean_files()

    # Extract important terms from cleaned scraped pages by calculating term frequency
    extract_imp_terms()

    # Create knowledge base from important terms which holds word definitions
    kb_dict = create_kb()

    # Pickle knowledge base dictionary for later use
    with open('kb_dict_pickle', 'wb') as handle:
        pickle.dump(kb_dict, handle)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
