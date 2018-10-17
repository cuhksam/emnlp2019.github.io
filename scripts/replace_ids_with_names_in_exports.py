#!/usr/bin/env python3

'''
This script takes the exported sessions and authors CSVs and replaces
the IDs that are being used as names with the actual names that are
picked up from the sessions.csv and authors.csv files that were generated
earlier using the `parse_order_file_for_app.py` script.
'''

import argparse
import logging

import pandas as pd


def main():

    # set up an argument parser
    parser = argparse.ArgumentParser(prog='replace_ids_with_names_in_exports.py')
    parser.add_argument(dest="exported_sessions_csv",
                        help="The sessions CSV file exported from Guidebook")
    parser.add_argument(dest="exported_authors_csv",
                        help="The authors CSV file exported from Guidebook")
    parser.add_argument("--sessions",
                        dest="sessions_csv",
                        required=True,
                        help="The CSV file containing sessions information")
    parser.add_argument("--authors",
                        dest="authors_csv",
                        required=True,
                        help="Path to CSV file containing authors information")
    parser.add_argument("--papers",
                        dest="papers_csv",
                        required=True,
                        help="Path to CSV file containing papers information")

    # parse given command line arguments
    args = parser.parse_args()

    # set up the logging
    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)

    # read in the sessions, authors, and papers data frames with the relevant
    # IDs as the index and the titles as the values
    df_sessions = pd.read_csv('data/app/sessions.csv', usecols=['Session ID', 'Session Title'], index_col='Session ID')
    df_papers = pd.read_csv('data/app/papers.csv', usecols=['Presentation ID', 'Session Title'], index_col='Presentation ID')
    df_authors = pd.read_csv('data/app/authors.csv', usecols=['Author ID', 'Name'], index_col='Author ID').drop_duplicates()

    # concatenate the sessions and papers into one data frame
    df_papers.index.name = 'Session ID'
    df_sessions_and_papers = df_sessions.append(df_papers)

    # read in the exported CSVs
    df_exported_sessions = pd.read_csv(args.exported_sessions_csv)
    df_exported_authors = pd.read_csv(args.exported_authors_csv)

    df_session_import_with_names = df_exported_sessions.copy()
    df_session_import_with_names['Session Title'] = df_exported_sessions.apply(lambda row: df_sessions_and_papers.loc[row['Session Title']]['Session Title'], axis=1)

    df_author_import_with_names = df_exported_authors.copy()
    df_author_import_with_names['Name'] = df_exported_authors.apply(lambda row: df_authors.loc[row['Name']]['Name'], axis=1)

    # write out the new CSVs
    df_session_import_with_names.to_csv('data/app/sessions-import-with-names.csv', index=False)
    df_author_import_with_names.to_csv('data/app/authors-import-with-names.csv', index=False)


if __name__ == '__main__':
    main()
