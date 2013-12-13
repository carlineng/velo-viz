#!/usr/bin/env python

from bs4 import BeautifulSoup
import requests
import sys
from datetime import timedelta

def parse_html(input_html):
    soup = BeautifulSoup(input_html)

    title = soup.title.contents[0]
    title_words = title.split(' ')

    year = title_words[1]
    stage = title_words[6]

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
                result['time'] = winning_time + result['plus_time']

        result_str = []
        for result in parsed_results:
            result_str.append(year + '\t' + stage + '\t' + str(result['place']) + '\t' +\
            result['first_name'] + '\t' +\
            result['last_name'] + '\t' +\
            str(result['team']) + '\t' +\
            str(result['time']) + '\t' + str(result['plus_time']))

        for result in result_str:
            print result.encode('utf-8')

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
            , 'time': parse_time(time)
            , 'plus_time': parse_time('0') }

def parse_dnf(row_tail):
    fields = [x.strip() for x in row_tail.split(',')]
    name = parse_name(fields[0])
    team = fields[1]
    return {'first_name': name[0]
            , 'last_name': name[1]
            , 'team': team
            , 'place': -1
            , 'time': None
            , 'plus_time': None }

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
            , 'time': None
            , 'plus_time': parse_time(time)}

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

def parse_time(time_str):
    time_components = time_str.split(':')
    seconds_str = time_components.pop()

    minutes_str = '0'
    result_minutes = 0

    hours_str = '0'
    result_hours = 0

    if len(time_components) > 0:
        minutes_str = time_components.pop()

    if len(time_components) > 0:
        hours_str = time_components.pop()

    result_seconds = int(seconds_str)
    if minutes_str != '':
        result_minutes = int(minutes_str)
    if hours_str != '':
        result_hours = int(hours_str)

    parsed_time = timedelta(hours = result_hours, minutes = result_minutes,
                            seconds = result_seconds)

    return parsed_time
    


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print "Usage: " + sys.argv[0] + " <URL>"
    else:
        url = sys.argv[1]
        r = requests.get(url)
        if r.status_code == 200:
            html_text = r.text
            parse_html(html_text)
        else:
            print "ERROR: request returned non-200 status code"

