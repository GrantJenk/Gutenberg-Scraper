import sys
import requests
from bs4 import BeautifulSoup
import csv
import string

book_num = sys.argv[1]
url = "https://www.gutenberg.org/files/" + book_num + "/" + book_num + "-h/" + book_num + "-h.htm"
r = requests.get(url)
soup = BeautifulSoup(r.content, "html.parser")
book_paragraphs = soup.find_all("p")

csv_file = open("" + book_num + ".csv", "w")
csv_writer = csv.writer(csv_file)

word_dict = {}
book_text = ""


def add_word(word):
    if word in word_dict:
        word_dict[word] += 1
    else:
        word_dict[word] = 1

def remove_punctuation(word):
    result = ""
    for char in word:
        if char not in string.punctuation:
            if char == "“" or char == "”":
                continue
            result += char

    return result.lower()


for paragraph in book_paragraphs:
    p = str(paragraph.text)
    p = p.replace("—", " ")
    for wrd in p.split():
        word_no_punc = remove_punctuation(wrd)
        add_word(word_no_punc)

word_list_ordered = sorted(word_dict.items(), reverse=True, key=lambda x: x[1])

csv_writer.writerow(["Word", "Count"])

for elem in word_list_ordered:
    csv_writer.writerow([elem[0], elem[1]])

csv_file.close()
