#!/usr/bin/env python3

'''
This script parses the following four files and generates the HTML that can
then be added to the program page on the website:

- order.txt
- authors.csv
- session-chairs.csv
- anthology-mapping.csv

Note that:

1. `dos2unix` must be run on the order file before processing.

2. The order file does not contain any information about tutorials, workshops, or welcome reception.

3. It also does not contain any authors for any papers/posters/demos.

4. The first three files were provided by the program chairs.

5. The last file was scraped manually from the anthology webpage. Although this should not be necessary as the anthology links are generated based on the `order.txt` file, in this case, changes were made to the order file AFTER the handbook was published and, therefore, the anthology was out of sync.
'''

import argparse
import csv
import logging
import re

from itertools import count, cycle

# define some regular expressions to parse the various order file entries
NON_PAPER_SESSION_REGEXP = re.compile(r'([0-9]{2}:[0-9]{2})--([0-9]{2}:[0-9]{2})\s+(.*?)\s+\((.*?)\)')
BREAK_SESSION_REGEXP = re.compile(r'([0-9]{2}:[0-9]{2})--([0-9]{2}:[0-9]{2})\s+(.*)')
PAPER_SESSION_GROUP_REGEXP = re.compile(r'([0-9]{2}:[0-9]{2})--([0-9]{2}:[0-9]{2})\s+(.*?)\((.*?)\)\s+(.*)')
PAPER_SESSION_GROUP_REGEXP2 = re.compile(r'([0-9]{2}:[0-9]{2})--([0-9]{2}:[0-9]{2})\s+(.*)')
PAPER_SESSION_REGEXP = re.compile(r'Session ([^:]+): ([^\(]+) \((.*?)\)')
PAPER_REGEXP = re.compile(r'([^ ]+)\s+([0-9]{2}:[0-9]{2})--([0-9]{2}:[0-9]{2})\s#\s(.*)')
POSTER_DEMO_REGEXP = re.compile(r'([^ ]+)\s#\s(.*)')
BEST_PAPER_REGEXP = re.compile(r'([^ ]+)\s+([0-9]{2}:[0-9]{2})--([0-9]{2}:[0-9]{2})\s#\s(.*)')

KEYNOTE_ABSTRACT_DICT = {
    'Cha': 'Artificial intelligence (AI) is reshaping business and science. Computational social science is an interdisciplinary field that solves complex societal problems by adopting AI-driven methods, processes, algorithms, and systems on data of various forms. This talk will review some of the latest advances in the research that focuses on fake news and legal liability. I will first discuss the structural, temporal, and linguistic traits of fake news propagation. One emerging challenge here is the increasing use of automated bots to generate and propagate false information. I will also discuss the current issues on the legal liability of AI and robots, particularly on how to regulate them (e.g., moral machine, punishment gap). This talk will suggest new opportunities to tackle these problems.',
    'Cho': 'In this talk, I take the audience on a tour of my earlier and recent experiences in building neural sequence models. I start from the earlier experience of using a recurrent net for sequence-to-sequence learning and talk about the attention mechanism. I discuss factors behind the success of these earlier approaches, and how these were embraced by the community even before they sota’d. I then move on to more recent research direction in unconventional neural sequence models that automatically learn to decide on the order of generation.',
    'Slonim': 'Project Debater is the first AI system that can meaningfully debate a human opponent. The system, an IBM Grand Challenge, is designed to build coherent, convincing speeches on its own, as well as provide rebuttals to the opponent’s main arguments. In February 2019, Project Debater competed against Harish Natarajan, who holds the world record for most debate victories, in an event held in San Francisco that was broadcasted live world-wide. In this talk I will tell the story of Project Debater, from conception to a climatic final event, describe its underlying technology, and discuss how it can be leveraged for advancing decision making and critical thinking.'}


def process_line(line):
    end_index = line.find('[') if '[' in line else len(line)
    processed_line = line[:end_index].strip()
    return processed_line


def collect_instances(iterator, character):
    groups = []
    group = []
    start = True
    while 1:
        try:
            line = next(iterator)
        except StopIteration:
            groups.append(group)
            break
        else:
            if line.startswith(character):
                if start:
                    group.append(line)
                    start = False
                else:
                    groups.append(group)
                    group = [line]
            else:
                if not line:
                    continue
                group.append(line)
    return groups


def get_anthology_link(anthology_id):
    return "http://aclweb.org/anthology/{}".format(anthology_id)


def main():

    # set up an argument parser
    parser = argparse.ArgumentParser(prog='parse_order_file_and_generate_schedule.py')
    parser.add_argument("--order",
                        dest="order_file",
                        required=True,
                        help="Path to order file containing session information")
    parser.add_argument("--authors",
                        dest="authors_csv",
                        required=True,
                        help="Path to CSV file containing author information")
    parser.add_argument("--chairs",
                        dest="chairs_csv",
                        required=True,
                        help="Path to CSV file containing session chair information")
    parser.add_argument("--anthology",
                        dest="anthology_csv",
                        required=True,
                        help="Path to CSV file containing anthology IDs for papers, posters, and demos")

    # parse given command line arguments
    args = parser.parse_args()

    # set up the logging
    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)

    # initialize the list of generated HTML items
    generated_html = []

    # open order file and capture the contents of each day into separate lists
    with open(args.order_file, 'r') as orderfh:
        processed_lines = [process_line(line) for line in orderfh]
    days = collect_instances(iter(processed_lines), '*')

    # read in the CSV file mapping paper IDs to authors
    authors_dict = {}
    with open(args.authors_csv, 'r') as authorsfh:
        reader = csv.DictReader(authorsfh, fieldnames=["Submission ID", "Authors"])
        for row in reader:
            assert row['Submission ID'] not in authors_dict
            authors_dict[row['Submission ID']] = row['Authors']

    # read in the CSV file mapping sessions to chairs
    chairs_dict = {}
    with open(args.chairs_csv, 'r') as chairsfh:
        reader = csv.DictReader(chairsfh, fieldnames=["Session", "Name", "Email"])
        for row in reader:
            session_id = row['Session'].split(':')[0]
            assert session_id not in chairs_dict
            chairs_dict[session_id] = (row['Name'], row['Email'])

    # read in the CSV file mapping paper/poster titles to anthology IDs
    anthology_dict = {}
    with open(args.anthology_csv, 'r') as anthologyfh:
        reader = csv.DictReader(anthologyfh, fieldnames=["Title", "ID"])
        for row in reader:
            anthology_dict[row['Title'].lower()] = row['ID']

    # now in each day, process each session one by one
    days_counter = count(start=3)
    lunch_id_counter = count(start=3)
    break_id_counter = count(start=1)
    paper_session_group_counter = count(start=1)
    paper_session_counter = cycle([1, 2, 3, 4])
    poster_session_counter = count(start=1)
    for day in days:
        day_string = day.pop(0).lstrip('* ')
        generated_html.append('<div class="day" id="day-{}">{}</div>'.format(next(days_counter), day_string))

        # take the days's contents and group them into sessions
        day_sessions = collect_instances(iter(day), '+')

        # now iterate over each session in the day
        for session in day_sessions:
            session_string = session.pop(0).lstrip('+ ').strip()
            if 'break' in session_string.lower() or 'lunch' in session_string.lower():
                session_start, session_end, break_title = BREAK_SESSION_REGEXP.match(session_string).groups()
                if break_title.lower() == 'lunch':
                    break_title = 'Lunch'
                    break_type = 'lunch'
                    break_id = next(lunch_id_counter)
                elif 'mini' in break_title.lower():
                    break_title = 'Mini-Break'
                    break_type = 'break'
                    break_id = next(break_id_counter)
                else:
                    break_title = 'Coffee Break'
                    break_type = 'break'
                    break_id = next(break_id_counter)
                generated_html.append('<div class="session session-break session-plenary" id="session-{}-{}"><span class="session-title">{}</span><br/><span class="session-time" title="{}">{} &ndash; {}</span></div>'.format(break_type, break_id, break_title, day_string, session_start, session_end))
            elif 'keynote' in session_string.lower():
                session_start, session_end, session_title, session_location = NON_PAPER_SESSION_REGEXP.match(session_string).groups()

                if 'Cha' in session_title:
                    session_title = session_title.replace('Meeyoung Cha ', '')
                    session_abstract = KEYNOTE_ABSTRACT_DICT['Cha']
                    session_people = 'Meeyoung Cha (KAIST)'
                    session_people_link = 'https://ds.kaist.ac.kr/professor.html'
                elif 'Cho' in session_title:
                    session_title = session_title.replace('Kyunghyun Cho ', '')
                    session_abstract = KEYNOTE_ABSTRACT_DICT['Cho']
                    session_people = 'Kyunghyun Cho (New York University)'
                    session_people_link = 'http://www.kyunghyuncho.me'
                elif 'Slonim' in session_title:
                    session_title = session_title.replace('Noam Slonim ', '')
                    session_abstract = KEYNOTE_ABSTRACT_DICT['Slonim']
                    session_people = 'Noam Slonim (IBM Haifa Research Lab)'
                    session_people_link = 'http://researcher.watson.ibm.com/researcher/view.php?person=il-NOAMS'

                generated_html.append('<div class="session session-expandable session-plenary"><div id="expander"></div><a href="#" class="session-title"><strong>{}</strong></a><br/><span class="session-people"><a href="{}" target="_blank">{}</a></span><br/><span class="session-time" title="{}">{} &ndash; {}</span><br/><span class="session-location btn btn--info btn--location">{}</span><div class="paper-session-details"><br/><div class="session-abstract"><p>{}</p></div></div></div>'.format(session_title, session_people_link, session_people, day_string, session_start, session_end, session_location, session_abstract))
            elif 'opening' in session_string.lower():
                session_start, session_end, session_title, session_location = NON_PAPER_SESSION_REGEXP.match(session_string).groups()
                generated_html.append('<div class="session session-plenary" id="session-welcome"><span class="session-title">{}</span><br/><span class="session-time" title="{}">{} &ndash; {}</span><br/> <span class="session-location btn btn--info btn--location">{}</span></div>'.format(session_title, day_string, session_start, session_end, session_location))
            elif 'social event' in session_string.lower():
                session_start, session_end, session_title, session_location = NON_PAPER_SESSION_REGEXP.match(session_string).groups()
                generated_html.append('<div class="session session-expandable session-plenary" id="session-social"><div id="expander"></div><a href="#" class="session-title">{}</a><br/><span class="session-time" title="{}">{} &ndash; {}</span><br/><span class="session-external-location btn btn--info btn--location">{}</span> <div class="paper-session-details"> <br/><div class="session-abstract"><p>On the evening of Saturday, November 3rd, the EMNLP 2018 social event will take place at the Royal Museums of Fine Arts of Belgium. Four museums, housed in a single building, will welcome the EMNLP delegates with their prestigious collection of 20,000 works of art. The Museums’ collections trace the history of the visual arts — painting, sculpture and drawing — from the 15th to the 21st century.</p></div></div></div>'.format(session_title, day_string, session_start, session_end, session_location))
            elif 'business meeting' in session_string.lower():
                session_start, session_end, session_title, session_location = NON_PAPER_SESSION_REGEXP.match(session_string).groups()
                generated_html.append('<div class="session session-expandable session-plenary" id="session-business"><div id="expander"></div><a href="#" class="session-title">{}</a><br/><span class="session-time" title="{}">{} &ndash; {}</span><br/><span class="session-location btn btn--info btn--location">{}</span><br/><div class="paper-session-details"> <br/><div class="session-abstract">All attendees are encouraged to participate in the business meeting.</div></div></div>'.format(session_title, day_string, session_start, session_end, session_location))
            elif 'best paper' in session_string.lower():
                session_start, session_end, session_title, session_location = NON_PAPER_SESSION_REGEXP.match(session_string).groups()
                generated_html.append('<div class="session session-expandable session-papers-best"><div id="expander"></div><a href="#" class="session-title">{}</a><br/><span class="session-time" title="{}">{} &ndash; {}</span><br/><span class="session-location btn btn--info btn--location">{}</span><br/><div class="paper-session-details"><br/><table class="paper-table">'.format(session_title, day_string, session_start, session_end, session_location))
                for paper in session:
                    best_paper_id, best_paper_start, best_paper_end, best_paper_title = BEST_PAPER_REGEXP.match(paper.strip()).groups()
                    best_paper_authors = authors_dict[best_paper_id].strip()
                    best_paper_url = get_anthology_link(anthology_dict[best_paper_title.lower()])
                    generated_html.append('<tr id="best-paper" paper-id="{}"><td id="paper-time">{}&ndash;{}</td><td><span class="paper-title">{}. </span><em>{}</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="{}" aria-hidden="true"></i></td></tr>'.format(best_paper_id, best_paper_start, best_paper_end, best_paper_title, best_paper_authors, best_paper_url))
                generated_html.append('</table></div></div>')
            elif re.search(r"Session (\d+)", session_string):
                session_group_start, session_group_end, session_group_description = PAPER_SESSION_GROUP_REGEXP2.match(session_string).groups()
                paper_session_group_id = next(paper_session_group_counter)
                #session_group_type = session_group_type.replace('and', '&amp;')
                #session_group_description = session_group_description.replace('and', '&amp;')
                #generated_html.append('<div class="session-box" id="session-box-{}"><div class="session-header" id="session-header-{}">{}{} ({})</div>'.format(paper_session_group_id, paper_session_group_id, session_group_type, session_group_roman_numeral, session_group_description))
                generated_html.append('<div class="session-box" id="session-box-{}"><div class="session-header" id="session-header-{}"> ({})</div>'.format(paper_session_group_id, paper_session_group_id, session_group_description))
                day_session_splits = collect_instances(iter(session), '=')
                for split in day_session_splits:
                    split_string = split.pop(0).lstrip('= ').strip()
                    session_id, session_title, session_parens = PAPER_SESSION_REGEXP.match(split_string).groups()
                    session_title = session_title.replace('and', '&amp;')
                    if ',' in session_parens:
                        session_type, session_location = session_parens.split(', ')
                        session_type = session_type.strip()
                        session_location = session_location.strip()
                    else:
                        session_location = session_parens.strip()
                        session_type = ''
                    if 'poster' in session_type.lower() or 'poster' in session_id.lower():
                        session_title = '{} ({})'.format(session_title, session_type) if session_type else session_title
                        generated_html.append('<div class="session session-expandable session-posters" id="session-poster-{}"><div id="expander"></div><a href="#" class="session-title">{}: {} </a><br/><span class="session-time" title="{}">{} &ndash; {}</span><br/><span class="session-location btn btn--info btn--location">{}</span><div class="poster-session-details"><br/><table class="poster-table">'.format(next(poster_session_counter), session_id, session_title, day_string, session_group_start, session_group_end, session_location))
                    else:
                        session_chair_name, session_chair_email = chairs_dict[session_id]
                        #generated_html.append('<div class="session session-expandable session-papers{}" id="session-{}"><div id="expander"></div><a href="#" class="session-title">{}: {}</a><br/><span class="session-time" title="{}">{} &ndash; {}</span><br/><span class="session-location btn btn--info btn--location">{}</span><br/><div class="paper-session-details"><br/><a href="#" class="session-selector" id="session-{}-selector"> Choose All</a><a href="#" class="session-deselector" id="session-{}-deselector">Remove All</a><table class="paper-table"><tr><td class="session-chair" colspan="2">Chair: <a href="mailto:{}">{}</a></td></tr>'.format(next(paper_session_counter), session_id.lower(), session_id, session_title, day_string, session_group_start, session_group_end, session_location, session_id.lower(), session_id.lower(), session_chair_email, session_chair_name))
                        generated_html.append('<div class="session session-expandable session-papers{}" id="session-{}"><div id="expander"></div><a href="#" class="session-title">{}: {}</a><br/><span class="session-time" title="{}">{} &ndash; {}</span><br/><span class="session-location btn btn--info btn--location">{}</span><br/><div class="paper-session-details"><br/><a href="#" class="session-selector" id="session-{}-selector"> Choose All</a><a href="#" class="session-deselector" id="session-{}-deselector">Remove All</a><table class="paper-table"><tr><td class="session-chair" colspan="2">Chair: {}</td></tr>'.format(next(paper_session_counter), session_id.lower(), session_id, session_title, day_string, session_group_start, session_group_end, session_location, session_id.lower(), session_id.lower(), session_chair_name))
                    for paper in split:
                        paper = paper.strip()
                        if 'poster' in session_type.lower() or 'poster' in session_id.lower():
                            if paper.startswith('@'):
                                poster_topic = paper.lstrip('@ ')
                                generated_html.append('<tr><td><span class="poster-type">{}</span></td></tr>'.format(poster_topic))
                                continue
                            else:
                                poster_id, poster_title = POSTER_DEMO_REGEXP.match(paper).groups()
                                if poster_id.endswith('-TACL'):
                                    poster_title = '[TACL] {}'.format(poster_title)
                                    # tacl_article_id = poster_id.split('-')[0]
                                    # poster_url = 'https://transacl.org/ojs/index.php/tacl/article/view/{}'.format(tacl_article_id)
                                    poster_url = ''
                                else:
                                    poster_url = get_anthology_link(anthology_dict[poster_title.lower()])
                                poster_authors = authors_dict[poster_id].strip()
                                generated_html.append('<tr id="poster" poster-id="{}"><td><span class="poster-title">{}. </span><em>{}</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="{}" aria-hidden="true"></i></td></tr>'.format(poster_id, poster_title, poster_authors, poster_url))
                        else:
                            paper_id, paper_start, paper_end, paper_title = PAPER_REGEXP.match(paper.strip()).groups()
                            paper_authors = authors_dict[paper_id].strip()
                            if paper_id.endswith('-TACL'):
                                paper_title = '[TACL] {}'.format(paper_title)
                                # tacl_article_id = paper_id.split('-')[0]
                                # paper_url = 'https://transacl.org/ojs/index.php/tacl/article/view/{}'.format(tacl_article_id)
                                paper_url = ''
                            else:
                                paper_url = get_anthology_link(anthology_dict[paper_title.lower()])
                            generated_html.append('<tr id="paper" paper-id="{}"><td id="paper-time">{}&ndash;{}</td><td><span class="paper-title">{}. </span><em>{}</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="{}" aria-hidden="true"></i></td></tr>'.format(paper_id, paper_start, paper_end, paper_title, paper_authors, paper_url))
                    generated_html.append('</table></div></div>'.format(paper_id, paper_start, paper_end, paper_title))
                generated_html.append('</div>')

    print('\n'.join(generated_html))


if __name__ == '__main__':
    main()
