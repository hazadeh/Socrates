# Beautiful soup is for HTML parsing
from bs4 import BeautifulSoup

# For working with data
import pandas as pd


# Opening the HTML file as a file
with open('test.html', 'r') as file:
    # Reading the contents of the file into varilable page
    page = file.read()

    # Converting into format that BFsoup can parse
    soup = BeautifulSoup(page, 'lxml')

# create a list , that will contain pairs of "Text" & "URLS"
text_and_url = []

# For every link found in soup, which is just contents of the HTML page
for link in soup.findAll('a'):
    text_and_url.append({'text': link.string, 'url': link.get('href')})
    # Add a pair of the text and the url associated with the link in this loop iteration to the text_and_irl list

# Create a dataframe with the list in it
df = pd.DataFrame(text_and_url)

# Print dataframe onto csv
df.to_csv('test.csv', index=False, header=False)