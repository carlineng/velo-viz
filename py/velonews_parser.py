#!/usr/bin/env python

from bs4 import BeautifulSoup
import sys

def parse_html(input_html):
    soup = BeautifulSoup(input_html)
    results_list_ul = soup.find_all("ul", attrs={"class":"results_list"})
    if len(results_list_ul) != 1:
        print "Error: results_list != 1, quitting"
    else:
        results = [x.string for x in results_list_ul[0].children if len(x.string) > 1]

def parse_result_row(result_row):
    first_space = result_row.find(' ')

    place = 0
    place_str = result_row[0:first_space]
    if place_str == 'DNF':
        place = -1
    else:
        place = int(place_str[:-1])

    row_tail = result_row[first_space].strip()


if __name__ == "__main__":
    testfile = 'test_results.html'
    input_html = open(testfile, 'rb')
    parse_html(input_html)
