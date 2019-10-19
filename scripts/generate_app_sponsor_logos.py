#!/usr/bin/env python3

import shlex
import subprocess
import sys
import zipfile

from os import makedirs
from os.path import basename

import frontmatter

import pandas as pd

# read in the custom list template
df_sponsors = pd.read_csv('data/app/Guidebook_CL_Template.csv')
rows = []

# create the directory that will store the resized sponsor logs
outdir = 'guidebook-sponsor-logos'
makedirs(outdir, exist_ok=True)

# create the zip file that will contain the resized logs
thumbnail_zipfh = zipfile.ZipFile('sponsor-thumbs.zip', 'w')

# read in the frontmatter from the sponsors page so that we can get
# the logos by sponsor level
content = frontmatter.load('../_pages/sponsors/general.md')
for level in ['diamond', 'platinum', 'gold', 'silver', 'bronze', 'supporter']:
    print(level)
    try:
        logo_info = [(obj['title'], obj['image_path']) for obj in content[level] if 'title' in obj]
    except KeyError:
        continue
    for title, image_path in logo_info:

        image_name = basename(image_path)

        print(' {}'.format(image_path))

        # resize the image to 240x240 since that's what guidebook requires
        try:
            cmd = 'convert ../{} -resize 240x240 {}/{}'.format(image_path, outdir, image_name)
            subprocess.check_call(shlex.split(cmd))
        except subprocess.CalledProcessError:
            print("Something went wrong when resizing {}".format(image_path))
            sys.exit(1)

        # add the resized image to the zip file but don't store the full path
        thumbnail_zipfh.write('{}/{}'.format(outdir, image_name), arcname=image_name)

        # now create the row for the custom list
        d = {'Name': title,
             "Sub-Title (i.e. Location, Table/Booth, or Title/Sponsorship Level)": '{}'.format(level.title()),
             'Description (Optional)': '',
             'Location/Room': '',
             'Image (Optional)': '',
             'Thumbnail (Optional)': image_name}
        rows.append(d)

# close the zip file
thumbnail_zipfh.close()

# write the custom list rows out to a CSV file
df_sponsors = df_sponsors.append(rows)
df_sponsors.to_csv('emnlp2019-sponsors.csv', index=False)
