## To generate the schedule for the website

1. Make sure you have the files `order.txt`, `authors.csv`, `session-chairs.csv` and `anthology-mapping.csv` under the `data` directory.

2. Run `python parse_order_file_and_generate_schedule.py --order data/order.txt --authors data/authors.csv --chairs data/session-chairs.csv --anthology data/anthology-mapping.csv`. This will print out the HTML schedule to standard output. Take this output and replace the HTML in `schedule.md` in the appropriate place (which is the HTML that starts at the div block of Day 2 of the conference - November 2, 2018 and goes till right before the div block of the form containing the generate PDF button).

3. Manually link the TACL PDFs (under `downloads`) to the appropriate papers in the schedule.

## To generate the sponsor thumbnails for the GuideBook app

1. Install the python-frontmatter package. 

2. Make sure you have the `convert` tool from ImageMagick.

3. Run `python generate_app_sponsor_logos.py`.

4. Upload the generated files `emnlp2019-sponsors.csv` and `sponsors-thumbs.zip` into the "Sponsors" custom list in the GuideBook builder.

## To generate the schedule for the GuideBook app

1. Make sure you have the files `order.txt`, `authors.csv`, `session-chairs.csv`, `abstracts.csv`, and `anthology-mapping.csv` under the `data` directory. (Note: If you need to regenerate `abstracts.csv`, you will need to run `python generate_abstract_csv.py --input abstracts --output data/abstracts.csv --anthology data/anthology-mapping.csv` where `abstracts` is the directory containing the individual abstract files obtained from the program/pub chairs). Note that `anthology-mapping.csv` is generated by screen-scraping the anthology webpages for EMNLP 2018.

2. Run `python parse_order_file_for_app.py --order data/order.txt --authors data/authors.csv --chairs data/session-chairs.csv --abstracts data/abstracts.csv --anthology data/anthology-mapping.csv` to generate the following files: 
    - `data/app/sessions.csv`
    - `data/app/authors.csv`
    - `data/app/papers.csv`
    - `data/app/linking.csv`

    Note that `sessions.csv`, `authors.csv` and `linking.csv` are already pre-populated (with tutorial and workshop info) and will be appended to rather than created from scratch. `papers.csv` only pertains to posters and presentations and will be created from scratch.

3. Make sure you have the following Guidebook template files in the `data/app` directory:

    - `CustomListItem_Link_template.csv`
    - `Guidebook_CL_Template.csv`
    - `Guidebook_Schedule_Template.csv`
    - `Sessions_Link_template.csv`

4. Run `python fill_in_app_templates.csv --sessions data/app/sessions.csv --authors data/app/authors.csv --papers data/app/papers.csv --linking data/app/linking.csv` to generate the follwing files:
    - `data/app/all-sessions-ids-as-names.csv`
    - `data/app/all-authors-ids-as-names.csv`
    - `data/app/authors-to-presentations-links.csv`
    - `data/app/sessions-to-presentations-links.csv`

5. Upload the file `all-sessions-ids-as-names.csv` into the "Full Schedule" section of the app.

6. Upload the file `all-authors-ids-as-names.csv` into the "All Authors" custom list section of the app.

7. Upload the file `authors-to-presentations-links.csv` into the "Links" part of the "All Authors" section of the app.

8. Upload the file `sessions-to-presentations-links.csv` into the "Links" part of the "Full Schedule" section of the app.

9. Export the CSVs for the "Schedule Sessions" and "Authors" from the Guidebook dashboard under "Advanced Tools" -> "Export Data".

10. Run `python replace_ids_with_names_in_exports.csv <csv1> <csv2> --sessions data/app/sessions.csv --authors data/app/authors.csv --papers data/app/papers.csv` where `<csv1>` and `<csv2>` are the names of the exported CSV files for schedule sessions and authors respectively. This command will generate the following new files:

    - `data/app/sessions-import-with-names.csv`
    - `data/app/authors-import-with-names.csv`

11. Upload the above two files into the "Full Schedule" and "All Authors" sections of the app respectively.

12. Make sure the "Schedule" section in the app is disabled. Add "Conference Sessions", "Main Papers & Posters", "Tutorials", and "Workshops" tracks as menu items. 

13. Reorder the "All Authors" item by selecting "Quick Reorder" and choosing "By Last Word (A -> Z)".

14. Manually link the TACL paper PDFs (under `downloads`) to the relevant papers in the app. 
