#!/usr/bin/env python3

'''
This script takes the abstracts provided by the program/pub chairs and creates a CSV
file mapping the paper ID to the abstract text.
'''

import argparse
import logging

import pandas as pd

from pathlib import Path


def main():

    # set up an argument parser
    parser = argparse.ArgumentParser(prog='generate_abstract_csv.py')
    parser.add_argument("--input",
                        dest="abstract_dir",
                        required=True,
                        help="Path to the input directory containing the abstracts")
    parser.add_argument("--output",
                        dest="abstract_csv",
                        required=True,
                        help="Path to output CSV file")

    # parse given command line arguments
    args = parser.parse_args()

    # set up the logging
    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)

    # save the abstracts in a dictionary with the paper IDs as keys
    abstract_rows = []
    for abstract_file_path in Path(args.abstract_dir).glob('*.tex'):
        paper_id = abstract_file_path.stem
        if paper_id.startswith('papers-'):
            paper_id = str(int(paper_id.lstrip('papers-')))
        elif paper_id.startswith('TACL-'):
            paper_id = '{}-TACL'.format(int(paper_id.split('-')[1]))
        elif paper_id.startswith('demos-'):
            paper_id = '{}-demo'.format(int(paper_id.split('-')[1]))
        # ignore any papers that do not have a starting prefix
        else:
            continue

        # read in the abstract and store it
        with open(abstract_file_path, 'r') as abstractfh:
            abstract = abstractfh.read().strip()
        abstract_rows.append((paper_id, abstract))

    # write out the dictionary to a CSV file
    df = pd.DataFrame(abstract_rows)
    df.columns = ['Paper ID', 'Abstract']
    df.sort_values(by='Paper ID', inplace=True)
    df.to_csv(args.abstract_csv, index=False)


if __name__ == '__main__':
    main()
