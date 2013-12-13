#!/usr/bin/env python

from bs4 import BeautifulSoup
import sys
from datetime import timedelta

def parse_html(input_html):
    soup = BeautifulSoup(input_html)
    results_list_ul = soup.find_all("ul", attrs={"class":"results_list"})
    if len(results_list_ul) != 1:
        print "Error: results_list != 1, quitting"
    else:
        results = [x.string for x in results_list_ul[0].children if len(x.string) > 1]
        parsed_results = [parse_result_row(x) for x in results]

        winning_time = None
        for result in parsed_results:
            if result['place'] == 1:
                winning_time = result['time']
            break

        for result in parsed_results:
            if result['place'] > 1:


def parse_result_row(result_row):
    first_space = result_row.find(' ')
    place_str = result_row[0:first_space]
    row_tail = result_row[first_space:].strip()

    if place_str == '1.':
        return parse_first(row_tail)
    elif place_str == 'DNF':
        return parse_dnf(row_tail)
    else:
        return parse_other(place_str, row_tail)

def parse_first(row_tail):
    fields = [x.strip() for x in row_tail.split(',')]
    name = parse_name(fields[0])
    team = fields[1]

    time_start_pos = fields[2].find(' ') + 1
    time = fields[2][time_start_pos:]
    return {'first_name': name[0]
            , 'last_name': name[1]
            , 'team': team
            , 'place': 1
            , 'time': time}

def parse_dnf(row_tail):
    fields = [x.strip() for x in row_tail.split(',')]
    name = parse_name(fields[0])
    team = fields[1]
    return {'first_name': name[0]
            , 'last_name': name[1]
            , 'team': team
            , 'place': -1
            , 'time': None}

def parse_other(place_str, row_tail):
    place = int(place_str[:-1])

    fields = [x.strip() for x in row_tail.split(',')]
    name = parse_name(fields[0])
    team = fields[1]

    time_start_pos = fields[2].find(' ') + 1
    time = fields[2][time_start_pos:]
    return {'first_name': name[0]
            , 'last_name': name[1]
            , 'team': team
            , 'place': place
            , 'time': time}

def parse_name(name_str):
    first_name_words = []
    last_name_words = []

    name_words = name_str.split()
    for word in name_words:
        if all( [letter.isupper() for letter in word if letter.isalpha()] ):
            last_name_words.append(word)
        else:
            first_name_words.append(word)

    first_name = ' '.join(first_name_words)
    last_name = ' '.join(last_name_words)
    return (first_name, last_name)

if __name__ == "__main__":
    testfile = 'test_results.html'
    input_html = open(testfile, 'rb')
    parse_html(input_html)
