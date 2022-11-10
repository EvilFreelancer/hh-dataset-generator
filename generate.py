# -*- coding: utf-8 -*-

import json
import os
import re
import html
import csv
import glob
from datetime import datetime

# Datetime object containing current date and time
now = datetime.now()

# Load JSON files
excludes = json.loads(open('./excludes.json', "r").read())
aliases = json.loads(open('./aliases.json', "r").read())

# https://stackoverflow.com/questions/753052/strip-html-from-strings-in-python
def strip_tags(value):
    """Returns the given HTML with all tags stripped."""
    tag_re = re.compile(r'(<!--.*?-->|<[^>]*>)')
    # Remove well-formed tags, fixing mistakes by legitimate users
    no_tags = tag_re.sub('', value)
    # Clean up anything else by escaping
    return html.escape(no_tags)


# Open CSV file for writing in append mode
suffix = now.strftime("%Y-%m-%d_%H:%M")
csvfile = open('./docs/csv/output_' + suffix + '.csv', 'a')
filewriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
filewriter.writerow(['text', 'keys'])

# Get list of all scrapped vacancies
vacancies = glob.glob('./docs/vacancies/*')
vacanciesCount = len(vacancies)
i = 0
for fl in vacancies:
    # Increment counter
    i = i + 1

    # Open file
    f = open(fl, encoding='utf8')
    jsonText = f.read()
    f.close()

    # Read JSON to array format
    jsonArr = json.loads(jsonText)

    # If key_skills list is empty, then skip this step
    if not jsonArr['key_skills']:
        continue

    # Extract only required fields
    id = jsonArr['id']
    name = jsonArr['name']
    description = strip_tags(jsonArr['description']).lower()
    key_skills = [skill.get('name') for skill in jsonArr['key_skills']]

    # Damn... Pandas, Numpy, Matplotlib / Plotly
    tmpKeySkills = []
    for skill in key_skills:
        if ',' in skill:
            tmpKeySkills + skill.split(',')
        else:
            tmpKeySkills.append(skill)

    # Sanitize list
    filterKeySkills = []
    for skill in tmpKeySkills:
        _skill = skill.lower().strip().rstrip('.')
        # Let's skip excludes
        if _skill in excludes:
            continue

        # Check if skill is not an alias
        filterSkill = _skill
        for key, value in aliases.items():
            if _skill in value:
                filterSkill = key.lower()

        # Add to output array
        filterKeySkills.append(filterSkill)

    # Sort and remove duplicates
    filterKeySkills = sorted(set(filterKeySkills))

    # Parse skill, we need keys which exists in text
    skills = []
    for skill in filterKeySkills:
        # Check if skill from keys is in main text
        if re.search(r'' + re.escape(skill), name + ' ' + description, re.MULTILINE | re.IGNORECASE):
            skills.append(skill)

    # If key_skills list is empty, then skip this step
    if not skills:
        continue

    # Build string of skills
    skills = sorted(skills)
    skills = ",".join(skills)

    # Status report
    message = '[{}/{}] id:{} skills:{}'.format(i, vacanciesCount, id, skills)
    print(message)

    # Put data to file
    filewriter.writerow([name + " " + description, skills])
