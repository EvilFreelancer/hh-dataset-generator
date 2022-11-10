import json
import os
import re
import html
import csv
from datetime import datetime

# Datetime object containing current date and time
now = datetime.now()


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
vacancies = os.listdir('./docs/vacancies')
vacanciesCount = len(vacancies)
i = 0
for fl in vacancies:
    # Increment counter
    i = i + 1

    # Open file
    f = open('./docs/vacancies/{}'.format(fl), encoding='utf8')
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
    description = strip_tags(jsonArr['description'])
    key_skills = ",".join([key_skill.get('name') for key_skill in jsonArr['key_skills']])

    # Status report
    message = '[{}/{}] id:{} name:{}'.format(i, vacanciesCount, id, name)
    print(message)

    # Put data to file
    filewriter.writerow([name + " " + description, key_skills])
