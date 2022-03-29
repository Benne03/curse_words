# Author: Benne Jongsma
# Date: 29-3-2022
# File name: swear_word_freq.py
# Usage: python3 swear_word_freq.py
# A python program that uses multiple gz files and creates multiple csv files
# with the collected data as output.

import os
import json
import gzip
import re
from spacy.lang.en import English
import csv
import matplotlib.pyplot as plt
import pandas as pd


def file_search(directory, file_type):
    """Searches for files with an given extension and directory"""
    return [x for x in os.listdir(directory) if x.endswith(file_type)]


def find_american_english_tweets(file):
    """Searches for American english tweets by the place of the tweet and
    does not select the retweets.
    """

    american_tweet_list = []
    for tweet in file:
        tweet_dict = json.loads(tweet)
        if tweet_dict["text"][:2] != "RT":
            for key, value in tweet_dict.items():
                if key == "place" and value != None:
                    for key_place, value_place in value.items():
                        if key_place == "country_code" and value_place == "US":
                            american_tweet_list.append(tweet_dict["text"])

    return american_tweet_list


def find_british_english_tweets(file):
    """Searches for British english tweets by the place of the tweet and
    does not select the retweets.
    """

    brittish_tweet_list = []
    for tweet in file:
        tweet_dict = json.loads(tweet)
        if tweet_dict["text"][:2] != "RT":
            for key, value in tweet_dict.items():
                if key == "place" and value != None:
                    for key_place, value_place in value.items():
                        if key_place == "country_code" and value_place == "GB":
                            brittish_tweet_list.append(tweet_dict["text"])

    return brittish_tweet_list


def get_words_tweets(file):
    """Creeates tokenized word list from a given text file with Spacy.
    It does not include usernames, ampersand symbols and other characters
    than words.
    """

    nlp = English()
    words_list = []
    tweet_count = 0
    with open(file, 'r') as tweets_file:
        for tweet in tweets_file:
            tweet = tweet.rstrip()
            tweet_count = tweet_count + 1
            if tweet != '':
                tweet = re.sub(' +', ' ', tweet)
                for word in tweet.split():
                    if '@' in word:
                        tweet = tweet.replace(word + ' ', '')
                    if word == '&amp;':
                        tweet = tweet.replace(word, '')
                if '@' in word:
                    tweet = tweet.replace(word, '')

                tokenize_tweet = nlp(tweet)
                for token in tokenize_tweet:
                    token = re.sub(r'[^A-Za-z]+', '', token.text)
                    if token != '' and token[:5] != 'https':
                        words_list.append(token)

    return words_list, tweet_count


def word_count(words, query):
    """Counts the frequency of a given query and his plural forms
    in a given word list.
    """

    count = 0
    for token in words:
        if token.lower() == query or token.lower() == query + 's' or token.lower() == query + 'es':
            count = count + 1

    return count


def create_results_csv_file(csv_file, swear_word_list, word_list_A, word_list_B, country):
    """Creates three csv files with data about British swear words, American swear words,
    the total (relative) frequencies of the swear words.
    """

    rows_country = []
    rows_total = []
    total_cwords_list_A = 0
    total_cwords_list_B = 0
    word_amount_list_A = len(word_list_A)
    word_amount_list_B = len(word_list_B)
    fieldnames_countries = ['swear word', 'frequency in US tweets', 'frequency in GB tweets',
                  'relative frequency in US tweets', 'relative frequency in GB tweets']

    fieldnames_total = ['swearword list country', 'total frequency in US tweets', 'total frequency in GB tweets',
                  'total relative frequency in US tweets', 'total relative frequency in GB tweets']

    for cword in swear_word_list:
        occurences_cword_list_A = word_count(word_list_A, cword)
        occurences_cword_list_B = word_count(word_list_B, cword)
        swear_word_row = {'swear word': cword,
                          'frequency in US tweets': occurences_cword_list_A,
                          'frequency in GB tweets': occurences_cword_list_B,
                          'relative frequency in US tweets': (occurences_cword_list_A / word_amount_list_A),
                          'relative frequency in GB tweets': (occurences_cword_list_B / word_amount_list_B)}
        rows_country.append(swear_word_row)
        total_cwords_list_A += occurences_cword_list_A
        total_cwords_list_B += occurences_cword_list_B

    with open(csv_file, 'w', encoding='UTF8', newline='') as f_country:
        writer = csv.DictWriter(f_country, fieldnames=fieldnames_countries)
        writer.writeheader()
        writer.writerows(rows_country)

    rows_total.append({'swearword list country': country,
                        'total frequency in US tweets': total_cwords_list_A,
                        'total frequency in GB tweets': total_cwords_list_B,
                        'total relative frequency in US tweets': (
                               total_cwords_list_A / word_amount_list_A),
                        'total relative frequency in GB tweets': (
                               total_cwords_list_B / word_amount_list_B)})

    if country == 'US':
        with open('total_curse_tabel.csv', 'w', encoding='UTF8', newline='') as f_total:
            writer = csv.DictWriter(f_total, fieldnames=fieldnames_total)
            writer.writeheader()
            writer.writerows(rows_total)
    else:
        with open('total_curse_tabel.csv', 'a', encoding='UTF8', newline='') as f_total:
            writer = csv.DictWriter(f_total, fieldnames=fieldnames_total)
            writer.writerows(rows_total)

        with open('total_curse_tabel.csv', 'a', encoding='UTF8',newline='') as f_total:
            writer = csv.DictWriter(f_total, fieldnames=fieldnames_total)
            df2 = pd.read_csv('total_curse_tabel.csv')
            total_frequency_US_tweets = df2['total frequency in US tweets'].sum()
            total_frequency_GB_tweets = df2['total frequency in GB tweets'].sum()
            writer.writerows([{'swearword list country': 'total',
                               'total frequency in US tweets': total_frequency_US_tweets,
                               'total frequency in GB tweets': total_frequency_GB_tweets,
                               'total relative frequency in US tweets': total_frequency_US_tweets/word_amount_list_A,
                               'total relative frequency in GB tweets': total_frequency_GB_tweets/word_amount_list_B}])


def create_data_csv_file(american_word_list, british_word_list, american_tweet_amount, british_tweet_amount):
    """Creates a csv file that contains information about the American and British swear amount and the
    amount of collected words for both countries
    """

    header = ['country tweets', 'collected tweet amount',
              'collected word amount']
    data = [
        ['America', american_tweet_amount, len(american_word_list)],
        ['United Kingdom', british_tweet_amount, len(british_word_list)]
    ]
    with open('data_information.csv', 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(data)


def main():
    compressed_files_list = file_search("./en", ".gz")
    with open("british_out.txt", "w") as british_tweets, open("american_out.txt", "w") as american_tweets:
        for file in compressed_files_list:
            with gzip.open(os.path.join("en", file), 'r') as input_british, gzip.open(os.path.join("en", file), 'r') as input_american:
                print("\n".join(find_british_english_tweets(input_british)), file=british_tweets)
                print("\n".join(find_american_english_tweets(input_american)), file=american_tweets)

    british_word_list, british_tweet_amount = get_words_tweets('british_out.txt')
    american_word_list, american_tweet_amount = get_words_tweets('american_out.txt')

    american_swear_word_list = ['jerk', 'moron', 'weird', 'lost mind', 'stupid', 'bitch', 'idiot', 'wacko', 'silly', 'loser', 'shit']
    british_swear_word_list = ['bollocks', 'bugger', 'wanker', 'daft', 'thick', 'nutter', 'fucking hell', 'bonkers', 'cunt', 'bastard', 'arsehole']

    create_results_csv_file('US_curse_table.csv', american_swear_word_list,
                            american_word_list, british_word_list, 'US')
    create_results_csv_file('GB_curse_table.csv', british_swear_word_list, american_word_list, british_word_list, 'GB')

    create_data_csv_file(american_word_list, british_word_list,
                         american_tweet_amount, british_tweet_amount)


if __name__ == "__main__":
    main()