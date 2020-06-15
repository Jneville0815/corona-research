import requests
import time
from bs4 import BeautifulSoup
import csv

# Traverse URL's and create a list of them
article_list = []
with open("BBC.csv") as f:
    for row in f:
        article_list.append(row.split(',')[0])

# Remove header
article_list.pop(0)

i = 0
content_list = []
for url in article_list: 
	try:
		page = requests.get(url).text
	except:
		time.sleep(5)
		continue

	# Turn page into BeautifulSoup object to access HTML tags
	soup = BeautifulSoup(page, features="html.parser")

	# Get text from all <p> tags.
	p_tags = soup.find_all('p')

	# Get the text from each of the “p” tags and strip surrounding whitespace.
	p_tags_text = [tag.get_text().strip() for tag in p_tags]

	# Filter out sentences that contain newline characters '\n' or don't contain periods.
	sentence_list = [sentence for sentence in p_tags_text if not '\n' in sentence]
	sentence_list = [sentence for sentence in sentence_list if '.' in sentence]

	# Combine list items into string.
	article = ' '.join(sentence_list)

	content_list.append(article)

	print(i)

	i+=1


# Write URL's to new csv file
counter = 0
thecsv = csv.writer(open("BBC-content-all.csv", 'w'))
for content in content_list:
    thecsv.writerow([article_list[counter], content])
    counter+=1